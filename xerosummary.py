import os
import json
import base64
import requests

TOKEN_URL = "https://identity.xero.com/connect/token"
ACCOUNTING_BASE = "https://api.xero.com/api.xro/2.0"
TOKENS_FILE = "xero_tokens.json"


def load_tokens():
    with open(TOKENS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tokens(tokens):
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)


def refresh_access_token(refresh_token: str) -> dict:
    client_id = os.environ["XERO_CLIENT_ID"]
    client_secret = os.environ["XERO_CLIENT_SECRET"]

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {basic}"}
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    r = requests.post(TOKEN_URL, data=data, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


#-----------------same for every case till now------------------------

def fetch_bank_summary_json(access_token: str, tenant_id: str, from_date: str, to_date: str) -> dict:
    url = f"{ACCOUNTING_BASE}/Reports/BankStatementsPlus"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "xero-tenant-id": tenant_id,
        "Accept": "application/json",
    }
    params = {"fromDate": from_date, "toDate": to_date}

    r = requests.get(url, headers=headers, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def get_bank_summary_json(from_date: str, to_date: str) -> dict:
    tokens = load_tokens()

    refreshed = refresh_access_token(tokens["refresh_token"])
    access_token = refreshed["access_token"]

    # refresh token can rotate — keep the newest one
    tokens["refresh_token"] = refreshed.get("refresh_token", tokens["refresh_token"])
    save_tokens(tokens)

    payload = fetch_bank_summary_json(access_token, tokens["tenant_id"], from_date, to_date)
    return payload


if __name__ == "__main__":
    payload = get_bank_summary_json("2025-01-01", "2025-01-31")

    # Print full JSON nicely
    print(json.dumps(payload, indent=2))
