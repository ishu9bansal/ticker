# Ticker

A simple FastAPI backend project for learning Python web development, dependency management with `uv`, and deployment workflows.

## 🚀 Features

- Simple "Hello World" REST API endpoint
- Health check endpoint for monitoring
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

```
ticker/
├── main.py              # FastAPI application with endpoints
├── pyproject.toml       # Project metadata and dependencies
├── .python-version      # Python version specification
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── .venv/              # Virtual environment (auto-created, not in git)
```

## 🌐 API Endpoints

### GET /
Returns a simple "Hello World" message.

**Response:**
```json
{
  "message": "Hello World"
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