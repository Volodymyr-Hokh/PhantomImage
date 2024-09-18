import asyncio

from flask import Flask, request, jsonify

from api.blueprints.users import users
from api.blueprints.images import images


app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(images)


@app.route("/test", methods=["GET"])
async def test():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(port=8443)
