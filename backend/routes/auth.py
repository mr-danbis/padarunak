import os
import secrets

import requests
from flask import Blueprint, redirect, session, jsonify

from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    FRONTEND_URL,
    API_URL,
)
from database import get_db
from queries.users import get_by_google_id, create, update_profile
from serializers import row_to_user

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
SCOPE = "openid email profile"


def _redirect_uri():
    base = API_URL.rstrip("/")
    return f"{base}/api/auth/callback"


@bp.route("/login")
def login():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        return redirect(f"{FRONTEND_URL}?error=oauth_not_configured")
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": _redirect_uri(),
        "response_type": "code",
        "scope": f"{SCOPE}",
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    return redirect(f"{GOOGLE_AUTH_URL}?{qs}")


@bp.route("/callback")
def callback():
    from flask import request

    err = request.args.get("error")
    if err:
        return redirect(f"{FRONTEND_URL}?error={err}")
    state = request.args.get("state")
    if not state or state != session.get("oauth_state"):
        return redirect(f"{FRONTEND_URL}?error=invalid_state")
    session.pop("oauth_state", None)
    code = request.args.get("code")
    if not code:
        return redirect(f"{FRONTEND_URL}?error=no_code")

    token_resp = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": _redirect_uri(),
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    if token_resp.status_code != 200:
        return redirect(f"{FRONTEND_URL}?error=token_failed")
    data = token_resp.json()
    access_token = data.get("access_token")
    if not access_token:
        return redirect(f"{FRONTEND_URL}?error=no_token")

    user_resp = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if user_resp.status_code != 200:
        return redirect(f"{FRONTEND_URL}?error=userinfo_failed")
    info = user_resp.json()
    google_id = info.get("id")
    email = (info.get("email") or "").strip().lower()
    if not google_id or not email:
        return redirect(f"{FRONTEND_URL}?error=invalid_userinfo")
    if not email.endswith("@gmail.com") and not email.endswith("@googlemail.com"):
        return redirect(f"{FRONTEND_URL}?error=only_gmail")

    conn = get_db()
    try:
        user = get_by_google_id(conn, google_id)
        name = info.get("name") or ""
        picture_url = info.get("picture") or ""
        if not user:
            user = create(conn, google_id=google_id, email=email, name=name, picture_url=picture_url)
        else:
            update_profile(conn, user["id"], name, picture_url)
            user = get_by_google_id(conn, google_id)
        session["user_id"] = user["id"]
        return redirect(FRONTEND_URL)
    finally:
        conn.close()


@bp.route("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(error="Not authenticated"), 401
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            session.pop("user_id", None)
            return jsonify(error="User not found"), 401
        return jsonify(row_to_user(row))
    finally:
        conn.close()


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_id", None)
    return redirect(FRONTEND_URL)
