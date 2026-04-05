# Milestone 3 Report

Team: SE Project Group 65
Date: April 05, 2026
Focus: API Endpoints, Test Cases, and User Testing

## 1. Sprint Scope and User Stories Implemented

Sprint 1 and Sprint 2 focused on building backend APIs for authentication, customer workflows, pharmacy operations, and staff/admin operations.

Implemented user-story areas:

- User registration and login with JWT authentication
- Doctor listing and appointment booking
- Prescription upload and AI-assisted extraction
- Inventory management
- Cart and order workflows
- Medicine request workflow
- Staff and customer management
- Feedback submission and review

## 2. APIs Integrated (External)

The project integrates external API services through library clients:

| Integrated API | Purpose | Integration code |
| --- | --- | --- |
| Google Gemini Developer API | Prescription image understanding and structured extraction | [backend/app/llm.py](../../../backend/app/llm.py) |

Supporting libraries used for auth and API operation:

- python-jose for JWT signing and verification
- FastAPI OAuth2 password flow support

## 3. APIs Created By Dev Team

All API endpoints are implemented in FastAPI route modules and exported in Swagger-compatible YAML.

| Domain | Endpoints created |
| --- | --- |
| Auth | POST /api/auth/register, POST /api/auth/login |
| User session | GET /api/user/me, GET /api/user/logout |
| Prescriptions | POST /api/prescriptions/create, GET /api/prescriptions, GET /api/prescriptions/{prescription_id} |
| Doctors | GET /api/doctors, GET /api/doctors/{doctor_id} |
| Appointments | POST /api/appointments, GET /api/appointments |
| Inventory | GET/POST /api/inventory, GET/PUT/DELETE /api/inventory/{medicine_id} |
| Orders | GET/POST /api/orders, GET/PUT /api/orders/{order_id} |
| Cart | GET/POST /api/cart, GET/PUT/DELETE /api/cart/{cart_item_id} |
| Medicine requests | GET/POST /api/medicine-requests, GET/PUT /api/medicine-requests/{request_id} |
| Staff | GET/POST /api/staff, GET/PUT/DELETE /api/staff/{staff_id} |
| Customers | GET /api/customers, GET/PUT /api/customers/{customer_id} |
| Feedback | GET/POST /api/feedback, GET /api/feedback/{feedback_id} |

## 4. Description of API Endpoints (Problem-Statement Fit)

| Problem requirement | API endpoints serving it |
| --- | --- |
| Secure user onboarding and access control | /api/auth/register, /api/auth/login, /api/user/me |
| Discover doctors and schedule consultation | /api/doctors, /api/appointments |
| Manage medicine catalog and stock | /api/inventory, /api/inventory/{medicine_id} |
| Build cart and place medicine orders | /api/cart, /api/orders |
| Request unavailable medicines | /api/medicine-requests |
| Manage pharmacy staff and customers | /api/staff, /api/customers |
| Collect user satisfaction feedback | /api/feedback |
| Process prescription images | /api/prescriptions/create, /api/prescriptions |

## 5. YAML Submission (Swagger Compatible)

- Submitted API specification file: [docs/openapi.yaml](../../openapi.yaml)
- Compatibility: OpenAPI 3.1.0 and loadable by Swagger tooling
- This file was refreshed from current codebase to match implementation and schema updates.

## 6. API Implementation Code References

| Area | Implementation files |
| --- | --- |
| Application entry and router inclusion | [backend/main.py](../../../backend/main.py) |
| Auth routes | [backend/app/routes/auth_routes.py](../../../backend/app/routes/auth_routes.py) |
| User identity routes | [backend/app/routes/user_routes.py](../../../backend/app/routes/user_routes.py) |
| Prescription routes | [backend/app/routes/prescription_routes.py](../../../backend/app/routes/prescription_routes.py) |
| Doctor routes | [backend/app/routes/doctor_routes.py](../../../backend/app/routes/doctor_routes.py) |
| Appointment routes | [backend/app/routes/appointment_routes.py](../../../backend/app/routes/appointment_routes.py) |
| Inventory routes | [backend/app/routes/inventory_routes.py](../../../backend/app/routes/inventory_routes.py) |
| Order routes | [backend/app/routes/order_routes.py](../../../backend/app/routes/order_routes.py) |
| Cart routes | [backend/app/routes/cart_routes.py](../../../backend/app/routes/cart_routes.py) |
| Medicine request routes | [backend/app/routes/medicine_request_routes.py](../../../backend/app/routes/medicine_request_routes.py) |
| Staff routes | [backend/app/routes/staff_routes.py](../../../backend/app/routes/staff_routes.py) |
| Customer routes | [backend/app/routes/customer_routes.py](../../../backend/app/routes/customer_routes.py) |
| Feedback routes | [backend/app/routes/feedback_routes.py](../../../backend/app/routes/feedback_routes.py) |
| Shared model and validation schemas | [backend/app/models.py](../../../backend/app/models.py) |

## 7. API Test Cases

Test execution command:

python -m pytest -q

