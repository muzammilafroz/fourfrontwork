# Project Debug Map

Last updated: 2026-04-05

This document is a debugging-first map of the repository.
Use it to quickly locate where behavior lives, where failures usually originate, and where fixes are most likely needed.

## 1) Project Tree (Debug View)

```text
.
├── .gitignore
├── README.md
├── backend
│   ├── .env.example
│   ├── .python-version
│   ├── README.md
│   ├── app
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── llm.py
│   │   ├── models.py
│   │   ├── routes
│   │   │   ├── appointment_routes.py
│   │   │   ├── auth_routes.py
│   │   │   ├── cart_routes.py
│   │   │   ├── customer_routes.py
│   │   │   ├── doctor_routes.py
│   │   │   ├── feedback_routes.py
│   │   │   ├── inventory_routes.py
│   │   │   ├── medicine_request_routes.py
│   │   │   ├── order_routes.py
│   │   │   ├── prescription_routes.py
│   │   │   ├── staff_routes.py
│   │   │   └── user_routes.py
│   │   └── seed.py
│   ├── database.db
│   ├── main.py
│   ├── pyproject.toml
│   ├── tests
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_cart.py
│   │   ├── test_customers.py
│   │   ├── test_feedback.py
│   │   ├── test_inventory.py
│   │   ├── test_medicine_requests.py
│   │   ├── test_orders.py
│   │   └── test_staff.py
│   └── uv.lock
├── docs
│   ├── README.md
│   ├── arch.md
│   ├── data.md
│   ├── flask.md
│   ├── milestones
│   │   ├── milestone-1
│   │   │   ├── interviews
│   │   │   │   ├── business-interview.mp3
│   │   │   │   ├── business-interview.pdf
│   │   │   │   ├── customer-interview-1.mp3
│   │   │   │   ├── customer-interview-2.mp3
│   │   │   │   └── customer-interview-3.mp3
│   │   │   ├── milestone-1.md
│   │   │   └── milestone-1.pdf
│   │   ├── milestone-2
│   │   │   ├── jira.md
│   │   │   └── jira_template.pdf
│   │   └── milestone-3
│   │       └── report.md
│   ├── minutes
│   │   ├── init_project.md
│   │   └── minutes_meeting_template.md
│   ├── notes
│   │   ├── honor_code_template.md
│   │   └── problem_statement.md
│   ├── openapi.yaml
│   └── project_debug_map.md
├── frontend
│   ├── .env.example
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── public
│   │   ├── favicon.ico
│   │   ├── placeholder.svg
│   │   └── robots.txt
│   ├── src
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── components
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   ├── LoadingSkeleton.tsx
│   │   │   ├── NavLink.tsx
│   │   │   ├── RouteGuard.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   ├── ThemeToggle.tsx
│   │   │   └── ui
│   │   │       ├── button.tsx
│   │   │       ├── dialog.tsx
│   │   │       ├── input.tsx
│   │   │       ├── label.tsx
│   │   │       ├── select.tsx
│   │   │       ├── skeleton.tsx
│   │   │       ├── sonner.tsx
│   │   │       ├── switch.tsx
│   │   │       ├── textarea.tsx
│   │   │       ├── toast.tsx
│   │   │       ├── toaster.tsx
│   │   │       └── tooltip.tsx
│   │   ├── hooks
│   │   │   ├── use-mobile.tsx
│   │   │   └── use-toast.ts
│   │   ├── index.css
│   │   ├── lib
│   │   │   └── utils.ts
│   │   ├── main.tsx
│   │   ├── pages
│   │   │   ├── Index.tsx
│   │   │   ├── Landing.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── NotFound.tsx
│   │   │   ├── PrescriptionReader.tsx
│   │   │   ├── Register.tsx
│   │   │   └── customer
│   │   │       ├── AppointmentHistory.tsx
│   │   │       ├── BookAppointment.tsx
│   │   │       └── Doctors.tsx
│   │   └── stores
│   │       ├── authStore.ts
│   │       └── themeStore.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── project_details.pdf
```

