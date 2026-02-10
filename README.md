# Ishaan Sahu – Hestabit Trainee
 
# Week 1
 
Following are the task advancements for week 1 assigned tasks.
 
---
 
## Day 1: System Reverse Engineering & Node.js Basics
 
 
### Tasks Performed
 
1. **System Health Script (`sysinfo.js`)**
2. **Performance Logging**
3. **Terminal Optimization**
 
### Deliverables
---
 
#### `.bashrc` Alias Configuration
![Bashrc Aliases](https://github.com/ishaans-hestabit/ishaan-sahu-trainee-hestabit/blob/main/Week-1/Day-1/images/Alias%20Screenshot.png)
 

### Learnings

- Got familiar with Node.js system modules and how to extract system-level information.
- Learned how to measure script performance using time and memory metrics.
- Understood how terminal aliases can improve daily development workflow.

---

## Day 2: Node.js CLI & Concurrency

---

### Tasks Performed

- **Built a CLI tool (`stats.js`) for counting lines, words, and characters**
- **Processed multiple files in parallel**
- **Logged execution time and memory usage**
- **Removed duplicate lines and saved output files**

---

### Deliverables

- `stats.js` CLI
- `/logs/performance*.json`
- Output files with uniqueness processing

---

### Learnings

- Learned how to build and run a custom CLI tool using Node.js.
- Understood asynchronous file handling and parallel execution.
- Gained experience in logging performance data and working with output files.

---

## Day 3: Git Mastery (Reset, Revert, Cherry-pick, Stash)

---

### Tasks Performed

1. **Created a repository with multiple commits and intentionally introduced a syntax error.**
2. **Used `git bisect` to trace and identify the commit that caused the issue.**
3. **Created a release branch from an older stable commit.**
4. **Used `git cherry-pick` to move only required changes from `main` to the release branch.**
5. **Used `git stash` while switching branches and restored the changes without conflicts.**

---

### Deliverables

- `bisect-log.txt` – bisect command history and results  
- `cherry-pick-report.md` – details of cherry-picked commits  
- `stash-proof.txt` – stash and restore verification  
- Commit graph screenshot  

---

### Learnings

- Understood how Git tracks commits and how to debug issues using `git bisect`.
- Learned practical usage of cherry-pick for selective commit transfer.
- Got clarity on safely handling uncommitted changes using git stash.

#### `git graph` Git Graph
![Git Graph](https://github.com/ishaans-hestabit/ishaan-sahu-trainee-hestabit/blob/main/Week-1/Day-3/git%20graph/Git%20Graph%20Week-1%20Day-3%20Updated.png)

---

## Day 4: HTTP / API Forensics (cURL & Postman)

---

### Tasks Performed

1. **Used `curl` to fetch GitHub API data and inspected response headers.**
2. **Extracted and logged important headers like rate-limit, ETag, and server details.**
3. **Tested API pagination by navigating through multiple pages of GitHub repositories.**
4. **Documented pagination behavior using Link headers.**
5. **Created a Postman collection to test GitHub user and repository APIs.**
6. **Built a simple HTTP server with endpoints to return timestamps, headers, and an in-memory counter.**

---

### Deliverables

- `curl-headers.txt`
- `pagination-analysis.md`
- Exported Postman collection (`.json`)
- `server.js`

---

### Learnings

- Understood how HTTP headers work and how APIs expose metadata.
- Learned how pagination is handled in REST APIs using Link headers.
- Gained hands-on experience with Postman for API testing.
- Learned how to build basic HTTP endpoints and manage in-memory state.

---

## Day 5: Automation & Mini CI Pipeline

---

### Tasks Performed

1. **Created a health check script (`healthcheck.sh`) to ping the server at regular intervals.**
2. **Logged server failures to `logs/health.log`.**
3. **Set up pre-commit checks using Husky to:**
   - **Ensure `.env` file is not committed**
   - **Ensure JavaScript files are properly formatted**
   - **Ensure log files are ignored**
4. **Created a packaging script to generate timestamp-based zip bundles.**
5. **Generated checksum files to verify package integrity.**
6. **Scheduled the health check script using cron for automated execution.**

---

### Deliverables

- `healthcheck.sh`
- Husky pre-commit hook screenshots (failed & passed)
- `bundle-<timestamp>.zip`
- `checksums.sha1`
- Screenshot of scheduled cron job

---

### Learnings

- Learned how to automate server health monitoring using shell scripts.
- Understood the role of pre-commit hooks in maintaining code quality.
- Gained experience in basic CI-like workflows without external tools.
- Learned how cron jobs help automate recurring system tasks.

#### `Crontab` Crontab
![Crontab]()

#### `Husky Commit Failed` Husky Commit Failed
![Husky Commit Failed]()

#### `Husky Commit Success` Husky Commit Success
![Husky Commit Success]()

---
