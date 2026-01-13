# Ticker

A simple FastAPI backend project for learning Python web development, dependency management with `uv`, and deployment workflows.

## 🚀 Features

- Simple "Hello World" REST API endpoint
- Health check endpoint for monitoring
- **Organized multi-file project structure** with proper Python packaging
- **Clear import patterns** that work both locally and in production
- Modern Python dependency management with `uv`
- Ready for deployment on Render

## 📋 Prerequisites

- Python 3.12 or higher
- `uv` package manager (installation instructions below)

## 🛠️ Setup and Installation

### 1. Install uv

If you don't have `uv` installed, install it using pip:

```bash
pip install uv
```

Or using the official installer (Unix/macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the Repository

```bash
git clone https://github.com/ishu9bansal/ticker.git
cd ticker
```

### 3. Install Dependencies

`uv` will automatically create a virtual environment and install all dependencies:

```bash
uv sync
```

This command:
- Creates a `.venv` directory with a virtual environment
- Installs all dependencies listed in `pyproject.toml`
- Generates a `uv.lock` file for reproducible builds

## 🏃 Running Locally

### Option 1: Using uv run (Recommended)

```bash
uv run uvicorn main:app --reload
```

### Option 2: Activating the virtual environment

```bash
# On Unix/macOS
source .venv/bin/activate

# On Windows
.venv\Scripts\activate

# Then run the server
uvicorn main:app --reload
```

The API will be available at:
- Main endpoint: http://localhost:8000
- Health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## 📦 Adding New Dependencies

To add a new dependency to your project:

```bash
uv add <package-name>
```

For example:
```bash
uv add requests
uv add sqlalchemy
```

To add development dependencies:

```bash
uv add --dev pytest
uv add --dev black
```

To remove a dependency:

```bash
uv remove <package-name>
```

## 🔍 Project Structure

This project follows a well-organized structure that scales as your application grows:

```
ticker/
├── main.py                      # Entry point - imports app from app.main
├── app/                         # Main application package
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # FastAPI app instance and router configuration
│   ├── api/                    # API route handlers (organized by domain)
│   │   ├── __init__.py
│   │   ├── health.py          # Health check endpoints
│   │   └── ticker.py          # Ticker-related endpoints
│   ├── models/                 # Pydantic models for data validation
│   │   ├── __init__.py
│   │   ├── health.py          # Health check models
│   │   └── ticker.py          # Ticker data models
│   └── services/               # Business logic layer
│       ├── __init__.py
│       └── ticker_service.py  # Ticker business logic
├── pyproject.toml              # Project metadata and dependencies
├── .python-version             # Python version specification
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── .venv/                      # Virtual environment (auto-created, not in git)
```

### Why This Structure?

1. **Separation of Concerns**: Routes (API), models (data), and services (logic) are separated
2. **Scalability**: Easy to add new endpoints, models, or services
3. **Maintainability**: Related code is grouped together
4. **Testability**: Each module can be tested independently

## 🔌 How Imports Work

### Understanding Python Imports in This Project

The key to making imports work both locally and in production is to:
1. **Always run from the project root** (where `main.py` is located)
2. **Use absolute imports** from the `app` package

### Import Patterns

**✅ Correct - Absolute imports (recommended):**
```python
# In any file under app/
from app.models.ticker import TickerResponse
from app.services.ticker_service import TickerService
from app.api import health, ticker
```

**❌ Incorrect - Relative imports (avoid for this structure):**
```python
# Don't use these
from ..models.ticker import TickerResponse  # Can cause issues
from .ticker_service import TickerService    # Can fail in production
```

### Entry Point Explained

**`main.py`** (in project root) is the entry point:
```python
from app.main import app  # Import the FastAPI app instance
```

**`app/main.py`** contains the actual FastAPI app:
```python
from fastapi import FastAPI
from app.api import health, ticker  # Absolute imports

app = FastAPI(title="Ticker API", version="0.1.0")
app.include_router(health.router, tags=["health"])
app.include_router(ticker.router, tags=["ticker"])
```

### Why This Works

When you run `uvicorn main:app`:
1. Python looks for `main.py` in the current directory
2. It imports the `app` variable from that file
3. The `app` variable is imported from `app.main`
4. All imports in `app/main.py` use `app.` prefix, which Python can resolve because the project root is in `sys.path`

### Common Import Issues and Solutions

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Always run commands from the project root (where `main.py` is):
```bash
# ✅ Correct - from project root
cd /path/to/ticker
uv run uvicorn main:app --reload

# ❌ Wrong - from inside app/
cd /path/to/ticker/app
uv run uvicorn main:app --reload  # This will fail!
```

**Problem**: Imports work locally but fail in production

**Solution**: 
- Use absolute imports (`from app.xxx import yyy`)
- Ensure your start command runs from the project root
- The deployment command should be: `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🌐 API Endpoints

### GET /
Returns a simple "Hello World" message with version.

**Response:**
```json
{
  "message": "Hello World",
  "version": "0.1.0"
}
```

### GET /health
Health check endpoint for monitoring service status.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET /ticker
Example ticker endpoint demonstrating service layer pattern.

**Response:**
```json
{
  "symbol": "DEMO",
  "price": 100.50,
  "message": "This is example ticker data"
}
```

**Interactive Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📝 Adding New Endpoints

To add a new endpoint to your application:

1. **Create a model** (if needed) in `app/models/`:
```python
# app/models/user.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```

2. **Create a service** (if needed) in `app/services/`:
```python
# app/services/user_service.py
from app.models.user import User

class UserService:
    def get_user(self, user_id: int) -> User:
        # Your business logic here
        return User(id=user_id, name="John Doe", email="john@example.com")
```

3. **Create an API router** in `app/api/`:
```python
# app/api/users.py
from fastapi import APIRouter
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return user_service.get_user(user_id)
```

4. **Register the router** in `app/main.py`:
```python
from app.api import health, ticker, users  # Add your new module

app.include_router(users.router, tags=["users"])  # Register the router
```

5. **Test it**:
```bash
uv run uvicorn main:app --reload
curl http://localhost:8000/users/1
```

This pattern keeps your code organized and scalable!

## 🚢 Deployment on Render

### Quick Deploy Steps

1. **Push your code to GitHub** (if not already done)

2. **Sign up/Login to Render**
   - Go to [https://render.com](https://render.com)
   - Sign up or login with your GitHub account

3. **Create a New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

4. **Configure the Service**
   - **Name:** `ticker` (or your preferred name)
   - **Region:** Choose the closest to your users
   - **Branch:** `main` (or your default branch)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install uv && uv sync`
   - **Start Command:** `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Advanced Settings (Optional)**
   - **Environment Variables:** Add any required environment variables
   - **Auto-Deploy:** Enable to automatically deploy on git push

6. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application
   - You'll get a URL like `https://ticker-xxxx.onrender.com`

### Environment Variables (if needed)

In Render dashboard, you can add environment variables:
- Click on your service
- Go to "Environment" tab
- Add key-value pairs

Example:
```
ENVIRONMENT=production
LOG_LEVEL=info
```

### Verifying Deployment

Once deployed, test your endpoints:
- Main endpoint: `https://your-app.onrender.com/`
- Health check: `https://your-app.onrender.com/health`
- API docs: `https://your-app.onrender.com/docs`

## 🔧 Development Tips

### Running with auto-reload

The `--reload` flag automatically restarts the server when code changes:

```bash
uv run uvicorn main:app --reload
```

### Custom host and port

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8080
```

### Viewing installed packages

```bash
uv pip list
```

### Updating dependencies

```bash
uv sync --upgrade
```

## 🧪 Testing the API

Using curl:
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

Using Python requests:
```python
import requests

response = requests.get("http://localhost:8000/")
print(response.json())
```

## 📝 Why uv?

`uv` is a modern, fast Python package manager that offers:

- **Speed:** 10-100x faster than pip
- **Reliability:** Resolves dependencies correctly
- **Simplicity:** Single tool for all dependency management
- **Reproducibility:** Lock files ensure consistent installs
- **Modern:** Built with modern Python best practices

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve this project.

## 📄 License

This project is open source and available for learning purposes.