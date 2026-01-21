# Xero-API-GET-request
This repository is designed to help everyone easily interact with Xero’s API - specifically for making GET requests to Xero endpoints, cause other requests might break Xero :)


XERO API FETCH-ONLY GUIDE
This repository provides a simple way to connect to the Xero Accounting API and perform GET-only requests. It handles authentication once, saves your tokens, and lets you safely fetch data from Xero without modifying anything.

CREATE A XERO APP
Log in to the Xero Developer Portal: https://developer.xero.com/
Create a "Web Application"
Company URL: use http://localhost or any GitHub URL
Redirect URI: http://localhost:8080/callback
Save your Client ID and Client Secret


SET ENVIRONMENT VARIABLES (PowerShell)
Set the following:

$env:XERO_CLIENT_ID="CLIENT_ID"
$env:XERO_CLIENT_SECRET="CLIENT_SECRET"
$env:XERO_REDIRECT_URI="http://localhost:8080/callback"
Replace CLIENT_ID and CLIENT_SECRET with your own values. Keep the redirect URI exactly as shown.

RUN INITIAL AUTHORIZATION
Run:

python bootstrap.py
A browser will open. Log in to Xero, choose your organization, and authorize the connection. This step needs to be done only once.

ACTIVATE TOKEN CREDENTIALS
Run:

python xerobootstrap.py
This loads your stored tokens and prepares the authenticated connection for all future GET requests.

RUN YOUR FETCH SCRIPTS
Execute any script that fetches data from Xero, for example:

python get_invoices.py
Tokens will refresh automatically. No need to authorize again.

CLEAN THE JSON OUTPUT
After receiving a JSON response from Xero, you can clean and convert it into a usable format.

Example:
import json
import pandas as pd
with open("response.json") as f:
data = json.load(f)
df = pd.json_normalize(data, sep="_")
df.to_csv("clean_output.csv", index=False)
This converts the raw JSON into a tabular format suitable for reporting, reconciliation, analytics, or database loading.
SUMMARY

Authenticate once
Store tokens locally
Run fetch scripts anytime
Only GET requests (safe, read-only)
Clean the JSON into a usable dataset
