import uuid
import json
from datetime import datetime, timedelta, timezone
import base64
from lxml import etree
from signxml import XMLSigner, methods
import requests

# Hardcoded Certificates
CERT = """-----BEGIN CERTIFICATE-----
MIIC0DCCAbgCCQD4ymyYBcYvQDANBgkqhkiG9w0BAQsFADAqMSgwJgYDVQQDDB9i
YWxhLXNlY3VyZXMtYWkub2t0YXByZXZpZXcuY29tMB4XDTI2MDMxMTAyNDUyN1oX
DTI3MDMxMTAyNDUyN1owKjEoMCYGA1UEAwwfYmFsYS1zZWN1cmVzLWFpLm9rdGFw
cmV2aWV3LmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAK4QRhiP
FSAqWvLr6SnJjWH/u9KPxlL+twZlwvf+LKFO/I9kP89lcZI5117XDo3mryHWsab3
C5625w/HShY5otT8Cm/K5hLHnYMaBgd1oH9UiBmbeXCocJYWAwbAAJdJBft5FC62
Nr9q4K4WG0emn8H7EqqaHz1KYlEuzRUnsqI1TUx3vEaH4tFYt3qw8JC73bbA+eqz
4F5FG6ky2kqoY9IcNQwb+gsCXfkWR6dIGdMRPCwPbvi1Mc0BemqdGxmYs3MG2Y3c
V3gZTRLsIgko9djFLaT8uHRWcZtc26lqCkTU0B5iFj0uupWWlVvqi/RSnS4wtfnD
QTRXt5pTcDBV6k8CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAct7IKlgUbd2e04sd
6qmRxL2AAN4egEdNE2Tne1gFxEKcTg91GMBcMX3NrWgEOxy6xURJ15Le8FY8WXq/
aysRMWN4Er3DIqZ+gZotXoGC2JO+eSLL4kTuh0izQGSJ9e4NLXE/USidyjKSe7+K
TrgTWKYiihvsf7GCxdYVyifswOdr3YiTSUWBqbZaYIhnwcRwO2FFZ9NeNbI9bu36
MSy0vOSqpYMMUNURJfwjyplO8RzWawLGdb5WXwOdO4fFFTI21wSMGCA0VbRBi2KB
WwxOuKyBQ1C7u0ktJB4fMDwYzeRN4VLH3+GBwA0Z+kqUlLcdcM7uPXSgIHLnWx2V
QtFvsw==
-----END CERTIFICATE-----"""

KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCuEEYYjxUgKlry
6+kpyY1h/7vSj8ZS/rcGZcL3/iyhTvyPZD/PZXGSOdde1w6N5q8h1rGm9wuetucP
x0oWOaLU/ApvyuYSx52DGgYHdaB/VIgZm3lwqHCWFgMGwACXSQX7eRQutja/auCu
FhtHpp/B+xKqmh89SmJRLs0VJ7KiNU1Md7xGh+LRWLd6sPCQu922wPnqs+BeRRup
MtpKqGPSHDUMG/oLAl35FkenSBnTETwsD274tTHNAXpqnRsZmLNzBtmN3Fd4GU0S
7CIJKPXYxS2k/Lh0VnGbXNupagpE1NAeYhY9LrqVlpVb6ov0Up0uMLX5w0E0V7ea
U3AwVepPAgMBAAECggEAJ0dq2f3n0YNdVLYhvplJ+1RfSQvCwFXUbXAnSBkmbxxI
5/7CW4XT1CCTVkaHdUQaPzOYkUnsaFtz1t6s/EjzUsaxgDq0IobDJ6OGusYzeqhT
shugkuifx26eLjbDq2ACJpZTFJtvzVBL9VztuQSDxp1mv/LZm9YeS52ZD+4OZIXt
OMD4r9im8LgzTUIHOwWet4ejFPQKaXl1LLOTnLgWToUcNbXc4YI2aTCKm8razE9M
Y76kWdTpUzvCX8xS/RYnAc0YRi22kLDywmG6zBpBRzM+DcFfZbR53iCHl9k5Dl2N
Oc05jiS6eQRNPYUBmBR+ExCY/jsFTyQXGhVuLf66WQKBgQDhqXUMZUffFaL3nf2G
t3BvBL6hlZI2qOw29owCh54eBKF9CxW8zv6eAekq13aAGVvUEsNbASwi+faxD4ni
ZQrYEeKaLOa+5GFYf0TceGqSlZcBH1wkxfK4ZWCh92xVrEKTaUJ5Av6KE6hjV/gU
vOIU/ESnPT2Xwjoyki9kgqCfjQKBgQDFdvhYYVJ0HyeHXwGLCBG9/Zi1NWrKwwq1
nIidJQDoTMnUtRVbqMXVMrlYfc//a3cLFy9OjbsrCZXCYy50PsGLIV6DJK+C94mS
2u2d/RZMqi8jjivMxM7zNPCUmgl18LisOxQ8Nvsfh9q7+wLFF+7/VMpaimRC4Vfv
77T6o1LcSwKBgQDUIT8luuO4IxfCW+Niy3hG9JfbP8Zl2Z/L/zIYgrIxl7rS2CPE
DHWvxS4SFt+Phccb8dNw7gY2jvHG+kts5f0upol00zbKRdf4oBL0icHtL+/2nys4
alhD3RDc0MEnPDqNZkqVhSoQVHBbiutrWy/P+GD1MY1/5pZcya0BeAZUVQKBgE+M
yCvCuVbynhgZHCQIki06FuUZqfYZcR0M/LRiDeWH2d+JPBt6+IgVMToHJV4+yux6
4KIC0x5ZdC2lizdleM82GD847kQSuSeibwuww+UKwobOZbLOrpioASu8iocq/RrV
iidf9vcS4fnM+6avJ6dRX1vuWMngwm504TH/zgfVAoGAZz40DInQZYUb8ZFKPhYv
YahcVQDhHidSPhL0Ckz28J6pcl0CGcwovJwfqqdUUfKlZ4T3GGk+vL1wq6jfVu4T
PU39zaVoH+/avaSq3f7+FJyc+zztbeFcqW6pI7uFI6ijyci3TMV3Md0nIG22DSCH
xTfmps47fERyMgFrpdhtrZo=
-----END PRIVATE KEY-----"""

# Configuration
OKTA_DOMAIN = "bala-secures-ai.oktapreview.com"
MCP_GW_CLIENT_ID = "0oax1qvtg5B59aiRa1d7"
MCP_GW_CLIENT_SECRET = "sGGZlwdPZvdvD6X8N5ag2XjRGpV66LQ0G_ZBEQalTI4n6RHfBqfdi85pyPSrBQlC"
MCP_GW_IDP_ISSUER_URI = "https://mcp-gateway.saml-assertion"
MCP_GW_IDP_ACS_URL = "https://ai.authstar.org/sso/saml2/0oaw3jkwkkaU4KMOa1d7"
MCP_GW_IDP_AUDIENCE_URI = "https://www.okta.com/saml2/service-provider/spbvdqwtzjxebkcedihu"


class SignedSAMLAssertion:
    def __init__(self, idp_certificate, idp_private_key, idp_issuer_uri, idp_acs_url, idp_audience_uri):
        self.idp_certificate = idp_certificate
        self.idp_private_key = idp_private_key
        self.idp_issuer_uri = idp_issuer_uri
        self.idp_acs_url = idp_acs_url
        self.idp_audience_uri = idp_audience_uri

        self.saml_template = (
            '<saml2p:Response Destination="{ACS_URL}" ID="{RESPONSE_ID}" '
            'IssueInstant="{ISSUE_INSTANT}" Version="2.0" xmlns:saml2p="urn:oasis:names:tc:SAML:2.0:protocol">'
            '<saml2:Issuer Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity" '
            'xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion">{ISSUER}</saml2:Issuer>'
            '<saml2p:Status xmlns:saml2p="urn:oasis:names:tc:SAML:2.0:protocol">'
            '<saml2p:StatusCode Value="urn:oasis:names:tc:SAML:2.0:status:Success"/></saml2p:Status>'
            '<saml2:Assertion ID="{ASSERTION_ID}" IssueInstant="{ISSUE_INSTANT}" Version="2.0" '
            'xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion">'
            '<saml2:Issuer Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity">{ISSUER}</saml2:Issuer>'
            '<saml2:Subject><saml2:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">{USER_EMAIL}</saml2:NameID>'
            '<saml2:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">'
            '<saml2:SubjectConfirmationData NotOnOrAfter="{NOT_ON_OR_AFTER}" Recipient="{ACS_URL}"/></saml2:SubjectConfirmation>'
            '</saml2:Subject><saml2:Conditions NotBefore="{NOT_BEFORE}" NotOnOrAfter="{NOT_ON_OR_AFTER}">'
            '<saml2:AudienceRestriction><saml2:Audience>{AUDIENCE}</saml2:Audience></saml2:AudienceRestriction>'
            '</saml2:Conditions><saml2:AuthnStatement AuthnInstant="{AUTH_INSTANT}" SessionIndex="{SESSION_ID}">'
            '<saml2:AuthnContext><saml2:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml2:AuthnContextClassRef>'
            '</saml2:AuthnContext></saml2:AuthnStatement></saml2:Assertion></saml2p:Response>'
        )

    def _generate_saml_id(self):
        return f"id{uuid.uuid4().hex}"

    def _get_iso_timestamp(self, delta_seconds=0):
        dt = datetime.now(timezone.utc) + timedelta(seconds=delta_seconds)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    def generate_signed_saml_assertion(self, email):
        assertion_id = self._generate_saml_id()
        now = self._get_iso_timestamp()

        saml_response = self.saml_template.format(
            ISSUER=self.idp_issuer_uri,
            ACS_URL=self.idp_acs_url,
            AUDIENCE=self.idp_audience_uri,
            USER_EMAIL=email,
            AUTH_INSTANT=now,
            ISSUE_INSTANT=now,
            NOT_BEFORE=self._get_iso_timestamp(-10),
            NOT_ON_OR_AFTER=self._get_iso_timestamp(24 * 60),
            RESPONSE_ID=self._generate_saml_id(),
            ASSERTION_ID=assertion_id,
            SESSION_ID=self._generate_saml_id()
        )

        root = etree.fromstring(saml_response.encode('utf-8'))
        namespaces = {'saml2': 'urn:oasis:names:tc:SAML:2.0:assertion'}
        assertion_node = root.find('.//saml2:Assertion', namespaces=namespaces)

        signer = XMLSigner(
            method=methods.enveloped,
            signature_algorithm="rsa-sha256",
            digest_algorithm="sha256",
            c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"
        )

        signed_assertion_node = signer.sign(
            assertion_node,
            key=self.idp_private_key.encode('utf-8'),
            cert=self.idp_certificate.encode('utf-8'),
            reference_uri=f"#{assertion_id}"
        )

        signed_xml_bytes = etree.tostring(signed_assertion_node, xml_declaration=False, encoding='utf-8')
        signed_b64 = base64.b64encode(signed_xml_bytes).decode('utf-8')

        return signed_b64


def exchange_saml_for_token(saml_assertion, okta_domain, client_id, client_secret):
    url = f"https://{okta_domain}/oauth2/v1/token"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:saml2-bearer',
        'scope': 'openid email profile phone okta.myAccount.phone.manage offline_access',
        'assertion': saml_assertion
    }

    response = requests.post(url, headers=headers, data=payload, auth=(client_id, client_secret))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text, "status_code": response.status_code}


def handler(event, context):
    """Netlify Function handler"""

    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }

    # Only allow POST requests
    if event.get('httpMethod') != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed. Use POST.'})
        }

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')

        if not email:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Email is required'})
            }

        # Initialize SAML Generator
        generator = SignedSAMLAssertion(
            idp_certificate=CERT,
            idp_private_key=KEY,
            idp_issuer_uri=MCP_GW_IDP_ISSUER_URI,
            idp_acs_url=MCP_GW_IDP_ACS_URL,
            idp_audience_uri=MCP_GW_IDP_AUDIENCE_URI
        )

        # Generate signed assertion
        signed_assertion = generator.generate_signed_saml_assertion(email)

        # Exchange for token
        token_response = exchange_saml_for_token(
            saml_assertion=signed_assertion,
            okta_domain=OKTA_DOMAIN,
            client_id=MCP_GW_CLIENT_ID,
            client_secret=MCP_GW_CLIENT_SECRET
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'saml_assertion': signed_assertion,
                'token_response': token_response
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
