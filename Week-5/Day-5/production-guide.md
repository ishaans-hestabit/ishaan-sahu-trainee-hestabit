# Production Deployment Guide — Full Stack App (Docker + NGINX + HTTPS)



This project demonstrates a **production-style deployment** of a full-stack application using:

- **Frontend** → React 
- **Backend** → Node.js (Express)
- **Database** → MongoDB
- **Reverse Proxy** → NGINX
- **Security** → HTTPS (SSL with mkcert)
- **Orchestration** → Docker Compose (production setup)

---
## Tasks Performed

- Built a **full-stack application deployment** using Docker Compose
- Configured **NGINX as reverse proxy** for routing:
  - `/` → frontend (React)
  - `/api` → backend (Node.js)
- Implemented **HTTPS using self-signed certificates (mkcert)**
- Enforced **HTTP → HTTPS redirection (301)**
- Mounted SSL certificates using **Docker volumes**
- Connected backend to MongoDB using **container networking**
- Created **deployment script** for automated startup
---

## Folder Structure

```
.
├── backend/
├── frontend/
├── nginx/
├── docker-compose.prod.yml
├── deployment-script.sh
├── localhost.pem
├── localhost-key.pem
```

---
## Day-5 Frontend

![Day-5 frontend](../images/Day-5%20Frontend.png)

## Architecture Diagram

```mermaid
sequenceDiagram
    participant User
    participant NGINX as my-nginx
    participant Frontend as my-frontend
    participant Backend as my-backend
    participant DB as my-mongo

    Note over User, NGINX: HTTP → HTTPS Redirect
    User->>NGINX: Request (HTTP :80)
    NGINX-->>User: 301 Redirect to HTTPS

    Note over User, NGINX: HTTPS Connection
    User->>NGINX: Request (HTTPS :443)
    NGINX-->>User: SSL Certificate (localhost.pem)

    Note over User, Frontend: Frontend Request (/)
    User->>NGINX: GET /
    NGINX->>Frontend: proxy_pass http://my-frontend:5173
    Frontend-->>NGINX: HTML / Assets
    NGINX-->>User: Response

    Note over User, DB: API Request (/api)
    User->>NGINX: Request /api
    NGINX->>Backend: proxy_pass http://my-backend:3000/
    Backend->>DB: Query
    DB-->>Backend: Result
    Backend-->>NGINX: JSON
    NGINX-->>User: Response

```
---
## Learning Outcomes (Brief)

- Understood **full-stack deployment** using Docker Compose  
- Learned **NGINX reverse proxy** with path-based routing (`/` and `/api`)  
- Implemented **HTTPS with SSL (mkcert)** and HTTP → HTTPS redirection  
- Built a **production-like architecture** with frontend, backend, and database  
---
## Deliverables

- **Fully working application stack**
- **production-guide.md**
- **backend/\***
- **frontend/\***
- **nginx/\***
- **deployment-script.sh**