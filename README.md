<<<<<<< HEAD
# LinkedIn-Style Job Platform Backend
=======
README here is not for how to execute the project , but it's only the documentation i followed and mark points while i was learning!!🙅‍♂️🙅‍♂️🙅‍♀️🙅‍♀️
>>>>>>> 20223a4e99f38b4e9229ffdac0ecb28d5ae283e0

A backend system for managing users, authentication, and profile-related features in a job platform similar to LinkedIn.

This project focuses on **user management, authentication flows, and API design**, representing a production-style backend for a user-centric application.

---

## 🧠 Overview

This backend provides APIs for:

- user account management
- authentication and authorization
- profile updates
- avatar uploads
- admin-level monitoring

It demonstrates how real-world applications handle **user lifecycle, security, and API design**.

---

## ⚙️ Core Features

### 👤 User Management
- Create, read, update, and delete users
- Fetch current logged-in user (`/users/me`)
- Pagination-ready user listing
- Soft-delete support (optional design)

---

### 🔐 Authentication System
- JWT-based authentication
- Access + refresh token flow
- Secure login/logout system

**Flow:**
1. Login → receive access + refresh tokens  
2. Use access token for API requests  
3. Refresh token when expired  
4. Logout → invalidate session  

---

### 🧾 Signup System
- Dedicated signup endpoint
- Validates user data before creation
- Secure password handling (bcrypt)

---

### 🖼️ Avatar Upload
- Upload profile image
- Attach avatar to user profile
- File handling through API

---

### 🛠️ Admin Features
- Admin dashboard endpoint
- Central monitoring capability
- Foundation for role-based access control

---

## 🏗️ Architecture


Client
↓
FastAPI (API Layer)
↓
Services (Business Logic)
↓
Repositories (Database Layer)
↓
PostgreSQL


---

## 🧰 Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Access + Refresh Tokens)
- **Security**: Password hashing (bcrypt)
- **Validation**: Pydantic
- **Architecture**: Layered (API → Services → Repositories)

---

## 📡 API Endpoints

### Root
- `GET /`

---

### Users

- `GET /users/me` → Get current user  
- `POST /users/` → Create user  
- `GET /users/` → List users  
- `GET /users/{user_id}` → Get user by ID  
- `PUT /users/{user_id}` → Update user  
- `DELETE /users/{user_id}` → Delete user  
- `POST /users/{user_id}/avatar` → Upload avatar  
- `POST /users/signup` → Signup  

---

### Authentication

- `POST /auth/login` → Login  
- `POST /auth/refresh` → Refresh token  
- `POST /auth/logout` → Logout  

---

### Admin

- `GET /admin/dashboard` → Admin dashboard  

---

## 🔐 Authentication Flow


Login → Access Token + Refresh Token

API Requests:
Authorization: Bearer <access_token>

Token Expiry:
Use refresh token → get new access token

Logout:
Invalidate refresh token


---

## 📦 Example Request (Signup)

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}

🧪 Key Concepts Demonstrated
REST API design
JWT authentication (access + refresh tokens)
Secure password handling
Layered backend architecture
Dependency injection (FastAPI Depends)
File upload handling (avatars)
Request/response validation (Pydantic)
Role-based system foundation (admin endpoints)

Run:
uvicorn main:app --reload