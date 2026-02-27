import time

from flask import Blueprint, request, jsonify, session

from config import get_db_config
from database import get_db
from ids import generate_id
from queries.wishlist import wishlist_claim_orphans, wishlist_list, wishlist_create, wishlist_delete
from serializers import row_to_item

bp = Blueprint("wishlist", __name__, url_prefix="/api")


def _current_user_id():
    return session.get("user_id")


@bp.route("/wishlist", methods=["GET"])
def list_wishlist():
    user_id = _current_user_id()
    if not user_id:
        return jsonify(error="Not authenticated"), 401
    conn = get_db()
    try:
        wishlist_claim_orphans(conn, user_id)
        rows = wishlist_list(conn, user_id)
        data = [row_to_item(row) for row in rows]
        db_info = get_db_config()
        db_name = db_info.get("dbname", "DATABASE_URL") if isinstance(db_info, dict) else "url"
        print(f"[wishlist] DB: {db_name}, rows: {len(data)}")
        resp = jsonify(data)
        resp.headers["X-Wishlist-Count"] = str(len(data))
        return resp
    finally:
        conn.close()


@bp.route("/wishlist", methods=["POST"])
def create_item():
    user_id = _current_user_id()
    if not user_id:
        return jsonify(error="Not authenticated"), 401
    data = request.get_json() or {}
    name = data.get("name", "")
    image_url = data.get("imageUrl", "")
    link = data.get("link", "")
    price = data.get("price", "")
    item_id = generate_id()
    created_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    conn = get_db()
    try:
        row = wishlist_create(conn, user_id, item_id, name, image_url, link, price, created_at)
        return jsonify(row_to_item(row)), 201
    finally:
        conn.close()


@bp.route("/wishlist/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    user_id = _current_user_id()
    if not user_id:
        return jsonify(error="Not authenticated"), 401
    conn = get_db()
    try:
        deleted = wishlist_delete(conn, user_id, item_id)
        if deleted == 0:
            return jsonify(error="Not found"), 404
        return "", 204
    finally:
        conn.close()
