from flask import Blueprint, request, jsonify

from api.utils import generate_image_async


images = Blueprint("images", __name__, url_prefix="/images")


@images.route("/generate", methods=["POST"])
async def generate_image():
    data = request.json
    image_path = data["image_path"]
    prompt = data["prompt"]
    result = await generate_image_async(image_path, prompt)
    return jsonify({"result": result})
