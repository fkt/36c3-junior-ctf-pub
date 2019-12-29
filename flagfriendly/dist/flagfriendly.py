#!/usr/bin/env python3
import requests
from flag import flag
from flask import Flask, request, redirect, make_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    title = request.args.get("title", default="Flags for Friendly Fellows", type=str)
    if request.cookies.get("flag") == flag:
        # Make sure the filename never leaks!
        path = flag
    else:
        path = "static/flag"
    response = make_response(
        f"""<!doctype html>
<html>
<head>
   <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <img src="/{path}.gif"/>
</body>
</html>"""
    )
    response.headers["Content-Security-Policy"] = "img-src *; default-src 'none';"
    return response


@app.route("/report")
def report():
    """
    This can be used to make bots surf this site.
    Bots will have the flag cookie set accordingly.
    """
    url = request.args.get("url", default="", type=str)
    if not url:
        return "No url parameter provided to surf to"
    return requests.get(f"http://surfer:8075?url={url}").text


@app.route(f"/{flag}.gif")
def show_gif():
    return redirect("/static/flag.gif")


if __name__ == "__main__":
    app.run()
