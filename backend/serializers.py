"""Строки БД → dict для API (camelCase, даты в ISO)."""


def row_to_item(row):
    created = row["created_at"]
    if hasattr(created, "isoformat"):
        created = created.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {
        "id": row["id"],
        "name": row["name"],
        "imageUrl": row["image_url"],
        "link": row["link"],
        "price": row["price"],
        "createdAt": created,
    }


def row_to_user(row):
    return {
        "id": row["id"],
        "email": row["email"],
        "name": row["name"],
        "pictureUrl": row["picture_url"] or "",
    }


def row_to_product(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "link": row["link"],
        "imageUrl": row["image_url"],
    }
