## API Endpoints

The following are some API routes used in our application.

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
