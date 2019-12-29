#!/usr/bin/env ts-node
import * as Koa from "koa"
import * as Router from "koa-router"
import * as puppeteer from 'puppeteer'
import * as flags from "./flags";

const FLAG = flags.FLAG
console.log("FLAG:", FLAG)

const app = new Koa()
const router = new Router()
const PORT = 8075

const browserPromise = puppeteer.launch({args: ["--no-sandbox"]})

function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function surf(url: string) {
    const browser = await browserPromise
    const page = await browser.newPage()
    await page.setRequestInterception(true)
    page.on('request', r => r.url().startsWith("http") ? r.continue() : r.abort() && console.log("blocked", r.url()))
    // const host = new URL(url).host
    // console.log("Requesting host", host)
    await page.setCookie({
        name: "flag",
        value: FLAG,
        path: '/',
        secure: false,
        session: true,
        domain: "flagfriendly:8070",
        httpOnly: false,
    })
    await page.setCookie({
        name: "flag",
        value: FLAG,
        path: '/',
        secure: false,
        session: true,
        domain: "add.ip.here.local",
        httpOnly: false,
    })
    await page.goto(url)
    console.log(await page.content())

    await sleep(1000)
    await page.close()

}
        
browserPromise.catch(x => console.error)

router.get('/', async (ctx, next) => {
    const url = ctx.request.query.url
    console.log(url)
    await surf(url)
    ctx.body = 'done'
})
app.use(router.routes())

const server = app.listen(PORT, () => {
  console.log(`Server listening on port: ${PORT}`)
})

module.exports = server;
/*
await b.close()
await process.exit()
*/
