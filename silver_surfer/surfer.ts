#!/usr/bin/env ts-node
import * as Koa from "koa"
import * as Router from "koa-router"
import * as puppeteer from 'puppeteer'
import * as FLAG from './flags'

// load flags from ./flags.js
console.log("Flag", FLAG)

const app = new Koa()
const router = new Router()
const PORT = 8075

const browserPromise = puppeteer.launch({args: ["--no-sandbox"]})

function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function surf(code: string) {
    const browser = await browserPromise
    const page = await browser.newPage()
    await page.setRequestInterception(true)
    page.on('request', r => (
            r.url().startsWith("http:") ||
            r.url().startsWith("https:") ||
            (
                r.url().startsWith("file://") && (
                r.url().endsWith("static/kuchen.html") ||
                r.url().endsWith("static/blech.css") ||
                r.url().endsWith("static/flags.ts")
            )) ? r.continue() : r.abort() && console.log("blocked", r.url())
            )
    )
    console.log(await page.goto("file:///app/static/kuchen.html"))

    try {
        await page.evaluate(code)
    } catch (e) {
        return `<p>${e}</p>`
    }

    await sleep(1000)
    await page.close()
    return `<p>executed ${code}</p>`
}
        
browserPromise.catch(x => console.error("Error in browserpromise", x))

router.get('/', async (ctx, next) => {
    console.log("request incoming", ctx)
    const code = ctx.request.query.code
    console.log(code)
    if (code != undefined) {
        console.log(code)
        ctx.body = await surf(code)
    } else {
        ctx.body = '<p>No "code" parameter provided</p>'
    }
})

app.use(router.routes()).use(router.allowedMethods())

const server = app.listen(PORT, () => {
  console.log(`Server listening on port: ${PORT}`)
})