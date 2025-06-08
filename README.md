# Employee Management Application

This project is a full-featured Employee Management System built with Django.  
It includes authentication, CRUD operations, advanced filtering, and a RESTful API for managing Employee, Position, Department, and Status.  
It supports multiple environments: development, production, and testing.

## Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/Thitatpon-Niwatwong/employee_management.git
```
---
### 2. Copy the appropriate `.env` file:

   - For production:
     ```bash
     cp .env.example .env.prod
     ```
   - For development:
     ```bash
     cp .env.example .env.dev
     ```
   - For test:
     ```bash
     cp .env.example .env.test
     ```
---
### 3. Set the `ENVIRONMENT` variable in the `.env.*` file:
---
### 4. Running with Docker Compose
   - For production:
     ```bash
     docker-compose -f docker-compose.prod.yml up -d --build
     ```
   - For development:
     ```bash
     docker-compose -f docker-compose.dev.yml up -d --build
     ```
   - For test:
     ```bash
     docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
     ```
---

