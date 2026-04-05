# Finance Dashboard API

## Overview

This project is a backend system for managing financial records. It allows users to store income and expense data, apply filters, and view summary insights. 

The backend is built using FastAPI and PostgreSQL, with support for authentication and role-based access control. It was designed to be simple, efficient, and easy to understand.

---

## Tech Stack

* FastAPI – used to build the API quickly and efficiently
* PostgreSQL – used as the main database
* SQLAlchemy (Async) – for database operations
* Alembic – for database migrations
* JWT Authentication – for secure login

---

## Features

* JWT-based authentication
* Role-based access control (Admin, Analyst, Viewer)
* Create, view, update, and delete financial records
* Filtering records by type, category, and date
* Summary APIs (total, category-wise, monthly)
* Soft delete (records are not permanently removed)
* User management (Admin only)

---

## API Endpoints

### Authentication

* POST /auth/login

### Records

* GET /records
* POST /records
* PATCH /records/{id}
* DELETE /records/{id}

### Summary

* GET /summary
* GET /summary/category
* GET /summary/monthly

### Users

* GET /users
* POST /users
* PATCH /users/{id}

---

## Role Setup

The system uses role-based access control with three roles:

| Role    | Access                                 |
| ------- | -------------------------------------- |
| Admin   | Full access (manage records and users) |
| Analyst | Can view records and summary data      |
| Viewer  | Read-only access                       |

Roles are stored in the database and linked to users using `role_id`.

---

## Example API Response

### Login

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Summary

```json
{
  "total_income": 5000,
  "total_expense": 2000,
  "net_balance": 3000
}
```

---

## Setup Instructions

1. Clone the repository

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file
   ```text
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   ```

4. Run migrations
   ```bash
   alembic upgrade head
   ```

5. Start server
   ```bash
   python -m uvicorn app.main:app --reload
   ```

---

## Screenshots

Screenshots below show API testing using Swagger UI and Postman.

---

### 1. Swagger UI Overview


<img width="1814" height="862" alt="image" src="https://github.com/user-attachments/assets/f327348c-ddbd-47b4-82c6-04eead25675b" />


---

### 2. Login Successful
<img width="979" height="777" alt="image" src="https://github.com/user-attachments/assets/7101eb01-4628-4af6-8dec-f374c5040ca9" />


---

### 3. Get Records

<img width="979" height="721" alt="image" src="https://github.com/user-attachments/assets/a4e8a40b-639e-45d4-a241-eb64396ed1a9" />


---

### 4. Create Record

<img width="979" height="731" alt="image" src="https://github.com/user-attachments/assets/5088fb7b-0484-4b55-9afc-d981f49f3811" />


---


### 6. Delete Record

<img width="979" height="698" alt="image" src="https://github.com/user-attachments/assets/7b0de1ed-7a08-41d9-bd24-255d38f4f010" />



---

## Notes

* The backend uses async database operations for better performance
* Role-based access control is implemented to restrict access based on user permissions
* Soft delete is used to avoid permanent data loss by using an `is_deleted` flag

---

## Conclusion

This project demonstrates backend fundamentals such as authentication, role-based access control, API design, and database handling using FastAPI. 

It is designed as a clean and practical implementation of a financial data management system.
