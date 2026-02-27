from flask import Blueprint, request, jsonify

from services.link_preview import fetch_link_preview

bp = Blueprint("link_preview", __name__, url_prefix="/api")


@bp.route("/link-preview", methods=["GET"])
def link_preview():
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify(error="Укажите url"), 400
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    data, err_msg = fetch_link_preview(url)
    if data is None:
        return jsonify(error=err_msg or "Не удалось загрузить страницу или получить данные"), 422
    return jsonify(data)
