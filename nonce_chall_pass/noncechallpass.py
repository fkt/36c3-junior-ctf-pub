#!/usr/bin/env python3
import secrets
import requests
import urllib.parse
from flask import Flask, request, make_response

app = Flask(__name__)

with open("./static/html2canvas.min.js") as f:
    html2canvas = f.read()

@app.route("/", methods=["GET"])
def design_me():
    loadmsg = request.args.get("loadmsg", default="Loading...", type=str)
    contenturl = (
        request.args.get("contenturl", default="static/gabbagandalf.gif.html", type=str)
        .replace("\\", "")
        .replace('"', "")
    )
    contenttime = request.args.get("contenttime", default=0, type=int)
    reporturl = (
        request.args.get("reporturl", default="", type=str)
        .replace("\\", "")
        .replace('"', "")
    )
    reporttime = request.args.get("reporttime", default=500, type=int)
    nonce = hex(secrets.randbits(64))[2:]
    response = make_response(
        f"""
<html>
<head>
    <title>Nonce Chall Pass</title>
    <script nonce={nonce}> 
    async function loadContent() {{
        let contentDiv = document.querySelector("#content")
        let request = contentDiv.getAttribute("contenturl")
        let response = await fetch(request)
        let content = await response.text() 
        contentDiv.innerHTML = content
    }}
    setTimeout(loadContent, {contenttime});

    async function report() {{
        const contentDiv = document.querySelector("#content")
        const reporturl = contentDiv.getAttribute("reporturl")
        if (reporturl) {{
            html2canvas(document.body, {{ onrendered: async function(x) {{
                    const screenshot = x.toDataURL()
                    let response = await fetch(reporturl, {{
                        method: 'POST',
                        body: `<img src="${{screenshot}}" />`
                    }})
                    console.log("Uploaded report", response)
                }}
            }})
        }} else {{
            console.log("No reporturl specified")
        }}
    }}
    setTimeout(report, {reporttime});

{html2canvas}
    </script>
    <style>
    body: {{
        color: red;
    }}
    </style>
</head>
<body nonc={nonce}>
    <h1>Nonce Chall Pass</h1>
    <div id="content" contenturl="{contenturl}" reporturl="{reporturl}">
        <p>{loadmsg}</p>
    </div>
    gabbagandalf
</body>
</html>
"""
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; "
        "connect-src *; "
        "style-src 'unsafe-inline'; "
        f"script-src 'nonce-{nonce}'; "
        "img-src data:; "
        "frame-ancestors 'none'"
    )
    return response


@app.route("/report")
def report():
    params = "&".join([f"{key}={value}" for key, value in request.args.items() if key is not "url"])
    url = f"http://noncechallpass:8010?{params}"
    print("Requesting", url)
    return requests.get("http://surfer:8075", params={'url': url}).text


if __name__ == "__main__":
    app.run()
