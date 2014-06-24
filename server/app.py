#!/usr/bin/env python2.7

from flask import Flask, make_response, render_template, request
import simplejson

app = Flask(__name__)

G = {
    "cmds": [],
    "outputs": {}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emit", methods=["POST"])
def emit():
    G["cmds"].append(request.data)
    return ''

@app.route("/cmd", methods=["GET"])
def cmd():
    return '%s,%s' % (len(G["cmds"])-1, G["cmds"][-1])

@app.route("/result", methods=["POST"])
def result():
    seq, data = request.data.split(',', 1)
    seq = int(seq)
    if seq < len(G["cmds"]) and seq not in G["outputs"]:
        G["outputs"][int(seq)] = data
    return ''

@app.route("/display", methods=["GET", "POST"])
def display():
    result = []
    for k, v in enumerate(G["cmds"][-10:]):
        result.append([k, G["cmds"][k], G["outputs"].get(k, "<not response yet>")])
    return simplejson.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, port=4444)
