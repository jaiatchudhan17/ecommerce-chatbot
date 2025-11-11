# Genesis E-commerce API

A modern e-commerce platform with AI-powered customer support chatbot, built with FastAPI and SQLite.

## 🚀 Features

- **User Management**: Track users with authentication-ready structure
- **Order Management**: Create and manage customer orders
- **Support Ticketing**: Full-featured support ticket system for order issues
- **AI Chatbot**: Google Gemini-powered customer support bot with RAG capabilities
- **RESTful API**: Well-structured API endpoints with comprehensive documentation
- **Database Integration**: SQLite with SQLModel ORM (easy setup, no server required)
- **Logging**: Comprehensive logging throughout the application
- **Auto-generated API Docs**: Interactive Swagger UI and ReDoc

## � Documentation

- **Main README**: You're reading it! (Quick overview and setup)
- **Complete Chatbot Guide**: [`CHATBOT_GUIDE.md`](CHATBOT_GUIDE.md) - Comprehensive documentation for the AI chatbot
- **API Documentation**: http://localhost:8000/docs (when server running)

## �📋 Requirements

- Python >= 3.12
- Google Gemini API Key (free tier available)
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer (recommended)

## 🛠️ Installation & Setup

### 1. Install uv (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd ecombot

# Create virtual environment and install dependencies with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project dependencies
uv pip install -e .
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
# SQLite database (file-based, no server required)
DATABASE_URL=sqlite:///./ecommerce.db

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your Gemini API key:**
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy it to your `.env` file

**For PostgreSQL (if you prefer):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ecombot_db
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Database Setup

#### Run Migrations

Create the SQLite database and all tables:

```bash
python migrate.py
```

This script will:
- Create a `ecommerce.db` SQLite database file
- Create all required tables (Users, Orders, Tickets)
- Log the migration process

#### Seed Sample Data (Optional)

Populate the database with sample data for testing:

```bash
python seed_data.py
```

This will create:
- 5 sample users
- 10-25 sample orders with various statuses
- Ready for testing the API and chatbot

## 🏃 Running the Application

### Quick Start (First Time Setup)

**Option 1: Automated Setup (Recommended)**
```bash
# 1. Install dependencies
pip install -e .

# 2. Configure environment (edit .env file)
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# 3. Run setup script (creates DB and optionally seeds data)
python setup_db.py

# 4. Start the server
python run.py
```

**Option 2: Manual Setup**
```bash
# 1. Install dependencies
pip install -e .

# 2. Configure environment (edit .env file)
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# 3. Create database and tables
python migrate.py

# 4. Add sample data (optional)
python seed_data.py

# 5. Start the server
python run.py
```

### Development Mode

Start the FastAPI development server with auto-reload:

```bash
python run.py
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Testing the Chatbot

After starting the server, test the AI chatbot:

```bash
# Run the demo script
python test_chatbot.py
```

Or try it manually:
```bash
curl -X POST "http://localhost:8000/v1/support/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your return policy?"}'
```

**For complete chatbot documentation**, see [`CHATBOT_GUIDE.md`](CHATBOT_GUIDE.md)

### Production Mode

For production deployment, run with gunicorn or use uvicorn directly:

```bash
uvicorn genesis_ecommerce.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

### Viewing API Endpoints

FastAPI automatically generates interactive API documentation:

1. **Swagger UI** (Recommended for testing):
   - Navigate to http://localhost:8000/docs
   - Try out endpoints directly in the browser
   - View request/response schemas
   - Test authentication

2. **ReDoc** (Better for reading):
   - Navigate to http://localhost:8000/redoc
   - Clean, searchable documentation
   - Better for sharing with team members

3. **OpenAPI JSON**:
   - Access raw OpenAPI schema at http://localhost:8000/openapi.json

### Available Endpoints

#### Health & Status
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

#### Orders (v1)
- `GET /v1/orders/user/{user_id}` - Fetch all orders for a specific user

#### Support Tickets (v1)
- `POST /v1/support/tickets` - Create a new support ticket
- `GET /v1/support/tickets` - List all tickets (optional status filter)
- `GET /v1/support/tickets/{ticket_id}` - Get specific ticket details
- `GET /v1/support/tickets/order/{order_id}` - Get tickets for an order
- `GET /v1/support/tickets/user/{user_id}` - Get all tickets for a user
- `PATCH /v1/support/tickets/{ticket_id}/status` - Update ticket status

#### AI Customer Support Chatbot (v1)
- `POST /v1/support/chat` - Chat with the AI support bot (general questions)
- `POST /v1/support/chat/order/{order_id}` - Chat about a specific order
- `POST /v1/support/chat/ticket/{ticket_id}` - Chat about a specific ticket

