# Public scanner helpers

Public repositories use this hosted-only workflow because private reusable sources
cannot be shared with public callers. This code is authored from public upstream
interfaces and contains no private Core source. Consumers must pin the accepted
public workflow commit. No App or repository visibility change is needed.

GitLeaks 8.30.1 scans current content with redaction. Trivy 0.74.0 scans HIGH and
CRITICAL vulnerabilities, secrets and misconfiguration, excluding unfixed
vulnerabilities. Each release archive has a fixed SHA-256 checksum. Only finding
counts reach job logs. Temporary reports are deleted, and no raw reports or source
snippets are uploaded. Invalid or unavailable scans fail instead of claiming clean.

Both jobs always use GitHub-hosted Ubuntu runners and read-only source permissions.
No secrets or configurable shell inputs are accepted. Forks use the same hosted
route. PR scanner policy edits are refused and require a separate reviewed policy
transition. Application deployment, paid scanning and required statuses are outside
this workflow.

The organization repository validates its candidate through local reusable-workflow
syntax. Its scanner utility dependency is immutable and separately committed.
The six focused tests cover private-value omission, unknown reports, finding exits
and immutable-base policy admission. Actual engines still require source-bound CI.
