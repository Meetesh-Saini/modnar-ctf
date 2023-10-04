import os
from flask import Flask, render_template, make_response, Response, redirect
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies
)
from roles import roles

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

with open("flag") as f:
    FLAG = f.read().strip()

jwt = JWTManager(app)

@app.route("/")
def home():
    resp = make_response(render_template("index.html"))
    access_token = create_access_token(identity={
        "role" : "guest"
    })
    set_access_cookies(resp, access_token)
    return resp, 200

@app.route("/internal-admin-page")
@jwt_required()
def internal():
    token = get_jwt_identity()
    if "read-admin" in roles[token["role"]]["permissions"]:
        return FLAG
    return Response(status=400)

@app.route("/view-permissions")
@jwt_required()
def view_permissions():
    token = get_jwt_identity()
    if "read" in roles[token["role"]]["permissions"]:
        return roles
    return Response(status=400)

@app.route("/source")
def source():
    return redirect("https://github.com/Meetesh-Saini/modnar-ctf")