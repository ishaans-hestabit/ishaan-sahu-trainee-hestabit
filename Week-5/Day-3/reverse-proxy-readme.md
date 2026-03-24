# Reverse Proxy & Load Balancing with NGINX (Docker)


This project demonstrates:

- Running **NGINX inside Docker**
- Using it as a **reverse proxy**
- Implementing **round-robin load balancing**
- Running **multiple backend instances**

All services are orchestrated using Docker Compose.

## Architecture Diagram

```mermaid
graph TD
    A[User] --> B[NGINX Reverse Proxy]

    B-->A
    B --> C1[Node Backend 1]
    B --> C2[Node Backend 2]
    C1-->B
    C2-->B
```

## Load Balancing Flow (Round Robin)

```mermaid
sequenceDiagram
    participant User
    participant NGINX
    participant Node1
    participant Node2

    User->>NGINX: Request 1
    NGINX->>Node1: Forward Request
    Node1-->>NGINX: Response
    NGINX-->>User: Response

    User->>NGINX: Request 2
    NGINX->>Node2: Forward Request
    Node2-->>NGINX: Response
    NGINX-->>User: Response

    User->>NGINX: Request 3
    NGINX->>Node1: Forward Request
    Node1-->>NGINX: Response
    NGINX-->>User: Response
```

## Folder Structure

```
.
├── backend
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   └── server.js
├── docker-compose.yml
└── nginx
    └── nginx.conf
```

## Deliverables

- **nginx.conf**
- **reverse-proxy-readme.md**
- **docker-compose.yml**
- **backend/***