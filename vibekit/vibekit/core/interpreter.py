"""
Function interpreter for VibeKit.

This module contains the implementation of the function interpreter that
translates dynamic function calls into actions using language models.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

class FunctionInterpreter:
    """
    Interpreter for dynamic function calls.
    
    This class is responsible for interpreting function calls based on their names
    and parameters, using language models to understand the user's intent.
    """
    
    def __init__(
        self,
        api_key: str,
        provider: str,
        timeout: float,
        retries: int
    ):
        """
        Initialize the function interpreter.
        
        Args:
            api_key: API key for the language model provider
            provider: Provider name ("openai" or "anthropic")
            timeout: Request timeout in seconds
            retries: Number of retry attempts
        """
        self.api_key = api_key
        self.provider = provider
        self.timeout = timeout
        self.retries = retries
        self.model = self._get_default_model()
        
        # Initialize provider-specific client
        self._client = self._initialize_client()
        
        logger.debug("Function interpreter initialized with provider: %s", provider)
    
    def _get_default_model(self) -> str:
        """
        Get the default model for the selected provider.
        
        Returns:
            Default model name
        """
        if self.provider == "openai":
            return "gpt-4o-mini"
        elif self.provider == "anthropic":
            return "claude-3-7-sonnet"
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _initialize_client(self) -> Any:
        """
        Initialize the provider-specific client.
        
        Returns:
            Client object for the selected provider
        """
        if self.provider == "openai":
            try:
                import openai
                client = openai.AsyncClient(api_key=self.api_key)
                logger.debug("OpenAI client initialized")
                return client
            except ImportError:
                raise ImportError("OpenAI package is required. Install with: pip install openai")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize OpenAI client: {e}")
        
        elif self.provider == "anthropic":
            try:
                import anthropic
                client = anthropic.AsyncAnthropic(api_key=self.api_key)
                logger.debug("Anthropic client initialized")
                return client
            except ImportError:
                raise ImportError("Anthropic package is required. Install with: pip install anthropic")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Anthropic client: {e}")
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def test_connection(self) -> bool:
        """
        Test the connection to the language model provider.
        
        Returns:
            True if the connection is successful, False otherwise
        """
        try:
            if self.provider == "openai":
                # Test OpenAI connection with a simple completion
                response = await self._client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                return True
            
            elif self.provider == "anthropic":
                # Test Anthropic connection with a simple completion
                response = await self._client.messages.create(
                    model="claude-3-7-sonnet",
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hello"}]
                )
                return True
            
        except Exception as e:
            logger.error("Connection test failed: %s", e)
            raise ConnectionError(f"Failed to connect to {self.provider} API: {e}")
    
    def update_config(self, options: Dict[str, Any]) -> None:
        """
        Update interpreter configuration.
        
        Args:
            options: Dictionary containing configuration options
            
        Returns:
            None
        """
        for key, value in options.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.debug("Updated interpreter configuration: %s = %s", key, value)
        
        # Reinitialize client if provider or API key changed
        if "provider" in options or "api_key" in options:
            if "provider" in options:
                self.model = self._get_default_model()
            self._client = self._initialize_client()
    
    async def execute_function(
        self, 
        function_name: str, 
        args: Tuple[Any, ...], 
        kwargs: Dict[str, Any]
    ) -> Any:
        """
        Execute a dynamic function call.
        
        Args:
            function_name: Name of the function to execute
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Result of the function execution
        """
        # Convert function call to a description
        function_description = self._format_function_description(function_name, args, kwargs)
        
        # Get function implementation through LLM
        result = await self._get_function_implementation(function_description)
        
        return result
    
    def _format_function_description(
        self, 
        function_name: str, 
        args: Tuple[Any, ...], 
        kwargs: Dict[str, Any]
    ) -> str:
        """
        Format a function call into a natural language description.
        
        Args:
            function_name: Name of the function
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Natural language description of the function call
        """
        # Convert snake_case to human-readable form
        readable_name = " ".join(function_name.split("_"))
        
        # Format args and kwargs into strings
        args_str = ", ".join(str(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        
        # Combine all parameters
        params_str = ""
        if args_str and kwargs_str:
            params_str = f"{args_str}, {kwargs_str}"
        elif args_str:
            params_str = args_str
        elif kwargs_str:
            params_str = kwargs_str
        
        # Create the final description
        if params_str:
            return f"{readable_name} with parameters: {params_str}"
        else:
            return readable_name
    
    async def _get_function_implementation(self, function_description: str) -> Any:
        """
        Get the implementation of a function from its description using a language model.
        
        Args:
            function_description: Natural language description of the function
            
        Returns:
            Result of the function execution
        """
        for attempt in range(self.retries + 1):
            try:
                if self.provider == "openai":
                    return await self._execute_with_openai(function_description)
                elif self.provider == "anthropic":
                    return await self._execute_with_anthropic(function_description)
                
            except Exception as e:
                if attempt < self.retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(
                        "Attempt %d failed: %s. Retrying in %d seconds...",
                        attempt + 1, e, wait_time
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("All %d attempts failed", self.retries + 1)
                    raise
    
    async def _execute_with_openai(self, function_description: str) -> Any:
        """
        Execute a function using OpenAI.
        
        Args:
            function_description: Natural language description of the function
            
        Returns:
            Result of the function execution
        """
        system_prompt = (
            "You are VibeKit, a dynamic function interpreter. "
            "Interpret and execute the following function request. "
            "Return only the result in a JSON format that can be parsed."
        )
        
        user_prompt = f"Execute this function: {function_description}"
        
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            timeout=self.timeout
        )
        
        try:
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            # If the result has a 'result' field, return that, otherwise return the whole object
            return result.get("result", result)
            
        except json.JSONDecodeError:
            logger.error("Failed to parse OpenAI response as JSON: %s", response)
            raise ValueError("OpenAI returned an invalid JSON response")
    
    async def _execute_with_anthropic(self, function_description: str) -> Any:
        """
        Execute a function using Anthropic.
        
        Args:
            function_description: Natural language description of the function
            
        Returns:
            Result of the function execution
        """
        system_prompt = (
            "You are VibeKit, a dynamic function interpreter. "
            "Interpret and execute the following function request. "
            "Return only the result in a JSON format that can be parsed."
        )
        
        user_prompt = f"Execute this function: {function_description}"
        
        response = await self._client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.2,
            timeout=self.timeout
        )
        
        try:
            result_text = response.content[0].text
            # Try to extract JSON from the response
            if "{" in result_text and "}" in result_text:
                json_str = result_text[result_text.find("{"):result_text.rfind("}") + 1]
                result = json.loads(json_str)
                
                # If the result has a 'result' field, return that, otherwise return the whole object
                return result.get("result", result)
            else:
                logger.error("No JSON found in Anthropic response: %s", result_text)
                raise ValueError("Anthropic response does not contain valid JSON")
                
        except json.JSONDecodeError:
            logger.error("Failed to parse Anthropic response as JSON: %s", response)
            raise ValueError("Anthropic returned an invalid JSON response") 