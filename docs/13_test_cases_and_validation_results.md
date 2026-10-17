# 13. Test Cases and Validation Results Matrix

## 13.1 Automated Test Execution Summary
- **Test Framework:** `pytest 9.1.1` with Flask Test Client and in-memory SQLite database.
- **Python Version:** 3.13.1 (Windows 64-bit environment).
- **Execution Command:** `pytest`
- **Total Tests Executed:** 34
- **Passed:** 34 (100%)
- **Failed:** 0 (0%)
- **Execution Time:** ~19.7 seconds

---

## 13.2 Traceability & Validation Matrix

| Test ID | Module | Test Scenario Description | Sample Inputs | Expected Outcome | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | `test_auth` | Valid citizen registration | Name: "Rahul", Email: "rahul@test.org", Pass: "Password123" | User created in DB with role 'citizen'; hashed password | User created; password salted & hashed | **PASS** |
| **TC-02** | `test_auth` | Duplicate registration prevention | Email: "citizen@test.org" (already registered) | Rejection with "account already exists" error flash | Duplicate rejected; flash rendered | **PASS** |
| **TC-03** | `test_auth` | Weak password rejection | Password: "pass" (< 8 chars) | Rejection with "at least 8 characters" message | Rejection message displayed | **PASS** |
| **TC-04** | `test_auth` | Mismatched confirmation password | Pass 1: "Pass123", Pass 2: "Diff123" | Rejection with "Passwords do not match" | Rejection message displayed | **PASS** |
| **TC-05** | `test_auth` | Valid Citizen login | `citizen@test.org` / `CitizenSecure123` | Session established; redirect to `/dashboard` | HTTP 200 on `/dashboard` | **PASS** |
| **TC-06** | `test_auth` | Valid Admin login | `admin@test.org` / `AdminSecure123` | Session established; redirect to `/admin/dashboard` | HTTP 200 on `/admin/dashboard` | **PASS** |
| **TC-07** | `test_auth` | Invalid password login | Valid email, wrong password | Rejection with "Invalid email or password" | Rejection message displayed | **PASS** |
| **TC-08** | `test_auth` | Non-existent user login | Unregistered email | Rejection with "Invalid email or password" | Rejection message displayed | **PASS** |
| **TC-09** | `test_auth` | User logout | Active session &rarr; `/auth/logout` | Session cleared; redirect to landing page | Session empty; flash displayed | **PASS** |
| **TC-10** | `test_reports` | Report with valid coordinates | Category: Plastic, Lat: 19.0269, Lng: 72.8373 | Report saved with `has_coordinates == True` | Stored accurately in SQLite | **PASS** |
| **TC-11** | `test_reports` | Report without coordinates | Category: Wet, Lat: None, Lng: None | Handled gracefully; `has_coordinates == False` | Stored; coordinates Null | **PASS** |
| **TC-12** | `test_reports` | Report with valid photo | Valid in-memory PNG stream | Image saved to uploads folder with UUID filename | UUID filename saved | **PASS** |
| **TC-13** | `test_reports` | Unauthenticated report access | Guest navigating to `/report` | Redirect (302) to `/auth/login` | Redirected to login | **PASS** |
| **TC-14** | `test_reports` | Citizen edit pending report | Edit report with status `Reported` | Title and landmark updated successfully | Record updated in DB | **PASS** |
| **TC-15** | `test_reports` | Citizen edit 'In Progress' blocked | Edit report with status `In Progress` | Edit blocked; flash warning displayed | Blocked with warning | **PASS** |
| **TC-16** | `test_reports` | Cross-citizen report edit blocked | Citizen 2 editing Citizen 1's report | HTTP 403 Forbidden | HTTP 403 returned | **PASS** |
| **TC-17** | `test_admin` | Admin dashboard authorization | Admin user accessing `/admin/dashboard` | HTTP 200 with dashboard metrics | HTTP 200 rendered | **PASS** |
| **TC-18** | `test_admin` | Citizen blocked from admin console | Citizen user accessing `/admin/dashboard` | HTTP 403 Forbidden | HTTP 403 rendered | **PASS** |
| **TC-19** | `test_admin` | Guest blocked from admin console | Anonymous user accessing `/admin/dashboard` | Redirect (302) to `/auth/login` | Redirected to login | **PASS** |
| **TC-20** | `test_admin` | Admin status update & audit log | Status changed to `In Progress` + notes | Report status updated; `ActivityLog` created | Status updated; log saved | **PASS** |
| **TC-21** | `test_admin` | Admin report deletion | Delete spam/duplicate report | Report purged; deletion audit log recorded | Report deleted; log saved | **PASS** |
| **TC-22** | `test_admin` | Audit log history access | Admin viewing `/admin/logs` | HTTP 200 with historical log table | HTTP 200 rendered | **PASS** |
| **TC-23** | `test_security`| Invalid category whitelist rejection| Category: "RadioactiveFuel" | Form validation error displayed | Rejection displayed | **PASS** |
| **TC-24** | `test_security`| Short title validation | Title: "Bad" (< 5 chars) | Rejection: "Title must be between 5 and 150" | Rejection displayed | **PASS** |
| **TC-25** | `test_security`| Short description validation | Description: "Too short" (< 10 chars) | Rejection: "Please provide detailed description"| Rejection displayed | **PASS** |
| **TC-26** | `test_security`| Coordinate boundary validation | Latitude: 999.99 (out of range) | Rejection: "Coordinates out of valid bounds" | Rejection displayed | **PASS** |
| **TC-27** | `test_security`| Disallowed file extension | Upload: `exploit.py` | Rejection: "Invalid file type" | Rejection displayed | **PASS** |
| **TC-28** | `test_security`| Corrupted / fake image stream | Upload: Text bytes with `.jpg` extension | Rejection via Pillow binary verification | Corrupted image rejected | **PASS** |
| **TC-29** | `test_security`| Path traversal prevention | GET `/uploads/reports/../../config.py` | HTTP 403 or 404; file not served | Access denied / 404 | **PASS** |
| **TC-30** | `test_security`| API geo-filtering by category | GET `/api/reports?category=Plastic` | Returns only reports matching category Plastic | Filtered JSON payload | **PASS** |
| **TC-31** | `test_db` | User password hashing | Generate hash & verify with Werkzeug | Plaintext not stored; verification accurate | Salted scrypt verified | **PASS** |
| **TC-32** | `test_db` | Role `is_admin` property | `role == 'admin'` vs `role == 'citizen'` | True for admin, False for citizen | Accurately evaluated | **PASS** |
| **TC-33** | `test_db` | Coordinate property logic | Valid vs None vs out-of-range coordinates | `has_coordinates` evaluates correctly | Accurate boolean | **PASS** |
| **TC-34** | `test_db` | Cascade log deletion | Delete parent Report | Child `ActivityLog` deleted via cascade | Log removed cleanly | **PASS** |

