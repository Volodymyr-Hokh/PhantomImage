from flask import Blueprint, request, jsonify

from api.database.repository import (
    add_user,
    get_user_by_telegram_id,
)
from schemas import UserInDB


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["POST"])
async def add_user_route():
    data = request.json
    user = await add_user(
        telegram_id=data["telegram_id"],
        username=data.get("username"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
    )
    return jsonify(UserInDB(**user.__dict__).model_dump())


@users.route("/", methods=["GET"])
async def get_user_by_telegram_id_route():
    telegram_id = request.args.get("telegram_id")
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        return jsonify(None)
    return jsonify(UserInDB(**user.__dict__).model_dump())
