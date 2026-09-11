import socket
from datetime import datetime

from flask import Flask, jsonify


app = Flask(__name__)


@app.get("/")
def inicio():
    return jsonify(mensaje="Backend funcionando")


@app.get("/api/info")
def informacion():
    return jsonify(
        hora=datetime.now().astimezone().isoformat(timespec="seconds"),
        pod=socket.gethostname(),
    )