## 2) File-by-File Purpose Index

### Root Files

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/.gitignore` | Git ignore patterns. | Explains why some generated files do not appear in commits. |
| `/README.md` | Project-wide setup and run instructions for frontend/backend. | First place to verify expected startup commands and required env setup. |
| `/project_details.pdf` | Project brief/specification artifact. | Useful to confirm expected behavior when code and implementation differ. |

### Backend: Configuration and Entrypoints

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/backend/.env.example` | Template environment variables for backend. | Missing or wrong env values often cause startup/runtime failures. |
| `/backend/.python-version` | Python version pin. | Version mismatch can break dependencies or typing behavior. |
| `/backend/README.md` | API endpoint summary and behavior notes. | Fast way to verify route intent versus actual implementation. |
| `/backend/main.py` | FastAPI app creation, startup hooks, router registration, CORS, OpenAPI YAML route. | Main backend entrypoint for boot and route wiring issues. |
| `/backend/pyproject.toml` | Backend package metadata and dependencies. | Dependency/version conflicts are diagnosed here first. |
| `/backend/uv.lock` | Locked dependency graph for uv-based installs. | Reproducibility source for environment-specific bugs. |
| `/backend/database.db` | SQLite runtime database file. | Useful to inspect seed data/state-related backend bugs. |

### Backend: Core App Layer

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/backend/app/config.py` | Environment/config loading and settings helpers. | Check here when env-based behavior is wrong. |
| `/backend/app/database.py` | SQLModel engine/session setup and table creation helpers. | First stop for DB connection/session errors. |
| `/backend/app/models.py` | SQLModel table models and Pydantic-style schemas. | Data shape bugs and validation errors usually trace here. |
| `/backend/app/crud.py` | Shared CRUD operations against models. | Central place for read/write logic regressions. |
| `/backend/app/auth.py` | Auth utilities (password hashing/JWT/current user helpers). | Authentication failures and token issues originate here. |
| `/backend/app/seed.py` | Initial/seed data population logic. | Startup crashes or invalid default data often originate here. |
| `/backend/app/llm.py` | LangChain + Google GenAI integration logic. | Diagnose AI feature errors, API key issues, and provider call failures. |

### Backend: API Route Modules

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/backend/app/routes/auth_routes.py` | Register/login endpoints and auth workflows. | Debug login/register failures, token responses, and form handling. |
| `/backend/app/routes/user_routes.py` | User-related API endpoints. | Check user profile/account endpoint behavior. |
| `/backend/app/routes/appointment_routes.py` | Appointment scheduling/listing endpoints. | Debug booking conflicts and appointment state issues. |
| `/backend/app/routes/cart_routes.py` | Cart CRUD endpoints. | Fix cart totals, item updates, and cart ownership bugs. |
| `/backend/app/routes/customer_routes.py` | Customer management endpoints. | Diagnose customer lookup/update issues. |
| `/backend/app/routes/doctor_routes.py` | Doctor-related endpoints. | Useful for doctor listing/assignment/lookup failures. |
| `/backend/app/routes/feedback_routes.py` | Feedback submission/listing endpoints. | Check validation and persistence of feedback data. |
| `/backend/app/routes/inventory_routes.py` | Medicine inventory endpoints. | Primary area for stock, SKU, and inventory update bugs. |
| `/backend/app/routes/medicine_request_routes.py` | Medicine request create/review endpoints. | Debug request lifecycle and approval state logic. |
| `/backend/app/routes/order_routes.py` | Order create/list/update endpoints. | Investigate order flow, status transitions, and price bugs. |
| `/backend/app/routes/prescription_routes.py` | Prescription-related endpoints. | Diagnose prescription parse/attach/fetch issues. |
| `/backend/app/routes/staff_routes.py` | Staff management endpoints. | Check role restrictions and staff CRUD behavior. |

