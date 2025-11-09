# Real-time Async Stack (Demo Project)

This project is a high-performance, real-time polling service built to demonstrate a modern, scalable backend architecture. It serves as a production-ready template for asynchronous Python applications, mirroring the requirements of a high-load environment.

The architecture intentionally separates concerns:
* **API (`app`):** Handles immediate HTTP/WS requests with minimal latency.
* **Worker (`worker`):** Processes data-intensive tasks asynchronously.
* **Databases:** Leverages PostgreSQL for persistence and Redis for caching, messaging, and real-time updates.

---

## 🚀 Tech Stack

This project uses the exact stack required for a modern high-load environment:

* **Backend:** **Python 3.11+** with **FastAPI** for the main API.
* **Databases:**
    * **PostgreSQL:** Main database for persistent data (polls, options).
    * **Redis:** Used for three distinct purposes:
        1.  **Message Broker:** `Redis Streams` for queuing vote events.
        2.  **Real-time Pub/Sub:** `Redis Pub/Sub` to push updates to WebSockets.
        3.  **Cache:** Caching poll results for fast read access.
* **Asynchronous Communication:**
    * **WebSockets:** For real-time updates to connected clients (e.g., live poll results).
    * **gRPC:** For high-performance internal service-to-service communication (admin functions).
* **DevOps:**
    * **Docker** & **Docker Compose:** Fully containerized development and production environment.
    * **Linux:** The base for all containers.
* **Code Quality:**
    * **SOLID & Clean Architecture:** Logic is decoupled into services and repositories.
    * **PEP8 Compliant:** Clean, readable code.
    * **Pytest:** Unit and integration tests for CI/CD.

---

## 🏛️ Architecture Diagram
```
[Client]
   |
(HTTP/WS)
   |
   v
[FastAPI (app)] <----(gRPC)----> [gRPC Server (admin)]
   |
   | 1. (POST /vote)
   v
[Redis (Stream: 'vote_events')]
   |
   | 2. (Worker consumes)
   v
[Worker]
   |
   +---- 3. Update DB ----> [PostgreSQL]
   |
   +---- 4. Update Cache --> [Redis (Cache)]
   |
   +---- 5. Publish Update -> [Redis (Pub/Sub: 'poll_updates')]
                                |
                                | 6. (WS connection listens)
                                v
                           [FastAPI (app)] ---> [Client]
```
---


## 🛠️ How to Run

This project is fully containerized and requires only **Docker** and **Docker Compose** to be installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dreamerScape/realtime-async-stack.git
    cd realtime-async-stack
    ```

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

3.  **That's it!** The services are now running:
    * **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **gRPC Server:** Running internally (check `docker-compose.yml`)

---

## ✅ Testing

The project includes a test suite using `pytest`.

To run the tests (inside the `app` container):

```bash
# Find your 'app' container name
docker ps

# Run pytest inside the container
docker exec -it <app_container_name> pytest
---

