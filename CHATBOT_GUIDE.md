# Genesis E-commerce AI Customer Support Chatbot

**A complete AI-powered customer support chatbot with RAG capabilities for e-commerce platforms**

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [What Was Built](#what-was-built)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [Security & Best Practices](#security--best-practices)
- [Next Steps](#next-steps)

---

## Overview

This is a production-ready AI chatbot for Genesis E-commerce that combines:
- **Google Gemini 1.5 Flash** for fast, intelligent natural language responses
- **RAG (Retrieval-Augmented Generation)** with comprehensive policy documents
- **Real-time database integration** for order and ticket information
- **Context-aware conversations** with history tracking
- **RESTful API** endpoints for easy integration

**Status**: ✅ Complete and Ready to Use

---

## Features

✅ **AI-Powered Responses** - Uses Google Gemini 1.5 Flash for intelligent, natural language understanding  
✅ **RAG-Based Knowledge** - Retrieves information from Terms & Conditions and Support Guide  
✅ **Database Integration** - Real-time access to orders, tickets, and user data  
✅ **Context-Aware** - Remembers conversation history for coherent dialogues  
✅ **Multi-Context Support** - Handles order_id, ticket_id, and user_id contexts  
✅ **Comprehensive Knowledge** - Policies, shipping, returns, support procedures  
✅ **Fast Responses** - Optimized with Gemini Flash model  
✅ **Easy Integration** - RESTful API endpoints with full documentation  
✅ **SQLite Database** - No server setup required, file-based storage

---

## What Was Built

### 1. Core Chatbot Module
**File**: `genesis_ecommerce/customer_support_bot/bot.py`

- RAG-based AI using Google Gemini 1.5 Flash
- Automatic document loading from knowledge base
- Database context fetching (orders, tickets, user data)
- Conversation history management
- Multi-context support (order_id, ticket_id, user_id)

### 2. Knowledge Base Documents

**Terms and Conditions** (`documents/terms_and_conditions.txt`)
- 16 comprehensive sections
- Order processing policies
- Payment and shipping terms
- Returns and refunds policy
- Customer rights and limitations
- Privacy and data protection

**Support Guide** (`documents/support_guide.txt`)
- Order management and tracking
- Return process (step-by-step)
- Shipping options and costs
- Payment troubleshooting
- Account management
- Technical support
- Comprehensive FAQ

### 3. API Endpoints
**File**: `genesis_ecommerce/api/v1/support.py`

Three chat endpoints added:

1. **General Chat** - `POST /v1/support/chat`
2. **Order Chat** - `POST /v1/support/chat/order/{order_id}`
3. **Ticket Chat** - `POST /v1/support/chat/ticket/{ticket_id}`

### 4. Configuration & Dependencies

- Added `gemini_api_key` to `config.py`
- Added `google-generativeai` to dependencies
- Updated `.env.example` with API key template
- SQLite database configuration

### 5. Documentation & Testing

- Complete chatbot README (`customer_support_bot/README.md`)
- Demo/test script (`test_chatbot.py`)
- Setup automation script (`setup_db.py`)
- Updated main README with chatbot info
- This comprehensive guide

---

## Quick Start

### Installation (5 minutes)

#### Step 1: Install Dependencies
```bash
pip install -e .
```

This installs:
- `google-generativeai` - For Gemini AI
- `fastapi`, `sqlmodel`, `uvicorn` - Core framework
- All other dependencies

#### Step 2: Get Your Gemini API Key

1. Visit: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (it's free!)

#### Step 3: Configure Environment

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` and add your key:
```env
DATABASE_URL=sqlite:///./ecommerce.db
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Note:** SQLite is file-based and requires no server setup!

#### Step 4: Initialize Database

**Option 1: Automated (Recommended)**
```bash
python setup_db.py
```

**Option 2: Manual**
```bash
python migrate.py        # Create database and tables
python seed_data.py      # Add sample data (optional)
```

#### Step 5: Start the Server
```bash
python run.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**That's it!** 🎉 Your chatbot is running at http://localhost:8000

---

## How It Works

### RAG (Retrieval-Augmented Generation) Flow

```
┌─────────────────────┐
│   User Question     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Load Support Documents             │
│  - Terms & Conditions               │
│  - Support Guide                    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Fetch Database Context (optional)  │
│  - Order details                    │
│  - Ticket information               │
│  - User order history               │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Build Comprehensive Prompt         │
│  System + Context + History + Q     │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Send to Google Gemini API          │
│  (gemini-1.5-flash)                 │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  Return AI-Generated Response       │
└─────────────────────────────────────┘
```

### Example Scenario

**User Question**: "What's the status of my order?" (with `order_id=123`)

**System Process**:
1. Loads Terms & Support Guide text
2. Queries SQLite database for Order #123 details
3. Builds prompt with:
   - System instructions (how to be a helpful support agent)
   - Support documents (Terms & Guide)
   - Order details (ID, status, items, dates)
   - User's question
4. Sends to Gemini API
5. Returns: "Your order #123 is currently SHIPPED. It contains 3 items (Laptop, Mouse, Keyboard) and was created on Nov 8, 2025..."

---

## API Reference

### 1. General Chat (Most Flexible)

**Endpoint**: `POST /v1/support/chat`

**Request Body**:
```json
{
  "message": "Your question here",
  "order_id": 123,           // Optional: adds order context
  "ticket_id": 456,          // Optional: adds ticket context
  "user_id": 789,            // Optional: adds user's orders
  "conversation_history": [  // Optional: for multi-turn chat
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response**:
```json
{
  "response": "AI-generated answer to your question..."
}
```

**Use Cases**:
- General policy questions
- Questions about specific orders
- Questions about tickets
- Multi-turn conversations

### 2. Order Chat (Convenience Endpoint)

**Endpoint**: `POST /v1/support/chat/order/{order_id}?message=your_question`

**Parameters**:
- `order_id` (path): Order ID to discuss
- `message` (query): Your question about the order

**Example**:
```bash
POST /v1/support/chat/order/123?message=Where%20is%20my%20order?
```

**Use Cases**:
- Quick order status checks
- Order-specific questions
- Simpler than general endpoint

### 3. Ticket Chat (Convenience Endpoint)

**Endpoint**: `POST /v1/support/chat/ticket/{ticket_id}?message=your_question`

**Parameters**:
- `ticket_id` (path): Ticket ID to discuss
- `message` (query): Your question about the ticket

**Use Cases**:
- Ticket status inquiries
- Issue resolution updates

---

## Usage Examples

### Python Examples

#### Basic Question
```python
import requests

response = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={"message": "What is your return policy?"}
)

print(response.json()["response"])
```

#### Order-Specific Query
```python
response = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "What's the status of my order?",
        "order_id": 123
    }
)

print(response.json()["response"])
```

#### Multi-Turn Conversation
```python
# First question
resp1 = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={"message": "Can I return a product?"}
)

# Follow-up with context
resp2 = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "How long do I have?",
        "conversation_history": [
            {"role": "user", "content": "Can I return a product?"},
            {"role": "assistant", "content": resp1.json()["response"]}
        ]
    }
)

print(resp2.json()["response"])
```

#### User's Order History
```python
response = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "Show me all my orders",
        "user_id": 1
    }
)

print(response.json()["response"])
```

#### Using Convenience Endpoints
```python
# Order chat
response = requests.post(
    "http://localhost:8000/v1/support/chat/order/123",
    params={"message": "Where is my order?"}
)

# Ticket chat
response = requests.post(
    "http://localhost:8000/v1/support/chat/ticket/456",
    params={"message": "What's the status of my issue?"}
)
```

### cURL Examples

#### General Chat
```bash
curl -X POST "http://localhost:8000/v1/support/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your return policy?"}'
```

#### Order-Specific Chat
```bash
curl -X POST "http://localhost:8000/v1/support/chat/order/123?message=Where%20is%20my%20order?" \
  -H "Content-Type: application/json"
```

#### With Context
```bash
curl -X POST "http://localhost:8000/v1/support/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my order status?",
    "order_id": 123,
    "user_id": 1
  }'
```

---

## Testing

### Option 1: Run Demo Script (Recommended)
```bash
python test_chatbot.py
```

This will automatically run through multiple scenarios:
- General policy questions
- Order-specific queries
- User order history
- Multi-turn conversations

### Option 2: Interactive API Docs
Open in browser: **http://localhost:8000/docs**

1. Navigate to `POST /v1/support/chat`
2. Click "Try it out"
3. Enter your test data
4. Click "Execute"
5. See the response

### Option 3: Manual Testing
Use the cURL or Python examples above with your own questions.

### Example Questions to Try

**Policy Questions**:
- "What is your return policy?"
- "How long does shipping take?"
- "What payment methods do you accept?"
- "Can I cancel my order?"
- "Do you offer free shipping?"

**Order Questions** (with `order_id`):
- "What's the status of my order?"
- "Where is my order?"
- "When will my order arrive?"
- "What items are in my order?"

**User Questions** (with `user_id`):
- "Show me all my orders"
- "What orders do I have?"
- "What's my order history?"

**Support Questions**:
- "How do I return an item?"
- "How do I track my package?"
- "How do I contact support?"
- "What are your business hours?"

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Server                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │     API Endpoints (/v1/support/chat)              │  │
│  └─────────────────────┬─────────────────────────────┘  │
│                        │                                 │
│  ┌─────────────────────▼─────────────────────────────┐  │
│  │         CustomerSupportBot (bot.py)               │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  RAG Document Loader                        │  │  │
│  │  │  - terms_and_conditions.txt                 │  │  │
│  │  │  - support_guide.txt                        │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Database Context Fetcher                   │  │  │
│  │  │  - Orders (SQLite)                          │  │  │
│  │  │  - Tickets (SQLite)                         │  │  │
│  │  │  - User data (SQLite)                       │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Prompt Builder                             │  │  │
│  │  │  - System instructions                      │  │  │
│  │  │  - Context + Documents                      │  │  │
│  │  │  - Conversation history                     │  │  │
│  │  │  - User message                             │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └─────────────────────┬─────────────────────────────┘  │
└────────────────────────┼─────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Google Gemini API   │
              │  (gemini-1.5-flash)  │
              └──────────────────────┘
                         │
                         ▼
                  AI-Generated Response
```

### Project Structure

```
ecombot/
├── genesis_ecommerce/
│   ├── app.py                    # FastAPI application
│   ├── config.py                 # Settings (includes gemini_api_key)
│   ├── logger.py                 # Logging configuration
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py       # API router registration
│   │       ├── orders.py         # Order endpoints
│   │       └── support.py        # Support & chatbot endpoints
│   ├── customer_support_bot/
│   │   ├── bot.py                # Core chatbot logic
│   │   ├── documents/            # RAG knowledge base
│   │   │   ├── terms_and_conditions.txt
│   │   │   └── support_guide.txt
│   │   └── README.md             # Detailed chatbot docs
│   └── db/
│       ├── core.py               # Database engine and session
│       └── schema.py             # SQLModel table definitions
├── migrate.py                    # Database migration script
├── seed_data.py                  # Sample data seeding
├── setup_db.py                   # Automated DB setup
├── run.py                        # Development server runner
├── test_chatbot.py               # Chatbot demo/test script
├── README.md                     # Main project README
├── CHATBOT_GUIDE.md              # This comprehensive guide
└── pyproject.toml                # Project dependencies
```

---

## Troubleshooting

### Installation Issues

#### "Import google.generativeai could not be resolved"
**Fix**: Install the package
```bash
pip install google-generativeai
```

#### "GEMINI_API_KEY not found"
**Fix**: Check your `.env` file has the correct key
```env
GEMINI_API_KEY=your_actual_key_here
```

**Note**: Don't use placeholder text - get a real key from https://aistudio.google.com/app/apikey

### Runtime Issues

#### "Connection refused" when testing
**Fix**: Make sure the server is running
```bash
python run.py
```

#### Slow responses
**Expected**: AI generation takes 1-3 seconds. Already using the fastest model (gemini-1.5-flash).

**To improve**:
- Reduce document size (edit files in `documents/`)
- Limit conversation history (currently max 5 messages)

#### Bot gives generic responses
**Fix**: Provide context parameters:
```python
# Instead of this:
{"message": "What's my order status?"}

# Do this:
{"message": "What's my order status?", "order_id": 123}
```

#### Empty or error responses
**Check**:
1. API key is valid (test at https://aistudio.google.com/)
2. You haven't exceeded quota (15 free requests/minute)
3. Check server logs for errors
4. Verify database has data (`python seed_data.py`)

### Database Issues

#### "No such table" errors
**Fix**: Run migration
```bash
python migrate.py
```

#### "Database is locked"
**Fix**: SQLite doesn't handle high concurrency well. For production, consider PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

---

## Advanced Usage

### Custom Knowledge Base

Add your own documents to `genesis_ecommerce/customer_support_bot/documents/`:

```python
# The bot automatically loads all .txt files
# Just add a new file:
custom_policy.txt
```

### Change AI Model

Edit `genesis_ecommerce/customer_support_bot/bot.py`:

```python
# Line ~34 - Change the model
self.model = genai.GenerativeModel('gemini-1.5-pro')  # More capable but slower
# or
self.model = genai.GenerativeModel('gemini-1.0-pro')  # Older version
```

**Available Models**:
- `gemini-1.5-flash` - Fastest, recommended (default)
- `gemini-1.5-pro` - More capable, slower
- `gemini-1.0-pro` - Older, stable

### Customize System Prompt

Edit the `system_prompt` in `CustomerSupportBot.__init__()` to change:
- Bot personality and tone
- Response structure
- Specific instructions
- Formatting preferences

### Add Authentication

Protect your endpoints with FastAPI dependencies:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.post("/chat")
async def chat_with_bot(
    chat_request: ChatRequest,
    session: Session = Depends(get_session),
    token: str = Depends(security)  # Add this
):
    # Verify token
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    # ... rest of code
```

### Rate Limiting

Prevent abuse with rate limiting:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/chat")
@limiter.limit("10/minute")  # 10 requests per minute
async def chat_with_bot(...):
    # ... code
```

---

## Security & Best Practices

### Security Checklist

⚠️ **Critical**:
- ✅ Never commit `.env` file with real API keys
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables for all secrets
- ✅ Implement authentication in production
- ✅ Add rate limiting to prevent abuse
- ✅ Sanitize user inputs before processing
- ✅ Monitor API usage and costs
- ✅ Set up proper error handling
- ✅ Log all interactions for audit

### Best Practices

**1. Always Provide Context**
```python
# Good
{"message": "Order status?", "order_id": 123}

# Less effective
{"message": "Order status?"}
```

**2. Use Conversation History**
```python
# For multi-turn conversations
{
  "message": "How long does that take?",
  "conversation_history": [...]  # Include previous messages
}
```

**3. Be Specific**
```python
# Good
{"message": "What is the return policy for electronics?"}

# Less effective
{"message": "Returns?"}
```

**4. Handle Errors Gracefully**
```python
try:
    response = requests.post(...)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    # Handle error appropriately
    logger.error(f"Chat request failed: {e}")
```

**5. Monitor Usage**
- Track API calls to stay within quota
- Log response times
- Monitor error rates
- Set up alerts for failures

### Cost Management

**Google Gemini 1.5 Flash Pricing**:
- **Free Tier**: 15 requests per minute
- **Paid Tier**: ~$0.00001 per request (very affordable)

**Monitor at**: https://aistudio.google.com/

**Tips to Reduce Costs**:
- Cache common responses
- Implement client-side validation
- Use rate limiting
- Optimize document size

---

## Next Steps

### To Start Using

1. ✅ Install dependencies: `pip install -e .`
2. ✅ Get Gemini API key from https://aistudio.google.com/app/apikey
3. ✅ Add to `.env` file
4. ✅ Run `python setup_db.py` (or `migrate.py` + `seed_data.py`)
5. ✅ Start server: `python run.py`
6. ✅ Test: `python test_chatbot.py` or visit http://localhost:8000/docs

### Optional Enhancements

**Backend**:
- [ ] Add user authentication
- [ ] Implement rate limiting
- [ ] Add response caching
- [ ] Store conversation history in database
- [ ] Add more knowledge base documents
- [ ] Implement feedback collection
- [ ] Add analytics/metrics logging
- [ ] Set up monitoring and alerts

**Frontend**:
- [ ] Create web UI for chat interface
- [ ] Build mobile app integration
- [ ] Add voice input/output
- [ ] Implement typing indicators
- [ ] Add suggested questions

**Advanced Features**:
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Auto-escalation to human agents
- [ ] Integration with CRM systems
- [ ] A/B testing different prompts
- [ ] Fine-tune model on your data

---

## Resources

- **Detailed Chatbot Docs**: `genesis_ecommerce/customer_support_bot/README.md`
- **Interactive API Docs**: http://localhost:8000/docs (when server running)
- **Main Project README**: `README.md`
- **Gemini API Documentation**: https://ai.google.dev/docs
- **Get API Key**: https://aistudio.google.com/app/apikey
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/

---

## Support

If you encounter issues:

1. **Check troubleshooting section** above
2. **Review server logs** for error messages
3. **Verify `.env` configuration** has correct values
4. **Ensure database is initialized** (`python migrate.py`)
5. **Test with demo script** (`python test_chatbot.py`)
6. **Check API key validity** at https://aistudio.google.com/

---

**Project**: Genesis E-commerce Customer Support Bot  
**Created**: November 11, 2025  
**Technology**: Python, FastAPI, Google Gemini, SQLModel, SQLite  
**Status**: ✅ Complete and Ready to Use

---

**You're all set! 🎉 Start the server and try asking the bot a question!**
