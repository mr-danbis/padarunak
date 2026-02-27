from flask import Blueprint, jsonify

from database import get_db
from queries.home import home_get_collections
from serializers import row_to_product

bp = Blueprint("home", __name__, url_prefix="/api")


@bp.route("/home", methods=["GET"])
def home_collections():
    conn = get_db()
    try:
        collections_raw = home_get_collections(conn)
        result = [
            {
                "id": c["id"],
                "name": c["name"],
                "products": [row_to_product(p) for p in c["products"]],
            }
            for c in collections_raw
        ]
        return jsonify({"collections": result})
    finally:
        conn.close()
