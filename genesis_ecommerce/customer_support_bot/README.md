# Genesis E-commerce Customer Support Chatbot

An AI-powered customer support chatbot using Google Gemini with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- 🤖 **AI-Powered Responses**: Uses Google Gemini 1.5 Flash for fast, intelligent responses
- 📚 **RAG-Based Knowledge**: Retrieves information from Terms & Conditions and Support Guide
- 🎫 **Ticket Integration**: Access real-time ticket and order information from the database
- 💬 **Context-Aware**: Maintains conversation history for coherent multi-turn dialogues
- 🔍 **Multi-Context Support**: Can answer questions about orders, tickets, and general policies

## Setup

### 1. Install Dependencies

```bash
pip install -e .
```

This will install all required packages including `google-generativeai`.

### 2. Configure Environment Variables

Add your Gemini API key to your `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
GEMINI_API_KEY=your_gemini_api_key_here
```

To get a Gemini API key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy it to your `.env` file

### 3. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Chat Endpoints

#### 1. General Chat
**POST** `/v1/support/chat`

Chat with the bot about anything. Provide optional context for better responses.

**Request Body:**
```json
{
  "message": "What is your return policy?",
  "order_id": 123,
  "ticket_id": 456,
  "user_id": 789,
  "conversation_history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help you?"}
  ]
}
```

**Response:**
```json
{
  "response": "Our return policy allows you to return items within 30 days..."
}
```

#### 2. Order-Specific Chat
**POST** `/v1/support/chat/order/{order_id}?message=your_question`

Ask questions about a specific order.

**Example:**
```bash
curl -X POST "http://localhost:8000/v1/support/chat/order/123?message=What%20is%20the%20status%20of%20my%20order?"
```

**Response:**
```json
{
  "response": "Your order #123 is currently in SHIPPED status. It was created on..."
}
```

#### 3. Ticket-Specific Chat
**POST** `/v1/support/chat/ticket/{ticket_id}?message=your_question`

Ask questions about a specific support ticket.

**Example:**
```bash
curl -X POST "http://localhost:8000/v1/support/chat/ticket/456?message=What%20is%20my%20ticket%20status?"
```

## Usage Examples

### Example 1: General Policy Question

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "How long does shipping take?"
    }
)

print(response.json()["response"])
# Output: Standard shipping takes 5-7 business days, express shipping takes 2-3 business days...
```

### Example 2: Order Status Inquiry

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "What's the status of my order?",
        "order_id": 123
    }
)

print(response.json()["response"])
# Output: Your order #123 is currently in PROCESSING status...
```

### Example 3: Multi-Turn Conversation

```python
import requests

# First message
response1 = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "Can I return a product?"
    }
)

# Follow-up with context
response2 = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "How long do I have to return it?",
        "conversation_history": [
            {"role": "user", "content": "Can I return a product?"},
            {"role": "assistant", "content": response1.json()["response"]}
        ]
    }
)

print(response2.json()["response"])
# Output: You have 30 days from the delivery date to return items...
```

### Example 4: User's All Orders

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/support/chat",
    json={
        "message": "Show me all my orders",
        "user_id": 789
    }
)

print(response.json()["response"])
# Output: You have 3 orders: Order #123 (SHIPPED), Order #124 (DELIVERED)...
```

## Testing with cURL

### General Chat
```bash
curl -X POST "http://localhost:8000/v1/support/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your business hours?"
  }'
```

### Order Chat
```bash
curl -X POST "http://localhost:8000/v1/support/chat/order/123?message=Where%20is%20my%20order?" \
  -H "Content-Type: application/json"
```

### Ticket Chat
```bash
curl -X POST "http://localhost:8000/v1/support/chat/ticket/456?message=Update%20on%20my%20issue?" \
  -H "Content-Type: application/json"
```

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI with interactive API testing.

## Knowledge Base

The chatbot has access to:

### 1. Terms and Conditions
- Order processing policies
- Payment terms
- Shipping and delivery information
- Returns and refunds
- Cancellation policy
- Privacy and data protection
- Customer support hours

### 2. Support Guide
- Order tracking instructions
- Return process steps
- Shipping options and costs
- Payment troubleshooting
- Account management
- Technical support
- FAQ section

### 3. Real-Time Database Information
- Order details (ID, status, items, dates)
- Ticket information (ID, status, issue description)
- User's order history

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  FastAPI Endpoint           │
│  /v1/support/chat           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  CustomerSupportBot         │
│  - Load RAG documents       │
│  - Fetch DB context         │
│  - Build prompt             │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Google Gemini API          │
│  (gemini-1.5-flash)         │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Response to Client         │
└─────────────────────────────┘
```

## Customization

### Adding More Documents

Add new text files to `genesis_ecommerce/customer_support_bot/documents/`:

```python
# The bot automatically loads all .txt files in the documents directory
new_doc = documents_dir / "new_policy.txt"
```

### Changing the AI Model

Edit `genesis_ecommerce/customer_support_bot/bot.py`:

```python
# Use a different Gemini model
self.model = genai.GenerativeModel('gemini-1.5-pro')  # More capable but slower
# or
self.model = genai.GenerativeModel('gemini-1.0-pro')  # Older version
```

### Adjusting the System Prompt

Modify the `system_prompt` in `CustomerSupportBot.__init__()` to change the bot's behavior, tone, or instructions.

## Troubleshooting

### Error: "Import google.generativeai could not be resolved"

Install the package:
```bash
pip install google-generativeai
```

### Error: "GEMINI_API_KEY not found"

Make sure your `.env` file contains:
```env
GEMINI_API_KEY=your_actual_api_key
```

### Slow Responses

- Consider using `gemini-1.5-flash` (default) instead of `gemini-1.5-pro`
- Reduce conversation history size (currently limited to last 5 messages)
- Optimize document size

### Rate Limiting

Google Gemini API has rate limits. For production:
- Implement request throttling
- Add retry logic with exponential backoff
- Consider caching common responses

## Best Practices

1. **Always provide context**: Include `order_id`, `ticket_id`, or `user_id` when available
2. **Use conversation history**: For multi-turn conversations, pass previous messages
3. **Be specific**: Detailed questions get better answers
4. **Handle errors**: Implement proper error handling in production
5. **Monitor usage**: Track API calls to stay within quota limits

## Security Notes

- Never commit your `.env` file with API keys
- Use environment variables for all sensitive configuration
- Implement rate limiting to prevent abuse
- Add authentication to API endpoints in production
- Sanitize user inputs before processing

## License

This project is part of Genesis E-commerce platform.
