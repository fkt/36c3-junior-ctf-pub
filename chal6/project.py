import os
from flask import Flask, render_template, render_template_string, request
app = Flask(__name__)

@app.route('/')
def index():
    with open(__file__) as f:
        return '<pre>' + "".join({'<':'&lt;','>':'&gt;'}.get(c,c) for c in f.read()) + '</pre>' + __file__

@app.route('/echo')
def echo():
    s = request.args.get('s')
    rendered_template = render_template("home.html", s=s)
    return render_template_string(rendered_template)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