### Backend: Test Suite

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/backend/tests/README.md` | Testing conventions/instructions. | Helps align expected test setup before running tests. |
| `/backend/tests/__init__.py` | Test package marker. | Ensures test import/package behavior is stable. |
| `/backend/tests/conftest.py` | Shared pytest fixtures and test setup. | Most test failures rooted in fixture/data setup start here. |
| `/backend/tests/test_auth.py` | Authentication test cases. | Reproduce and verify auth fixes. |
| `/backend/tests/test_cart.py` | Cart behavior tests. | Validate cart logic after changes. |
| `/backend/tests/test_customers.py` | Customer endpoint tests. | Verify customer API contract and regressions. |
| `/backend/tests/test_feedback.py` | Feedback flow tests. | Confirm feedback route behavior. |
| `/backend/tests/test_inventory.py` | Inventory API tests. | Catch stock/inventory regressions quickly. |
| `/backend/tests/test_medicine_requests.py` | Medicine request tests. | Validate request state transition logic. |
| `/backend/tests/test_orders.py` | Order processing tests. | Check order creation and update correctness. |
| `/backend/tests/test_staff.py` | Staff management tests. | Validate role/permission and staff CRUD behavior. |

### Frontend: Build and Tooling

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/.env.example` | Template env vars for frontend runtime/build. | Missing API base URLs and keys usually start here. |
| `/frontend/index.html` | Vite HTML shell and root mount point. | Check root div/script injection issues. |
| `/frontend/package.json` | Scripts, dependencies, and devDependencies. | First place for frontend build/run/package errors. |
| `/frontend/package-lock.json` | npm lockfile for exact package versions. | Reproducibility for environment-specific frontend bugs. |
| `/frontend/postcss.config.js` | PostCSS plugin config (Tailwind/autoprefixer). | CSS pipeline and style generation issues. |
| `/frontend/tailwind.config.ts` | Tailwind theme/content scan configuration. | Missing classes/styles often due to config scan paths. |
| `/frontend/tsconfig.json` | Base TypeScript config. | Type resolution and build mode behavior. |
| `/frontend/tsconfig.app.json` | App-specific TypeScript settings. | React app compile/type behavior tuning. |
| `/frontend/tsconfig.node.json` | Node-side TypeScript config for tooling files. | Vite config/type support and node tooling issues. |
| `/frontend/vite.config.ts` | Vite server/build configuration. | Dev server proxy, alias, and build config debugging. |

### Frontend: Public Assets

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/public/favicon.ico` | Browser tab icon. | Not usually logic-critical; useful for static asset path checks. |
| `/frontend/public/placeholder.svg` | Placeholder image asset. | Helpful when image loading paths fail. |
| `/frontend/public/robots.txt` | Robots directives. | Relevant for indexing/crawling behavior checks. |

### Frontend: App Bootstrap and Global Styles

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/src/main.tsx` | React bootstrap, root render, provider wiring. | Entry point for app startup/render failures. |
| `/frontend/src/App.tsx` | Top-level route composition and app shell logic. | Main navigation/view rendering bugs surface here. |
| `/frontend/src/index.css` | Global CSS and Tailwind layer declarations. | Global style collisions and base theme issues. |
| `/frontend/src/App.css` | App-level styles. | Component/layout visual regressions. |

