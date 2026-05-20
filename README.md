# SAML Token Generator - Netlify

Serverless function that generates signed SAML assertions and exchanges them for OAuth tokens via Okta.

## Project Structure

```
NetlifySAMLAssertion/
├── netlify.toml                           # Netlify configuration
├── public/
│   └── index.html                         # Web UI
├── netlify/
│   └── functions/
│       ├── generate-saml-assertion.py     # Serverless function
│       └── requirements.txt               # Python dependencies
├── runbook.md                             # Okta setup guide
└── README.md
```

## Deploy to Netlify

### Via CLI

```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

### Via Git

1. Push to GitHub/GitLab
2. Connect repo to Netlify

## API Usage

**POST** `/generate-saml-assertion`

```bash
curl -X POST https://your-site.netlify.app/generate-saml-assertion \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

### Response

```json
{
  "saml_assertion": "base64-encoded-assertion",
  "token_response": {
    "access_token": "...",
    "id_token": "...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

## Local Development

```bash
netlify dev
```
