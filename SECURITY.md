# Security policy

## Report a vulnerability privately

Email [promisepreston@gmail.com](mailto:promisepreston@gmail.com) with the subject `Security report: <repository name>`. This is the security reporting contact for Preston Core Systems repositories.

Do not disclose vulnerabilities in public issues, pull requests, discussions, or logs. For a public repository that offers GitHub's `Report a vulnerability` button under Security, you may use that private reporting channel instead. If that option is unavailable, use the email address above.

Include the information needed to understand and reproduce the issue safely:

- Repository or application name, affected version or commit, and relevant file or endpoint.
- Expected behavior, observed behavior, prerequisites, and potential security impact.
- Minimal reproduction steps or a proof of concept using accounts and data you control.
- Sanitized logs or screenshots, any suggested mitigation, and a way to contact you for follow-up.

Do not send passwords, API tokens, private keys, recovery codes, customer data, recordings, or other sensitive content. Redact examples and describe the exposure instead. If sensitive evidence is necessary, ask us to arrange an appropriate private transfer first. If a credential you control is exposed, revoke or rotate it promptly and report where it was exposed without including its value.

## Scope and supported revisions

Reports may concern application code, dependencies, infrastructure definitions, CI workflows, or repository access controls. Identify the affected revision even if it is an older release or a pre-release version. We assess the impact and available remediation individually; this policy does not promise maintenance or backports for every historical version.

Ordinary feature requests and non-security bugs belong in the repository's normal issue process. When unsure whether an issue is security-sensitive, use the private reporting address first.

## Safe reporting and follow-up

Use the smallest non-destructive demonstration possible. Do not access another person's data, disrupt services or builds, attempt persistence, or test third-party systems without their permission. This reporting policy does not itself authorize penetration testing or access beyond your existing permissions.

We review reports and coordinate follow-up through the private reporting channel. Acknowledgment and remediation timing depend on the issue and maintainer availability; no fixed response or resolution deadline is guaranteed. Please coordinate public disclosure with us so mitigations can be prepared without exposing users to unnecessary risk.

This policy does not establish a bug bounty or promise compensation. Adding it does not enable a scanner, change repository permissions, or purchase a security service.
