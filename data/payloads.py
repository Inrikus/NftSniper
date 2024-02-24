HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "content-type": "application/json",
    }
BM_PAYLOAD = {
        "currency": "",
        "tradeType": [0],
        "collections": ["657076832863162368"],
        "page": 1,
        "rows": 40,
        "orderBy": "amount_sort",
        "orderType": 1,
        "isBack": "1",
        "properties": [
            "GRADE->value=Common",
            "GRADE->value=Elite",
            "GRADE->value=Epic",
            "GRADE->value=Legend",],
    }

QP_PAYLOAD = {
    "currency": "",
    "tradeType": [0],
    "collections": ["672410811679416321"],
    "page": 1,
    "rows": 40,
    "orderBy": "amount_sort",
    "orderType": 1,
    "isBack": "1",
    "properties": [
        "GRADE->value=Epic",
        "GRADE->value=Elite",
        "GRADE->value=Legend",
        "GRADE->value=Mythical"],
}


BLUR_URL = "https://core-api.prod.blur.io/v1/collections/fusionist-quartan-primes/tokens?filters=%7B%22traits%22%3A%5B%5D%2C%22hasAsks%22%3Atrue%7D"
ELEM_URL = ""