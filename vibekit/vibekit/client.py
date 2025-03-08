"""
Main client implementation for VibeKit.
"""

import asyncio
import inspect
import logging
from typing import Any, Dict, List, Optional, Union

from .core.interpreter import FunctionInterpreter

logger = logging.getLogger(__name__)

class VibeKitClient:
    """
    VibeKit client that provides dynamic function execution capabilities.
    
    The client interprets and executes functions based on their names and parameters,
    using large language models (OpenAI or Anthropic) to understand the user's intent.
    """
    
    def __init__(
        self,
        api_key: str,
        timeout: float = 30.0,
        retries: int = 3,
        debug: bool = False
    ):
        """
        Initialize the VibeKit client.
        
        Args:
            api_key: API key for OpenAI or Anthropic (required)
            timeout: Request timeout in seconds (optional, defaults to 30.0)
            retries: Number of retry attempts (optional, defaults to 3)
            debug: Enable debug logging (optional, defaults to False)
        """
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries
        self.debug = debug
        self._interpreter = None
        self._connected = False
        
        # Configure logging based on debug setting
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level)
        
        logger.info("VibeKit client initialized")
        
    async def connect(self) -> None:
        """
        Initialize the function interpreter and connect to the appropriate LLM service.
        
        This method must be called before any dynamic function calls.
        
        Returns:
            None
        """
        logger.info("Initializing VibeKit...")
        
        # Determine which LLM provider to use based on API key format
        provider = self._detect_provider(self.api_key)
        
        # Initialize the function interpreter
        self._interpreter = FunctionInterpreter(
            api_key=self.api_key,
            provider=provider,
            timeout=self.timeout,
            retries=self.retries
        )
        
        # Test the connection
        await self._interpreter.test_connection()
        
        self._connected = True
        logger.info("VibeKit initialized using %s provider", provider)
    
    async def disconnect(self) -> None:
        """
        Disconnect and clean up resources.
        
        Returns:
            None
        """
        logger.info("Disconnecting VibeKit...")
        self._connected = False
        logger.info("VibeKit disconnected")
    
    def set_config(self, options: Dict[str, Any]) -> None:
        """
        Update client configuration.
        
        Args:
            options: Dictionary containing configuration options
            
        Returns:
            None
        """
        for key, value in options.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.debug("Updated configuration: %s = %s", key, value)
                
        # Update interpreter if it exists
        if self._interpreter is not None:
            self._interpreter.update_config(options)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current connection status.
        
        Returns:
            Dictionary containing status information
        """
        return {
            "connected": self._connected,
            "provider": self._interpreter.provider if self._interpreter else None,
            "model": self._interpreter.model if hasattr(self._interpreter, "model") else None
        }
    
    def _detect_provider(self, api_key: str) -> str:
        """
        Detect the LLM provider based on the API key format.
        
        Args:
            api_key: API key
            
        Returns:
            Provider name ("openai" or "anthropic")
        """
        if api_key.startswith("sk-proj"):
            return "openai"
        elif api_key.startswith(("sk-ant-", "sk-a-")):
            return "anthropic"
        else:
            # Default to OpenAI if format is unknown
            logger.warning("Unknown API key format, defaulting to OpenAI")
            return "openai"
    
    def __getattr__(self, name: str) -> Any:
        """
        Handle dynamic function calls by forwarding them to the interpreter.
        
        This method is called when an attribute lookup fails, allowing us to
        dynamically handle any function name the user calls.
        
        Args:
            name: Function name
            
        Returns:
            Async function that will execute the dynamic call
        """
        if not self._connected:
            raise RuntimeError("Not connected to VibeKit service. Call connect() first.")
        
        # Return a callable that will forward the request to the interpreter
        async def dynamic_function(*args, **kwargs):
            logger.debug("Dynamic function call: %s(%s, %s)", name, args, kwargs)
            return await self._interpreter.execute_function(name, args, kwargs)
        
        return dynamic_function 