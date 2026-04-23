# Application Architecture


- Loads app in a structured way (no messy `index.js`)
- Supports multiple environments (`.env.local`, `.env.dev`, `.env.prod`)
- Initializes database, middlewares, and routes in order
- Logs everything during startup

---

## Architecture Flow

```mermaid
flowchart LR
    A[Start Server] --> B[Load Config]
    B --> C[Initialize Logger]
    C --> D[Connect Database]
    D --> E[Load Middlewares]
    E --> F[Mount Routes]
    F --> G[Server Ready]
```

---

## Loaders Structure

- `app.js` → main app loader (entry point)
- `db.js` → handles DB connection
- `logger.js` → logging setup (Winston / Pino)

---

## Tasks Performed

- Built modular app loader  
- Added environment-based config system  
- Connected database using separate loader  
- Initialized middlewares in proper order  
- Mounted routes cleanly  
- Added structured startup logs  


---

## Learning Outcomes

- Understood structured app initialization  
- Learned environment-based configuration  
- Built modular and scalable backend setup  
- Learned importance of logging in startup  

---

## Deliverables

```
src/loaders/app.js
src/loaders/db.js
src/utils/logger.js
ARCHITECTURE.md
```
