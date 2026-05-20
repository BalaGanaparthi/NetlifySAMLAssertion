const crypto = require("crypto");
const { v4: uuidv4 } = require("uuid");
const { SignedXml } = require("xml-crypto");
const { DOMParser, XMLSerializer } = require("@xmldom/xmldom");

// Hardcoded Certificates
const CERT = `-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----`;

const KEY = `-----BEGIN PRIVATE KEY-----
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
-----END PRIVATE KEY-----`;

// Configuration
const OKTA_DOMAIN = "bala-secures-ai.oktapreview.com";
const MCP_GW_CLIENT_ID = "0oayvagmqu9IzSUYC1d7";
const MCP_GW_CLIENT_SECRET =
  "nPUn7VhW-6ntXoXbLDn2e5C8AnI9uxNOfDDOYkiqjj76rRuVrzGt1wPTTfdGVCjO";
const MCP_GW_IDP_ISSUER_URI = "https://benefits.streamward.com";
const MCP_GW_IDP_ACS_URL =
  "https://ai.authstar.org/sso/saml2/0oaw3jkwkkaU4KMOa1d7";
const MCP_GW_IDP_AUDIENCE_URI =
  "https://www.okta.com/saml2/service-provider/spbvdqwtzjxebkcedihu";

function generateSamlId() {
  return `id${uuidv4().replace(/-/g, "")}`;
}

function getIsoTimestamp(deltaSeconds = 0) {
  const dt = new Date(Date.now() + deltaSeconds * 1000);
  return dt.toISOString().replace(/\.\d{3}Z$/, "Z");
}

function getCertificateContent(cert) {
  return cert
    .replace(/-----BEGIN CERTIFICATE-----/, "")
    .replace(/-----END CERTIFICATE-----/, "")
    .replace(/\s/g, "");
}

function generateSignedSamlAssertion(email) {
  const assertionId = generateSamlId();
  const responseId = generateSamlId();
  const sessionId = generateSamlId();
  const now = getIsoTimestamp();
  const notBefore = getIsoTimestamp(-10);
  const notOnOrAfter = getIsoTimestamp(24 * 60);

  // Build the Assertion XML
  const assertionXml = `<saml2:Assertion ID="${assertionId}" IssueInstant="${now}" Version="2.0" xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion"><saml2:Issuer Format="urn:oasis:names:tc:SAML:2.0:nameid-format:entity">${MCP_GW_IDP_ISSUER_URI}</saml2:Issuer><saml2:Subject><saml2:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">${email}</saml2:NameID><saml2:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer"><saml2:SubjectConfirmationData NotOnOrAfter="${notOnOrAfter}" Recipient="${MCP_GW_IDP_ACS_URL}"/></saml2:SubjectConfirmation></saml2:Subject><saml2:Conditions NotBefore="${notBefore}" NotOnOrAfter="${notOnOrAfter}"><saml2:AudienceRestriction><saml2:Audience>${MCP_GW_IDP_AUDIENCE_URI}</saml2:Audience></saml2:AudienceRestriction></saml2:Conditions><saml2:AuthnStatement AuthnInstant="${now}" SessionIndex="${sessionId}"><saml2:AuthnContext><saml2:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml2:AuthnContextClassRef></saml2:AuthnContext></saml2:AuthnStatement></saml2:Assertion>`;

  // Parse the assertion
  const doc = new DOMParser().parseFromString(assertionXml, "text/xml");

  // Create the signature
  const sig = new SignedXml();
  sig.signatureAlgorithm = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256";
  sig.canonicalizationAlgorithm = "http://www.w3.org/2001/10/xml-exc-c14n#";

  sig.addReference(
    `//*[@ID='${assertionId}']`,
    [
      "http://www.w3.org/2000/09/xmldsig#enveloped-signature",
      "http://www.w3.org/2001/10/xml-exc-c14n#",
    ],
    "http://www.w3.org/2001/04/xmlenc#sha256",
  );

  sig.signingKey = KEY;

  sig.keyInfoProvider = {
    getKeyInfo: function () {
      return `<X509Data><X509Certificate>${getCertificateContent(CERT)}</X509Certificate></X509Data>`;
    },
  };

  sig.computeSignature(assertionXml, {
    prefix: "ds",
    location: { reference: `//*[@ID='${assertionId}']`, action: "prepend" },
  });

  const signedAssertion = sig.getSignedXml();

  // Base64 encode
  return Buffer.from(signedAssertion, "utf-8").toString("base64");
}

async function exchangeSamlForToken(samlAssertion) {
  const url = `https://${OKTA_DOMAIN}/oauth2/v1/token`;

  const params = new URLSearchParams({
    grant_type: "urn:ietf:params:oauth:grant-type:saml2-bearer",
    scope:
      "openid email profile phone okta.myAccount.phone.manage offline_access",
    assertion: samlAssertion,
  });

  const auth = Buffer.from(
    `${MCP_GW_CLIENT_ID}:${MCP_GW_CLIENT_SECRET}`,
  ).toString("base64");

  const response = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${auth}`,
    },
    body: params.toString(),
  });

  const data = await response.json();

  if (response.ok) {
    return data;
  } else {
    return { error: data, status_code: response.status };
  }
}

exports.handler = async (event, context) => {
  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
      },
      body: "",
    };
  }

  // Only allow POST requests
  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: "Method not allowed. Use POST." }),
    };
  }

  try {
    const body = JSON.parse(event.body || "{}");
    const email = body.email;

    if (!email) {
      return {
        statusCode: 400,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ error: "Email is required" }),
      };
    }

    // Generate signed assertion
    const signedAssertion = generateSignedSamlAssertion(email);

    // Exchange for token
    const tokenResponse = await exchangeSamlForToken(signedAssertion);

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        saml_assertion: signedAssertion,
        token_response: tokenResponse,
      }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: error.message }),
    };
  }
};
