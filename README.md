# Software Engineering Project

This repo contains all the files related to the Software Engineering Course - Project in IIT Madras degree in Data Science & Application.

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login (returns JWT token) |

### Inventory Management (`/api/inventory`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/inventory` | List all medicines |
| GET | `/api/inventory/{id}` | Get medicine details |
| POST | `/api/inventory` | Add new medicine (admin/employee) |
| PUT | `/api/inventory/{id}` | Update medicine (admin/employee) |
| DELETE | `/api/inventory/{id}` | Delete medicine (admin only) |

### Orders (`/api/orders`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | List orders |
| GET | `/api/orders/{id}` | Get order details |
| POST | `/api/orders` | Create new order |
| PUT | `/api/orders/{id}` | Update order status |

### Carts (`/api/carts`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/carts` | Get user's cart |
| POST | `/api/carts` | Add item to cart |
| PUT | `/api/carts/{id}` | Update cart item |
| DELETE | `/api/carts/{id}` | Remove cart item |

### Medicine Requests (`/api/medicine-requests`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/medicine-requests` | List requests |
| POST | `/api/medicine-requests` | Submit request |
| PUT | `/api/medicine-requests/{id}` | Approve/reject (admin) |

### Staff Management (`/api/staff`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/staff` | List staff members |
| GET | `/api/staff/{id}` | Get staff details |
| POST | `/api/staff` | Create staff account (admin) |
| PUT | `/api/staff/{id}` | Update staff details |
| DELETE | `/api/staff/{id}` | Deactivate staff (admin) |

### Customers (`/api/customers`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | List customers |
| GET | `/api/customers/{id}` | Get customer details |
| PUT | `/api/customers/{id}` | Update customer |

### Feedback (`/api/feedback`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feedback` | List feedback |
| POST | `/api/feedback` | Submit feedback |

## Setup

Get an API key from Google AI Studio for using AI features.

```bash
cd <PROJECT_NAME>/backend
mv .env.example .env
```

Now, add your keys to the `.env` file.

### Frontend: React App

Make sure `npm` is installed on your system.

```bash
cd <PROJECT_NAME>/frontend
npm install
npm run dev
```

### Backend: FastAPI Server

Make sure `uv` is installed on your system.

```bash
cd <PROJECT_NAME>/backend
uv sync
source .venv/bin/activate
uv run python main.py
```
