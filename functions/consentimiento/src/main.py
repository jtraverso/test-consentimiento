import json
import requests

def main(context):
    API_BASE = "https://demos2.vu-one.com"
    API_KEY = "17532252-8942-3036-v5eR-YRy5dV5OtxYK"
    JSESSIONID = "D8D3DC4396DC313EEE1601EE2F8B6B2F"
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    cookies = {"JSESSIONID": JSESSIONID}
    
    method = context.req.method

    # CORS preflight
    if method == "OPTIONS":
        response = context.res.json({})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    if method == "GET":
        template_id = context.req.query.get("id", "2")
        r1 = requests.get(
            f"{API_BASE}/consent/consentTemplate/getConsentTemplateById?id={template_id}",
            headers=headers, cookies=cookies
        )
        if r1.status_code != 200:
            response = context.res.json(
                {"error": "Error obteniendo consentimiento", "details": r1.text},
                status_code=500
            )
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            return response
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
        response = context.res.json(data)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    elif method == "POST":
        body = context.req.body.decode() if isinstance(context.req.body, bytes) else context.req.body
        try:
            data = json.loads(body)
        except Exception as e:
            response = context.res.json({"error": "JSON inválido", "details": str(e)}, status_code=400)
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            return response
        r = requests.post(
            f"{API_BASE}/consent/consentUser/save",
            headers=headers, cookies=cookies, json=data
        )
        if r.status_code != 200:
            response = context.res.json(
                {"error": "Error guardando consentimiento", "details": r.text},
                status_code=500
            )
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            return response
        response = context.res.json(r.json())
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    else:
        response = context.res.json({"error": "Método no soportado"}, status_code=405)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response
