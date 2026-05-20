## Create Okta Group

1. Group Name : Allow MCP Gateway, Group Description : Allow access to MCP Gateway application

## Generate Certs

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=bala-secures-ai.oktapreview.com'
```

Note : the -subj value in the openssl command must be your okta domain

## Application Setup : Native App in Okta with SAML 2.0 Assertion Grant Type

| Name                            | value                                                                       |
| :------------------------------ | :-------------------------------------------------------------------------- |
| Sign-in method                  | OIDC                                                                        |
| Application type                | Native                                                                      |
| App Name                        | MCP Gateway                                                                 |
| Grant type                      | [x] Authorization Code </br> [x] Refresh Token </br> [x] SAML 2.0 Assertion |
| Response type                   | Code                                                                        |
| Assignments > Controlled access | Limit access to selected groups </br> [Allow MCP Gateway]                   |
| Authentication policy           | MCP Gateway Policy                                                          |

## SAML 2.0 IDP Setup in Okta

| Name                            | Value                                                                                                |
| :------------------------------ | :--------------------------------------------------------------------------------------------------- |
| Name                            | SAML-Assertion-GrantType                                                                             |
| IdP Usage                       | SSO only                                                                                             |
| IdP username                    | idpuser.subjectNameId                                                                                |
| Match against                   | Okta Username                                                                                        |
| Account Link Policy             | Automatic                                                                                            |
| Auto-Link Restrictions          | None                                                                                                 |
| If no match is found            | Create new user (JIT)                                                                                |
| Profile Source                  | [x] Update attributes for existing users                                                             |
| Reactivation Settings           | [x] Reactivate users who are deactivated in Okta </br> [x] Unsuspend users who are suspended in Okta |
| Group Assignments               | Assign to specific groups                                                                            |
| Specific Groups                 | Allow MCP Gateway                                                                                    |
| IdP Issuer URI                  | https://mcp-gateway.saml-assertion                                                                   |
| IdP Single Sign-On URL          | https://mcp-gateway.saml-assertion/sso/saml                                                          |
| IdP Signature Certificate       | <cert.pem> created in the previous step                                                              |
| Response Signature Verification | Assertion                                                                                            |

## Authorization Server

| Name        | Value                                |
| :---------- | :----------------------------------- |
| Name        | MCP-Gateway                          |
| Audience    | https://mcp-gateway.saml-assertion   |
| Description | Authorization Server for MCP Gateway |

### Access Policy

| Name        | Value                                       |
| :---------- | :------------------------------------------ |
| Name        | MCP Gateway Policy                          |
| Description | MCP Gateway Policy                          |
| Assign to   | The following clients: \n Allow MCP Gateway |

### Access Policy Rule

| Name          | Value                   |
| :------------ | :---------------------- |
| Rule Name     | MCP Gateway Policy Rule |
| Grant type is | SAML 2.0 Assertion      |
