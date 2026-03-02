"""Превью по ссылке: загрузка страницы, парсинг OG/JSON-LD/script (без JS)."""

import json
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def fetch_link_preview(url):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None, "Некорректная ссылка"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            return None, "Сайт блокирует автоматическую загрузку (403). Добавьте товар вручную."
        if e.response is not None and e.response.status_code == 404:
            return None, "Страница не найдена (404)."
        return None, "Не удалось загрузить страницу. Добавьте товар вручную."
    except requests.exceptions.Timeout:
        return None, "Сайт не ответил вовремя. Попробуйте ещё раз или добавьте товар вручную."
    except requests.RequestException:
        return None, "Не удалось подключиться к сайту. Проверьте ссылку или добавьте товар вручную."

    soup = BeautifulSoup(resp.text, "html.parser")
    base_url = resp.url

    name = ""
    image_url = ""
    price = ""

    meta_og_title = soup.find("meta", property="og:title")
    if meta_og_title and meta_og_title.get("content"):
        name = meta_og_title["content"].strip()
    if not name:
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            name = title_tag.string.strip()

    meta_og_image = soup.find("meta", property="og:image")
    if meta_og_image and meta_og_image.get("content"):
        image_url = meta_og_image["content"].strip()
        if image_url.startswith(("/", "//")):
            image_url = urljoin(base_url, image_url)

    meta_price = soup.find("meta", property="product:price:amount")
    if meta_price and meta_price.get("content"):
        price = meta_price["content"].strip()
    meta_price_currency = soup.find("meta", property="product:price:currency")
    currency = meta_price_currency.get("content", "").strip() if meta_price_currency else ""

    def set_price(p_val):
        nonlocal price
        if p_val is not None and not price:
            price = str(p_val)
            if currency:
                price = f"{price} {currency}"

    def set_image(img_val):
        nonlocal image_url
        if not img_val or image_url:
            return
        if isinstance(img_val, list):
            img_val = img_val[0] if img_val else None
        if not img_val:
            return
        image_url_val = img_val if isinstance(img_val, str) else (img_val.get("url") or img_val.get("contentUrl"))
        if image_url_val:
            image_url = image_url_val
            if image_url.startswith(("/", "//")):
                image_url = urljoin(base_url, image_url)

    for script in soup.find_all("script", type="application/ld+json"):
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
            if not isinstance(data, dict):
                continue
            graphs = data.get("@graph", [data]) if "@graph" in data else [data]
            for node in graphs:
                if not isinstance(node, dict):
                    continue
                if node.get("@type") == "Product":
                    set_image(node.get("image"))
                    offers = node.get("offers") or {}
                    if isinstance(offers, list):
                        offers = offers[0] if offers else {}
                    p = offers.get("price") if isinstance(offers, dict) else None
                    if p is None and isinstance(node.get("offers"), dict):
                        p = node["offers"].get("price")
                    set_price(p)
                    if not name and node.get("name"):
                        name = node["name"].strip()
                    break
                if node.get("@type") == "ItemList":
                    for item in node.get("itemListElement") or []:
                        if isinstance(item, dict) and (item.get("item") or item.get("@type") == "ListItem"):
                            item_data = item.get("item") or item
                            if isinstance(item_data, dict) and item_data.get("@type") == "Product":
                                set_image(item_data.get("image"))
                                offers = item_data.get("offers") or {}
                                if isinstance(offers, list):
                                    offers = offers[0] if offers else {}
                                p = offers.get("price") if isinstance(offers, dict) else None
                                set_price(p)
                                if not name and item_data.get("name"):
                                    name = item_data["name"].strip()
                                break
        except (json.JSONDecodeError, TypeError):
            pass

    def _extract_from_obj(obj, path_names, path_image, path_price):
        nonlocal name
        if not isinstance(obj, dict):
            return
        for key in path_names:
            if key in obj and obj[key] and isinstance(obj[key], str):
                if not name:
                    name = obj[key].strip()
                break
        for key in path_image:
            if key in obj and obj[key]:
                val = obj[key]
                if isinstance(val, str):
                    set_image(val)
                elif isinstance(val, list) and val:
                    set_image(val[0])
                break
        for key in path_price:
            if key in obj and obj[key] is not None:
                set_price(obj[key])
                break

    for script in soup.find_all("script"):
        raw = script.string if script.string else ""
        if not raw or len(raw) < 50:
            continue
        stype = script.get("type") or ""
        if "application/ld+json" in stype:
            continue
        if stype and stype != "application/json":
            continue
        data = None
        try:
            text = raw.strip()
            if text.startswith("{"):
                data = json.loads(text)
            elif "=" in text and ("{" in text or "[" in text):
                for sep in (
                    "window.__DATA__ = ",
                    "window.__INITIAL_STATE__ = ",
                    "__NUXT_DATA__ = ",
                    "window.__PRELOADED_STATE__ = ",
                ):
                    if sep in text:
                        start = text.index(sep) + len(sep)
                        depth = 0
                        end = start
                        for i, c in enumerate(text[start:], start):
                            if c == "{":
                                depth += 1
                            elif c == "}":
                                depth -= 1
                                if depth == 0:
                                    end = i + 1
                                    break
                            elif c == "[" and depth == 0:
                                depth += 1
                        if depth == 0 and end > start:
                            data = json.loads(text[start:end])
                        break
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
        if data is None or not isinstance(data, dict):
            continue
        data = data.get("props", data) or data
        data = data.get("pageProps", data) or data
        data = data.get("data", data) or data
        if isinstance(data, dict):
            _extract_from_obj(
                data,
                ("name", "title", "productName", "product_name"),
                ("image", "imageUrl", "photo", "img", "picture"),
                ("price", "salePrice", "currentPrice", "priceWithDiscount"),
            )
        for key in ("product", "card", "item", "goods", "productInfo"):
            node = data.get(key) if isinstance(data, dict) else None
            if isinstance(node, dict):
                _extract_from_obj(
                    node,
                    ("name", "title", "productName", "product_name"),
                    ("image", "imageUrl", "photo", "img", "picture"),
                    ("price", "salePrice", "currentPrice", "priceWithDiscount"),
                )
            if name and image_url:
                break
        if name and image_url:
            break

    if not name.strip() and not image_url:
        return None, (
            "Не удалось получить данные со страницы. Сайт может подгружать контент через JavaScript. "
            "Добавьте товар вручную: нажмите «Добавить вручную», вставьте ссылку и заполните название и цену."
        )

    return (
        {
            "name": name or "Без названия",
            "imageUrl": image_url,
            "link": resp.url,
            "price": price,
        },
        None,
    )
