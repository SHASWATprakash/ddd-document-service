# 📄 Document Service (DDD Backend)

## 🚀 Overview

This project implements a **Document Management System** supporting invoices and receipts using **Domain Driven Design (DDD)** principles.

---

## 🧱 Architecture

The project follows strict DDD layering:

```
src/
├── document/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── services/
│   │   └── events/
│   ├── use_cases/
│   ├── persistence/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── mappers/
│   └── infrastructure/
│       └── controllers/
```

### Key Design Decisions

* **Entities** → Core business logic (`Document`)
* **Value Objects** → Validation (`DocumentDescription`, `DocumentReference`)
* **Domain Services** → Uniqueness enforcement
* **Factories** → Document creation
* **Repositories** → Data access abstraction
* **Mappers** → Domain ↔ ORM conversion

---

## 📡 API Endpoints

### Create Document

```
POST /documents/
```

### Get Document

```
GET /documents/{reference}/
```

### Add Line Items

```
PUT /documents/{reference}/line-items
```

### Remove Line Items

```
DELETE /documents/{reference}/line-items
```

### Update Document

```
PUT /documents/{reference}/
```

### Delete Document

```
DELETE /documents/{reference}/
```

---

## 📦 Domain Rules

* Reference must be **unique**
* Description ≤ **30 characters**
* Line items cannot exceed limit
* Cannot delete document with items unless `force_delete=true`

---

## 📤 Domain Events & Outbox

* Uses **Transactional Outbox Pattern**
* Events stored in DB and processed asynchronously
* Ensures **at-least-once delivery**
* Integrated with **Celery + Redis**

---

## 🐳 Running the Project

```bash
docker-compose up --build
```

Services:

* Django (8000)
* PostgreSQL
* Redis
* Celery Worker

---

## 🧪 Testing

```bash
pytest
```

Includes:

* Unit tests (domain logic)
* Integration tests (API)
* Edge case validations

---

## ⚙️ Tech Stack

* Django
* Django REST Framework
* PostgreSQL
* Celery + Redis
* Pytest
* Docker

---

## 💡 Assumptions

* Line items tracked as count (not full entity)
* Events are eventually consistent
* No