### Frontend: Shared Components

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/src/components/DashboardLayout.tsx` | Shared dashboard layout wrapper and page structure. | Debug sidebar/header/layout breakage. |
| `/frontend/src/components/EmptyState.tsx` | Empty-state UI component. | Validate no-data UX and conditional rendering paths. |
| `/frontend/src/components/LoadingSkeleton.tsx` | Loading placeholder component. | Check loading-state rendering and perceived latency UX. |
| `/frontend/src/components/NavLink.tsx` | Navigation link abstraction and active-state handling. | Route highlighting/navigation inconsistencies. |
| `/frontend/src/components/RouteGuard.tsx` | Auth/role-based route guard logic. | First stop for unexpected redirects/access denial. |
| `/frontend/src/components/StatusBadge.tsx` | Status label/badge UI for states. | Verify status-to-color/text mapping issues. |
| `/frontend/src/components/ThemeToggle.tsx` | Theme switch control. | Debug theme persistence and mode switching bugs. |

### Frontend: Reusable UI Primitives

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/src/components/ui/button.tsx` | Button primitive wrapper. | Shared button behavior/variant bugs. |
| `/frontend/src/components/ui/dialog.tsx` | Dialog/modal primitive wrapper. | Open/close/focus trap issues. |
| `/frontend/src/components/ui/input.tsx` | Input primitive wrapper. | Form input styling/behavior bugs. |
| `/frontend/src/components/ui/label.tsx` | Label primitive wrapper. | Accessibility and field association issues. |
| `/frontend/src/components/ui/select.tsx` | Select/dropdown primitive wrapper. | Dropdown value/select interaction bugs. |
| `/frontend/src/components/ui/skeleton.tsx` | Skeleton primitive wrapper. | Loading placeholder rendering consistency. |
| `/frontend/src/components/ui/sonner.tsx` | Sonner notification wrapper. | Toast visibility/stacking behavior issues. |
| `/frontend/src/components/ui/switch.tsx` | Toggle switch primitive wrapper. | Boolean setting interaction bugs. |
| `/frontend/src/components/ui/textarea.tsx` | Textarea primitive wrapper. | Multiline input sizing/validation behavior. |
| `/frontend/src/components/ui/toast.tsx` | Toast UI primitive definitions. | Toast styling and lifecycle issues. |
| `/frontend/src/components/ui/toaster.tsx` | Toast container/provider component. | Missing toasts usually traced here/provider wiring. |
| `/frontend/src/components/ui/tooltip.tsx` | Tooltip primitive wrapper. | Hover/focus hint rendering problems. |

### Frontend: Hooks, Utilities, and Stores

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/src/hooks/use-mobile.tsx` | Mobile breakpoint detection hook. | Responsive behavior bugs and conditional layout issues. |
| `/frontend/src/hooks/use-toast.ts` | Toast helper hook/API. | Investigate why notifications are not triggered. |
| `/frontend/src/lib/utils.ts` | Shared utility helpers (class merging, formatting, etc.). | Repeated subtle UI/logic issues can stem from shared helpers. |
| `/frontend/src/stores/authStore.ts` | Global auth state store (likely Zustand). | Login session/state drift and stale token bugs. |
| `/frontend/src/stores/themeStore.ts` | Theme preference state store. | Persistent theme and hydration mismatch issues. |

### Frontend: Pages

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/frontend/src/pages/Landing.tsx` | Public landing page UI and content. | Diagnose first-load/homepage issues. |
| `/frontend/src/pages/Login.tsx` | Login page form and submission logic. | Authentication UX/request issues often originate here. |
| `/frontend/src/pages/Register.tsx` | Registration page form and submit flow. | Debug sign-up validation/API payload mismatch. |
| `/frontend/src/pages/Index.tsx` | Main authenticated/default index page. | Route handoff and dashboard entry issues. |
| `/frontend/src/pages/NotFound.tsx` | 404 fallback page. | Route mismatch and invalid navigation behavior. |
| `/frontend/src/pages/PrescriptionReader.tsx` | Prescription reading/parsing workflow UI. | AI/document parsing UI bugs and request handling. |
| `/frontend/src/pages/customer/AppointmentHistory.tsx` | Customer appointment history view. | Debug historical data fetch and rendering. |
| `/frontend/src/pages/customer/BookAppointment.tsx` | Customer appointment booking flow. | Diagnose booking form, slot logic, API payload issues. |
| `/frontend/src/pages/customer/Doctors.tsx` | Customer doctor listing/selection page. | Debug doctor list loading/filtering/selection behavior. |

### Documentation and Artifacts

