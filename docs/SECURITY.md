# 🛡️ Security Policy & Hardening Standards — IRONSTACK

This document outlines the security architecture, hardening measures, and compliance mapping for the **IRONSTACK** framework. As a "Zero-Cloud" on-premise solution, security is integrated into the orchestration logic rather than added as an afterthought.

---

## 🧭 Threat Model & Mitigation

The infrastructure is designed to defend against the following threat vectors:

| Threat Vector | Mitigation Strategy | Implementation |
| :--- | :--- | :--- |
| **Lateral Movement** | Network Segmentation | Services isolated within a dedicated Docker Bridge network. |
| **Config Tampering** | Read-Only Filesystems | Nginx configuration files mounted as `:ro` (Read-Only). |
| **Unauthorized Access** | Service Obfuscation | Database ports are NOT exposed to the host; accessible only via internal bridge. |
| **Deployment Corruption**| Automated Integrity Audit | `infra_manager.py` performs a real SQL handshake before validating the stack. |

---

## 🧱 Hardening Measures

### 1. Network Isolation (Micro-segmentation)
All services communicate through a private internal network (`ironstack_network`). No service is reachable from the outside world except for the **Nginx Ingress Proxy** on port `8080`.

### 2. Ingress Hardening (Nginx GRC)
The Ingress controller is configured with security-focused HTTP headers to mitigate common web attacks:
*   `X-Frame-Options: SAMEORIGIN` (Prevents Clickjacking)
*   `X-Content-Type-Options: nosniff` (Prevents MIME-sniffing)
*   `Strict-Transport-Security` (Ready for SSL/TLS implementation)

### 3. Database Security
*   **Zero-Exposure:** The PostgreSQL engine is bound to the internal container network only.
*   **Persistence:** Data is stored in local encrypted volumes (where host-level encryption is active).
*   **Authentication:** Managed via environment variables, separated from the core logic to prevent credential leakage in logs.

---

## ⚖️ Compliance Mapping (GRC)

This framework aligns with international security standards:

*   **NIST SP 800-53 (AC-3):** Access Enforcement — Enforced through Docker network isolation and proxy-level access control.
*   **NIST SP 800-123:** Guide to General Server Security — Applied through minimal service installation and configuration hardening.
*   **Data Sovereignty:** Designed for compliance with local data protection regulations (GDPR/RDC Law) by ensuring 100% on-premise execution with no external telemetry.

---

## 🔍 Continuous Auditing

Unlike traditional monitoring, IRONSTACK uses a **Deterministic Logic Audit**:
1.  **State Check:** Verifies container health via Docker Socket.
2.  **Functional Check:** Performs an active TCP/SQL handshake.
3.  **Fail-Safe:** The CI/CD pipeline (GitHub Actions) will automatically terminate the deployment if any security or connectivity check fails.

---

## 📩 Vulnerability Disclosure

If you discover a security vulnerability within this framework, please do not open a public issue. Instead, follow the responsible disclosure process:

1.  Send a detailed report to the maintainer via **LinkedIn (Jeanluck NDATO)** or via email.
2.  Provide steps to reproduce the issue.
3.  Acknowledge that this is a hardened project used for professional demonstration purposes.

---
*"Security is not a product, but a process."*
