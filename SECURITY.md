# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Implemented Security Controls

EcoTrack incorporates robust security safeguards to ensure safe citizen reporting and administrative integrity:

1. **Password Hashing:**
   - User passwords are automatically salted and hashed using `werkzeug.security` (scrypt / PBKDF2 with SHA-256).
   - Plaintext passwords are never stored in the database or logged in application traces.

2. **Cross-Site Request Forgery (CSRF) Protection:**
   - Every state-modifying form submission (POST) validates a session-bound cryptographic CSRF token.
   - Timing attacks are mitigated using constant-time token comparison (`secrets.compare_digest`).

3. **Safe File Uploads:**
   - Extensions are strictly whitelisted to non-executable image formats: `.png`, `.jpg`, `.jpeg`, `.webp`.
   - Maximum upload payload is capped at 5 MB (`MAX_CONTENT_LENGTH`).
   - Image binary streams are verified using the Python Imaging Library (Pillow) via `Image.verify()` to prevent malicious scripts from executing.
   - Stored filenames are regenerated with UUIDv4 random identifiers to prevent path traversal and arbitrary file overwrite attacks.

4. **Directory Traversal Defense:**
   - File serving endpoints strictly sanitize paths and block `..` sequences, absolute path prefixes, and cross-directory references.

5. **Role-Based Access Control (RBAC):**
   - Administrative endpoints (`/admin/*`) strictly enforce server-side authentication and role checks (`@admin_required`).
   - Access attempts by unauthorized citizens or guests trigger HTTP 403 Forbidden or login redirects.

6. **Error Handling & Traceback Concealment:**
   - Custom HTTP error handlers (400, 403, 404, 500) render friendly user views without exposing internal Python stack traces, database schema details, or environment variables.

---

## Reporting a Vulnerability

If you discover a potential security flaw in EcoTrack:
1. Please **do not** report security vulnerabilities via public GitHub issues.
2. Email a detailed vulnerability advisory to `security@ecotrack.local` or the student project lead.
3. Include steps to reproduce the vulnerability, proof-of-concept payloads, and the affected version.
4. We acknowledge reports within 48 hours and work toward a coordinated fix.

