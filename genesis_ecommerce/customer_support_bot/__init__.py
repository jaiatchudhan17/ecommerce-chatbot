"""
Customer Support Bot module for Genesis E-commerce.

This module provides an AI-powered chatbot using Google Gemini
with RAG capabilities for customer support.
"""

from genesis_ecommerce.customer_support_bot.bot import (
    CustomerSupportBot,
    get_chatbot,
)

__all__ = ["CustomerSupportBot", "get_chatbot"]
