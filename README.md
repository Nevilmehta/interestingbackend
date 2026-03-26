# LinkedIn-Style Job Platform Backend

A production-style backend system for managing users, authentication, and profile workflows, built with FastAPI and designed with scalability, security, and real-world backend patterns in mind.

---

## 🧠 Overview

This project simulates the backend of a LinkedIn-style platform, focusing on:

- user lifecycle management
- secure authentication and authorization
- scalable API design
- real-world backend concerns like rate limiting, async processing, and file storage

It goes beyond basic CRUD by implementing **production-grade backend features**.

---

## ⚙️ Core Features

### 👤 User Management
- Full CRUD for users
- Fetch current authenticated user (`/users/me`)
- Pagination and filtering for user listing
- Ownership checks (users can only modify their own data)

---

### 🔐 Authentication & Security
- JWT-based authentication (access + refresh tokens)
- Secure password hashing (bcrypt)
- Token refresh mechanism
- Logout with token invalidation
- Role-based access control (RBAC)

---

### 🛡️ Role-Based Access Control (RBAC)
- Role-based permissions (user, admin)
- Protected admin endpoints
- Access control enforced at API/service level

---

### ⚡ Rate Limiting (Custom Logic)
- Redis-backed rate limiting
- User-based rate limiting using JWT identity
- IP-based fallback when unauthenticated
- Prevents abuse and API overuse

---

### 🖼️ File Uploads (S3 Integration)
- Avatar upload system
- Cloud storage using S3-compatible service
- Scalable and production-ready file handling

---

### 🔄 Async Background Tasks
- Celery-based background processing
- Redis as message broker
- Retry support for failed tasks
- Designed for:
  - email sending
  - async processing workflows

---

### 📄 Pagination & Filtering
- Efficient pagination for large datasets
- Query-based filtering
- Optimized API responses

---

### 🔒 Ownership Enforcement
- Users can only update/delete their own data
- Prevents unauthorized access to other users' resources

---

### 🛠️ Admin Features
- Admin dashboard endpoint
- Role-protected access
- Foundation for monitoring and management tools

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


Async Layer:
FastAPI → Redis (Queue) → Celery Worker → Background Tasks

## 🧰 Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Access + Refresh Tokens)
- **Security**: bcrypt password hashing
- **Caching / Rate Limiting**: Redis
- **Async Processing**: Celery
- **File Storage**: AWS S3 (or S3-compatible)
- **Validation**: Pydantic
- **Architecture**: Layered (API → Services → Repositories)

Login → Access Token + Refresh Token

API Request:
Authorization: Bearer <access_token>

Token Expiry:
Use refresh token → generate new access token

Logout:
Invalidate refresh token


---

## 🧪 Key Backend Concepts Demonstrated

- REST API design with FastAPI
- JWT authentication and token lifecycle management
- Role-based access control (RBAC)
- Redis-based rate limiting (user + IP fallback)
- Background job processing using Celery
- Retry-based fault tolerance
- File uploads using cloud storage (S3)
- Pagination and filtering strategies
- Ownership and authorization checks
- Layered backend architecture

---
Run: uvicorn main:app --reload