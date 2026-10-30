# Security Policy

## 🔒 Security & Privacy Overview

`haunted-shell` operates directly alongside the user's terminal environment. Because terminals handle sensitive credentials (SSH keys, AWS/cloud tokens, environment variables, and proprietary codebases), security and privacy are fundamental architectural priorities.

### 🛡️ Core Guarantees:
1. **Zero External Telemetry:** Under no circumstances does `haunted-shell` transmit commands, outputs, or metadata to external servers. All AI inference is either conducted via local open-weight models (e.g. Google Gemma 2 on localhost) or via the built-in offline rule/Markov spectral engine.
2. **Air-Gap Verification:** Users can audit the air-gap isolation at any time by running `haunt airgap`.
3. **No Credential Logging:** `haunted-shell` does not persist command history or logs to remote disks or telemetry sinks.

---

## 📋 Supported Versions

We provide security updates and patches for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability or privacy leak in `haunted-shell`:

1. **Do not create a public GitHub issue.**
2. Send an email to the maintainers at `swagatsouravdhar@users.noreply.github.com` or submit a private security advisory directly on GitHub via [Security Advisories](https://github.com/SWAGAT10241/haunted-shell/security/advisories/new).
3. Please include:
   - A description of the issue.
   - Steps to reproduce or a minimal proof of concept.
   - The impact on host system isolation or credential security.

### Response Timeline
- **Initial Response:** Within 48 hours.
- **Triage & Assessment:** Within 5 business days.
- **Fix & Public Advisory:** Coordinated release once patched.

---

## 🔍 Automated Security Scanning

This repository implements the following automated security controls:
- **GitHub CodeQL Analysis:** Static application security testing (SAST) on all pull requests and pushes to `main`.
- **pip-audit:** Scans third-party dependencies for known CVEs.
- **Secret Scanning:** Scans commits for accidentally leaked tokens or keys.