Current status:

- Total tests: 97
- Passed: 97
- Failed: 0

Required format used below:

[ API being tested, Inputs, Expected output, Actual Output, Result ]

### 7.1 Extensive Endpoint Test Cases

| API being tested | Inputs | Expected output | Actual output | Result |
| --- | --- | --- | --- | --- |
| POST /api/auth/register | New valid user JSON | 200 and created user | 200 with user id/email/role | Success |
| POST /api/auth/register | Duplicate email JSON | 400 duplicate error | 400 duplicate error | Success |
| POST /api/auth/login | Valid username and password form data | 200 and bearer token | 200 with access_token | Success |
| POST /api/auth/login | Wrong password | 400 invalid credentials | 400 invalid credentials | Success |
| GET /api/user/me | Valid bearer token | 200 current user profile | 200 with authenticated user object | Success |
| GET /api/doctors | Valid auth | 200 doctor list | 200 list returned | Success |
| POST /api/appointments | Customer payload with doctor and slot | 200 created appointment | 200 appointment created | Success |
| GET /api/appointments | Customer token | 200 own appointments | 200 list returned | Success |
| GET /api/inventory | Missing token | 401 unauthorized | 401 unauthorized | Success |
| POST /api/inventory | Admin payload with ISO date | 200 created medicine | 200 and date parsed correctly | Success |
| PUT /api/inventory/{medicine_id} | Admin partial update | 200 updated medicine | 200 updated fields returned | Success |
| DELETE /api/inventory/{medicine_id} | Admin token | 200 with ok true | 200 with ok true | Success |
| GET /api/cart | Customer token | 200 cart list | 200 list returned | Success |
| POST /api/cart | Customer adds item | 200 cart item | 200 cart item returned | Success |
| GET /api/orders | Admin token | 200 orders list | 200 list returned | Success |
| POST /api/orders | Customer payload | 200 order created | 200 order with customer binding | Success |
| PUT /api/orders/{order_id} | Employee/admin update | 200 order updated | 200 order status updated | Success |
| GET /api/medicine-requests | Valid token | 200 request list | 200 list returned | Success |
| PUT /api/medicine-requests/{request_id} | Employee/admin status update | 200 updated request | 200 with updated status | Success |
| GET /api/staff | Admin token | 200 staff list | 200 list returned | Success |
| POST /api/staff | Admin creates employee | 200 staff created | 200 with new staff data | Success |
| GET /api/customers | Admin/employee token | 200 customers list | 200 list returned | Success |
| PUT /api/customers/{customer_id} | Customer updates own profile | 200 updated customer | 200 updated profile | Success |
| POST /api/feedback | Customer rating 1..5 and comment | 200 feedback created | 200 feedback returned | Success |
| POST /api/feedback | Invalid rating or missing comment | 422 validation error | 422 validation error | Success |

### 7.2 Demonstrated Mismatch Case (Testing Drives Improvement)

| API being tested | Inputs | Expected output | Actual output | Result |
| --- | --- | --- | --- | --- |
| POST /api/prescriptions/create | Valid image payload but missing GOOGLE_API_KEY | 201 with extracted prescription | 500 AI extraction failed | Fail |

Action taken:

- Kept endpoint behavior explicit and documented dependency on Gemini API key.
- This case is retained to demonstrate practical environment-sensitive failures.

## 8. Sprint 1 Deliverables Check

| Deliverable | Status | Evidence |
| --- | --- | --- |
| Swagger-compatible YAML documentation | Completed | [docs/openapi.yaml](../../openapi.yaml) |
| Proper API test cases | Completed | [backend/tests](../../../backend/tests) |
| Input, expected, actual output in test documentation | Completed | Section 7 tables in this report and [backend/tests/README.md](../../../backend/tests/README.md) |
| Pytest submission for API suite | Completed | [backend/tests](../../../backend/tests) with 97 passing tests |
| Show expected vs actual mismatch scenario | Completed | Section 7.2 |

## 9. Are All APIs Made and Used?

### APIs made

- Yes. All endpoints listed in Section 3 are implemented and present in [docs/openapi.yaml](../../openapi.yaml).

### APIs used

- Used directly by frontend now: auth, doctors, appointments, prescriptions.
- Remaining APIs are implemented and verified through automated tests, but some are not yet connected to visible frontend flows.

Conclusion:

- API implementation is complete for planned backend scope.
- Frontend integration for inventory, orders, cart, feedback, staff, and customer-admin workflows is partially pending and can be expanded in next sprint.

## 10. End User Feedback and Next Sprint Plan

User testing summary from feature demos:

- Users liked fast login and clear doctor listing.
- Users requested better feedback for failed prescription extraction.
- Admin-oriented workflows are available in API but need richer frontend screens.

Next sprint plan:

1. Add frontend screens for inventory, orders, and medicine requests.
2. Add clearer UI error states for prescription AI failures.
3. Add API key health check endpoint for environment readiness.
4. Add pagination and filtering for list endpoints.
5. Add end-to-end tests across frontend and backend.
