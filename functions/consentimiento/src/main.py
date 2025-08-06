import json
import requests

def main(context):
    # Configuración
    API_BASE = "https://demos2.vu-one.com"
    API_KEY = "17532252-8942-3036-v5eR-YRy5dV5OtxYK"
    JSESSIONID = "D8D3DC4396DC313EEE1601EE2F8B6B2F"
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    cookies = {"JSESSIONID": JSESSIONID}
    
    method = context.req.method
    
    if method == "GET":
        # 1. Trae los datos del consentimiento por ID
        template_id = context.req.query.get("id", "2")
        r1 = requests.get(
            f"{API_BASE}/consent/consentTemplate/getConsentTemplateById?id={template_id}",
            headers=headers, cookies=cookies
        )
        if r1.status_code != 200:
            return context.res.json(
                {"error": "Error obteniendo consentimiento", "details": r1.text},
                status_code=500
            )
        data = r1.json()
        
        # 2. Trae el legalText por name/version fijo o los retornados
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
        
        # 3. Combina los datos y retorna todo junto
        data["legalText"] = legal_text
        return context.res.json(data)
    
    elif method == "POST":
        # Guarda el consentimiento
        body = context.req.body.decode() if isinstance(context.req.body, bytes) else context.req.body
        try:
            data = json.loads(body)
        except Exception as e:
            return context.res.json({"error": "JSON inválido", "details": str(e)}, status_code=400)
        r = requests.post(
            f"{API_BASE}/consent/consentUser/save",
            headers=headers, cookies=cookies, json=data
        )
        if r.status_code != 200:
            return context.res.json(
                {"error": "Error guardando consentimiento", "details": r.text},
                status_code=500
            )
        return context.res.json(r.json())
    
    else:
        return context.res.json({"error": "Método no soportado"}, status_code=405)
