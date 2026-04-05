# Backend API Test Suite

Test execution date: April 05, 2026

## Current Status

- Total tests: 97
- Passed: 97
- Failed: 0
- Command used: pytest -q

## Module-Wise Coverage

| Test file | Test count | Endpoint group covered |
| --- | ---: | --- |
| tests/test_auth.py | 10 | Auth register and login |
| tests/test_cart.py | 9 | Cart CRUD |
| tests/test_customers.py | 13 | Customer read and update |
| tests/test_feedback.py | 14 | Feedback create and read |
| tests/test_inventory.py | 11 | Inventory CRUD |
| tests/test_medicine_requests.py | 13 | Medicine request lifecycle |
| tests/test_orders.py | 13 | Order read and update |
| tests/test_staff.py | 14 | Staff CRUD and role checks |

## Required Test Case Format

All test cases follow this format:

[ API being tested, Inputs, Expected output, Actual output, Result ]

## Sample API Test Cases (Execution Snapshot)

| API being tested | Inputs | Expected output | Actual output | Result |
| --- | --- | --- | --- | --- |
| POST /api/auth/register | Valid user payload | 200 with created user object | 200 with id, name, email, role | Success |
| POST /api/auth/register | Duplicate email payload | 400 with duplicate email error | 400 with duplicate email error | Success |
| POST /api/auth/login | Valid credentials | 200 with JWT access_token | 200 with bearer token and user | Success |
| POST /api/auth/login | Invalid password | 400 invalid credentials | 400 invalid credentials | Success |
| GET /api/inventory | Missing bearer token | 401 unauthorized | 401 unauthorized | Success |
| POST /api/inventory | Admin payload with ISO date | 200 and created medicine | 200 and medicine stored | Success |
| POST /api/inventory | Employee token | 403 forbidden | 403 forbidden | Success |
| POST /api/feedback | Customer payload rating 5 | 200 with created feedback | 200 with customer_id and comment | Success |
| POST /api/feedback | Customer payload rating 6 | 422 validation error | 422 validation error | Success |
| POST /api/feedback | Missing comment | 422 validation error | 422 validation error | Success |
| PUT /api/customers/{id} | Customer updates own profile | 200 updated customer object | 200 updated profile | Success |
| PUT /api/customers/{id} | Customer updates other profile | 403 forbidden | 403 forbidden | Success |

## Notes For Reviewers

- The full test implementation is in the files listed above.
- Negative tests include authorization failures, validation failures, and not-found scenarios.
- Integration tests use FastAPI TestClient with an isolated SQLite test database.
