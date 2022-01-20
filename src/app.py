import json
import requests
from flask import Flask, render_template, session, request

BASE_API = "https://diamondapp.com/api/v0/"

config = json.load(open("config.json", "r"))
app = Flask(__name__)
# feel free to change secret key but keep it private
# This is used to safely store data in flask session locally in the browser
# idk how safe this is tho
app.secret_key = config["FLASK_SECRET_KEY"]
app.debug = True

reciever = config["TEST_RECIEVER"]


@app.route("/")
def home():
    try:
        logged_in_key = session["LoggedInUser"]
    except Exception:
        logged_in_key = None

    if logged_in_key:
        return render_template("home.html", data={"loggedInKey": logged_in_key, "reciever": reciever})
    else:
        return render_template("home.html", data={"reciever": reciever})


@app.route("/login", methods=["POST"])
def login():
    # once logged in, you can perform actions on this public key
    data = request.get_json(force=True)
    session["LoggedInUser"] = data["PublicKey"]
    return "OK"


@app.route("/create-txn", methods=["POST"])
def create_txn():
    payload = request.get_json(force=True)
    endpoint = BASE_API + payload["Endpoint"]
    data = payload["Data"]
    res = requests.post(endpoint, json=data)
    if res.status_code == 200:
        return res.json()["TransactionHex"]
    else:
        print(res.status_code, res.text)
        return None


@app.route("/submit-txn", methods=["POST"])
def submit():
    payload = request.get_json(force=True)
    endpoint = BASE_API + "submit-transaction"
    data = {
        "TransactionHex": payload["TransactionHex"]
    }
    res = requests.post(endpoint, json=data)
    if res.status_code == 200:
        return res.json()["TxnHashHex"]
    else:
        print(res.status_code, res.text)
        return None


app.run()
