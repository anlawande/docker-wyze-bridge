from typing import Any

from flask import Flask, render_template, jsonify, request
from flask_httpauth import HTTPBasicAuth
import json

wb: Any = None

def init(app: Flask, auth: HTTPBasicAuth, _wb: Any):
    global wb
    wb = _wb

    @app.route("/gas")
    @auth.login_required
    def get():
        print("server")
        return render_template("gas.html")

    @app.route("/gas/markers")
    @auth.login_required
    def get_marker_positions():
        f = open("img/markers.json", "r")
        response = app.response_class(
            response=f.read(),
            status=200,
            mimetype='application/json'
        )
        return response

    @app.route("/gas/markers", methods=["POST"])
    @auth.login_required
    def save_marker_positions():
        f = open("img/markers.json", "w")
        json_object = json.dumps(request.json, indent=4)
        f.write(json_object)

        return "Success"