| File | What it contains | Why it matters for debugging |
|---|---|---|
| `/docs/README.md` | Docs index/overview. | Navigation point for internal documentation. |
| `/docs/arch.md` | System architecture notes. | Understand design intent before changing internals. |
| `/docs/data.md` | Data model/data flow documentation. | Clarifies expected data relationships and constraints. |
| `/docs/flask.md` | Legacy/prototype framework notes. | Helps identify outdated assumptions vs FastAPI implementation. |
| `/docs/openapi.yaml` | API schema definition in OpenAPI format. | Contract reference for frontend-backend mismatch debugging. |
| `/docs/minutes/init_project.md` | Project kickoff meeting notes. | Provides early scope and requirement context. |
| `/docs/minutes/minutes_meeting_template.md` | Meeting minutes template. | Not runtime-critical; process documentation. |
| `/docs/notes/honor_code_template.md` | Honor code template artifact. | Compliance/process document, not runtime code. |
| `/docs/notes/problem_statement.md` | Problem statement and scope. | Confirms intended features and constraints. |
| `/docs/milestones/milestone-1/milestone-1.md` | Milestone 1 written deliverable. | Requirement traceability when behavior is disputed. |
| `/docs/milestones/milestone-1/milestone-1.pdf` | Milestone 1 PDF artifact. | Fixed-format milestone record. |
| `/docs/milestones/milestone-1/interviews/business-interview.mp3` | Business stakeholder interview audio. | Requirement rationale source. |
| `/docs/milestones/milestone-1/interviews/business-interview.pdf` | Business interview transcript/notes PDF. | Faster textual reference than raw audio. |
| `/docs/milestones/milestone-1/interviews/customer-interview-1.mp3` | Customer interview audio 1. | Requirement context source. |
| `/docs/milestones/milestone-1/interviews/customer-interview-2.mp3` | Customer interview audio 2. | Requirement context source. |
| `/docs/milestones/milestone-1/interviews/customer-interview-3.mp3` | Customer interview audio 3. | Requirement context source. |
| `/docs/milestones/milestone-2/jira.md` | Jira planning notes for milestone 2. | Useful to map issue tickets to implementation areas. |
| `/docs/milestones/milestone-2/jira_template.pdf` | Jira template artifact PDF. | Process artifact, not runtime code. |
| `/docs/milestones/milestone-3/report.md` | Final/report write-up for milestone 3. | Summarizes implementation decisions and outcomes. |

## 3) Quick Debug Hotspots (Where To Fix What)

Use this as a shortcut before deep searching:

| Symptom | Check first | Then check |
|---|---|---|
| Backend does not start | `/backend/pyproject.toml`, `/backend/.env` (from `.env.example`) | `/backend/main.py`, `/backend/app/config.py` |
| Auth fails (register/login/token) | `/backend/app/auth.py`, `/backend/app/routes/auth_routes.py` | `/frontend/src/pages/Login.tsx`, `/frontend/src/stores/authStore.ts` |
| 401/403 on guarded pages | `/frontend/src/components/RouteGuard.tsx` | `/backend/app/routes/*` permission logic |
| DB or model validation errors | `/backend/app/models.py` | `/backend/app/database.py`, `/backend/app/crud.py` |
| Cart/order/inventory mismatches | Corresponding route file in `/backend/app/routes/` | `/backend/app/crud.py`, matching backend test file |
| Toasts or UI alerts missing | `/frontend/src/hooks/use-toast.ts` | `/frontend/src/components/ui/toaster.tsx`, `/frontend/src/components/ui/sonner.tsx` |
| Frontend styling broken | `/frontend/src/index.css`, `/frontend/tailwind.config.ts` | component-level files in `/frontend/src/components/` |
| API payload mismatch between FE and BE | `/docs/openapi.yaml` | FE page file + matching BE route module |

## 4) Practical Debugging Workflow

1. Reproduce issue with exact API route/page and user role.
2. Identify feature area from tree and file index above.
3. Check route/page entry file first, then shared logic (`crud.py`, stores, hooks).
4. Confirm model/schema alignment (`models.py` and `openapi.yaml`).
5. Validate with nearest test module under `/backend/tests/`.

---

If you want, this map can be extended with a "call flow" section for each feature (Auth, Orders, Appointments) showing exact frontend page -> API route -> CRUD/model path.
