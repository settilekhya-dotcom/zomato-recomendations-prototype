import os
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GroqClient:
    """
    Wrapper for Groq API interaction.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the Groq client.
        
        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
            model: Model name to use for completions
        """
        # Try to get API key from various sources:
        # 1. Explicitly passed argument
        # 2. Environment variable
        # 3. Streamlit secrets (for cloud deployment)
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            try:
                import streamlit as st
                if hasattr(st, "secrets"):
                    self.api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                pass

        if not self.api_key:
            raise ValueError("Groq API key not found. Please set GROQ_API_KEY in .env file or Streamlit secrets.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def get_completion(self, messages: List[Dict[str, str]], temperature: float = 0.5, max_tokens: int = 1000) -> str:
        """
        Get a completion from the Groq API.
        
        Args:
            messages: List of message dictionaries (role, content)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            The completion string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            raise
