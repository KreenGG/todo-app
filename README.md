# Todo App

This is a simple Todo application built with FastAPI. The application provides a RESTful API for managing tasks, allowing you to create, read, update, and delete todo items. Also app have authentication, which used for managing todos by user.

## Features

- Authentication
- Managing todos by RESTful API endpoints
- Swagger documentation

## Requirements

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [GNU Make](https://www.gnu.org/software/make/)


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/KreenGG/todo-app.git
   cd todo-app
   ```
2. Install all required packages in `Requirements` section.

## Running the Application

1. **Start application in Docker Compose using Makefile**

   ```bash
   make app
   ```

2. **Access the API documentation:**

   Open your browser and navigate to `http://127.0.0.1:8000/api/docs` to see the interactive API documentation provided by Swagger UI.


## Dependencies

- **FastAPI:** The web framework for building APIs.
- **Pydantic:** For data validation and settings management using Python type annotations.
- **SQLAlchemy:** The database toolkit and object-relational mapping (ORM) library.
- **PostgreSQL:** The database engine.
- **Dishka:** Dependency Injection framework.
- **PyJWT** Lib which works with JWT tokens.
- **Pytest:** Framework for making tests.
