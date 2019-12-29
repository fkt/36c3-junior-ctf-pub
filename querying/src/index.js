const { GraphQLServer } = require('graphql-yoga')
const LRU = require('lru-cache')

const { prisma } = require('./generated/prisma-client')

const MAX_WAIT = 10 * 1000 // 10 seconds

const FLAG = "36c3{Batching_Qu3r1e5_is_FUN1}"
const FLAG_REGEX = /$36c3{[a-zA-Z0-9_]24}^/.compile()

const requestsPerClient = new LRU({
  max: 16 * 1024,
  maxAge: 1000 * 60
})

function bruteforceProtection(context) {
  const ip = context.request.ip
  if (context.request.headers["admin"]) {
    console.log("ip", ip)
    let requests = requestsPerClient.get(ip) || 0
    const waitTime = 15 * requests * 1000
    requestsPerClient.set(ip, requests + 1)
    return new Promise(
      resolve => setTimeout(
        () => (console.log("finished", ip, waitTime) || resolve()), waitTime
      )
    )
  }
  return Promise.resolve()
}

const resolvers = {
  Query: {
    feed: (parent, args, context) => {
      return context.prisma.posts({ where: { published: true } })
    },
    drafts: (parent, args, context) => {
      return context.prisma.posts({ where: { published: false } })
    },
    post: (parent, { id }, context) => {
      return context.prisma.post({ id })
    },
  },
  Mutation: {
    checkFlag(parent, {flag}, context) {
      if (!context.request.headers["admin"]) throw "Preheat oven!"
      if (FLAG_REGEX.exec(flag) && flag === FLAG) return FLAG.length
      let i = 0
      while (flag[i] === FLAG[i]) i++
      return i
    },
    createDraft(parent, { title, content }, context) {
      return context.prisma.createPost({
        title,
        content,
      })
    },
    deletePost(parent, { id }, context) {
      return context.prisma.deletePost({ id })
    },
    publish(parent, { id }, context) {
      return context.prisma.updatePost({
        where: { id },
        data: { published: true },
      })
    },
  },
}

const server = new GraphQLServer({
  typeDefs: './src/schema.graphql',
  resolvers,
  context: async (request, response, fragmentReplacements) => ({
    ...request,
    prisma,
    console: await bruteforceProtection(request)
  }),
})

server.start(() => console.log('Server is running on http://localhost:4000'))