**Chatbot Features:**
- Answers questions about policies, returns, shipping, and support
- Provides real-time order and ticket information
- Uses RAG (Retrieval-Augmented Generation) with support documents
- Maintains conversation context for natural dialogues
- Powered by Google Gemini 1.5 Flash for fast responses

**📖 For complete chatbot documentation, usage examples, and advanced features, see [`CHATBOT_GUIDE.md`](CHATBOT_GUIDE.md)**

## 🔍 Logging

The application uses a centralized logging system configured in `genesis_ecommerce/logger.py`.

### Log Levels
- **INFO**: Normal operations, startup/shutdown events
- **WARNING**: Non-critical issues (e.g., resource not found)
- **ERROR**: Errors that need attention (e.g., database failures)

### Log Format
```
YYYY-MM-DD HH:MM:SS - genesis_ecommerce - LEVEL - message
```

### Examples
```
2025-11-11 10:30:45 - genesis_ecommerce - INFO - Initializing database...
2025-11-11 10:30:45 - genesis_ecommerce - INFO - ✓ Database initialized
2025-11-11 10:31:12 - genesis_ecommerce - INFO - Fetching orders for user_id: 1
2025-11-11 10:31:12 - genesis_ecommerce - INFO - Found 3 orders for user_id: 1
```

### Viewing Logs
Logs are output to stdout and can be:
- Viewed directly in the terminal when running locally
- Redirected to files: `python run.py > app.log 2>&1`
- Sent to logging services in production (e.g., CloudWatch, Datadog)

## 📊 Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `email`: User email address
- `hashed_password`: Password hash
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Orders
- `id`: Primary key
- `user_id`: Foreign key to Users
- `items`: JSON array of ordered items
- `status`: Order status (pending, processing, shipped, delivered, cancelled)
- `created_at`, `updated_at`: Timestamps

### Tickets
- `id`: Primary key
- `order_id`: Foreign key to Orders
- `issue_description`: Problem description
- `status`: Ticket status (open, in_progress, resolved, closed)
- `created_at`, `updated_at`: Timestamps

## 🧪 Development

### Installing Development Dependencies

```bash
# Add development dependencies with uv
uv pip install pytest black ruff mypy

# Or add to pyproject.toml and sync
uv pip sync
```

### Code Quality

The project follows Python best practices:
- Type hints throughout the codebase
- Pydantic models for request/response validation
- Comprehensive error handling
- Consistent logging

### Project Structure

```
ecombot/
├── genesis_ecommerce/
│   ├── app.py              # FastAPI application
│   ├── config.py           # Configuration management
│   ├── logger.py           # Logging configuration
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py # API router registration
│   │       ├── orders.py   # Order endpoints
│   │       └── support.py  # Support ticket & chatbot endpoints
│   ├── customer_support_bot/
│   │   ├── bot.py          # AI chatbot core logic
│   │   ├── documents/      # RAG knowledge base
│   │   │   ├── terms_and_conditions.txt
│   │   │   └── support_guide.txt
│   │   └── README.md       # Chatbot documentation
│   └── db/
│       ├── core.py         # Database engine and session
│       └── schema.py       # SQLModel table definitions
├── migrate.py              # Database migration script
├── seed_data.py           # Sample data seeding
├── setup_db.py            # Automated DB setup
├── run.py                 # Development server runner
├── test_chatbot.py        # Chatbot demo/test script
├── README.md              # Main project README (this file)
├── CHATBOT_GUIDE.md       # Complete chatbot documentation
└── pyproject.toml         # Project dependencies
```

## 🔧 Troubleshooting

### Database Connection Issues
- SQLite database is file-based - no server setup needed!
- Database file `ecommerce.db` is created automatically on first run
- Check DATABASE_URL in `.env` file: `sqlite:///./ecommerce.db`
- For PostgreSQL: Verify server is running and credentials are correct

### Chatbot Issues
- **"GEMINI_API_KEY not found"**: Add your API key to `.env` file
- **"Import google.generativeai could not be resolved"**: Run `pip install google-generativeai`
- **Slow responses**: Normal for AI generation; using fastest model (gemini-1.5-flash)
- **Generic responses**: Provide context with `order_id`, `ticket_id`, or `user_id` parameters

### Migration Errors
- Delete `ecommerce.db` and run `python migrate.py` again
- Check logs for specific error messages
- Verify all models are imported in `migrate.py`

### Import Errors
- Ensure virtual environment is activated
- Run `uv pip install -e .` to install in editable mode
- Check Python version: `python --version` (should be >= 3.12)
