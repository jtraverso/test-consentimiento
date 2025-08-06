import json
import requests

def make_response(body, status_code=200):
    return {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
        },
        "statusCode": status_code,
        "body": json.dumps(body) if not isinstance(body, str) else body
    }

def main(context):
    API_BASE = "https://demos2.vu-one.com"
    API_KEY = "17532252-8942-3036-v5eR-YRy5dV5OtxYK"
    JSESSIONID = "D8D3DC4396DC313EEE1601EE2F8B6B2F"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    cookies = {"JSESSIONID": JSESSIONID}

    method = context.req.method.upper()

    # CORS preflight (OPTIONS)
    if method == "OPTIONS":
        return make_response({}, 200)

    if method == "GET":
        template_id = context.req.query.get("id", "2")
        r1 = requests.get(
            f"{API_BASE}/consent/consentTemplate/getConsentTemplateById?id={template_id}",
            headers=headers, cookies=cookies
        )
        if r1.status_code != 200:
            return make_response(
                {"error": "Error obteniendo consentimiento", "details": r1.text}, 500
            )
        data = r1.json()
        name = "CT-TOS-TANNER-CL"
        version = "1.0.1"
        r2 = requests.get(
            f"{API_BASE}/consent/consentTemplate/getLegalTextByNameAndVersion?name={name}&version={version}",
            headers=headers, cookies=cookies
        )
        if r2.status_code != 200:
            legal_text = None
        else:
            legal_text = r2.json().get("legalText")
        data["legalText"] = legal_text
        return make_response(data, 200)

    elif method == "POST":
        body = context.req.body.decode() if isinstance(context.req.body, bytes) else context.req.body
        try:
            data = json.loads(body)
        except Exception as e:
            return make_response({"error": "JSON inválido", "details": str(e)}, 400)
        r = requests.post(
            f"{API_BASE}/consent/consentUser/save",
            headers=headers, cookies=cookies, json=data
        )
        if r.status_code != 200:
            return make_response(
                {"error": "Error guardando consentimiento", "details": r.text}, 500
            )
        return make_response(r.json(), 200)

    else:
        return make_response({"error": "Método no soportado"}, 405)
