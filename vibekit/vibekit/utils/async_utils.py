"""
Asynchronous utilities for VibeKit.
"""

import asyncio
import functools
import logging
import sys
from typing import Any, Callable, Coroutine, TypeVar, cast

T = TypeVar('T')

logger = logging.getLogger(__name__)

def run_async(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., T]:
    """
    Decorator to run an async function in the event loop.
    
    This decorator allows calling async functions from synchronous code.
    It's useful for creating synchronous wrappers around async functions.
    
    Args:
        func: Async function to run
        
    Returns:
        Synchronous function that runs the async function in the event loop
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        """
        Wrapper function that runs the async function in the event loop.
        
        Args:
            *args: Positional arguments to pass to the async function
            **kwargs: Keyword arguments to pass to the async function
            
        Returns:
            Result of the async function
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If no event loop exists in the current thread, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_running():
            # If the loop is already running (e.g., in a Jupyter notebook),
            # we need to use a different approach
            if sys.version_info >= (3, 7):
                # For Python 3.7+, we can use asyncio.run_coroutine_threadsafe
                # with a new event loop in a separate thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(asyncio.run, func(*args, **kwargs))
                    return future.result()
            else:
                # For Python < 3.7, warn the user that they should use
                # the async version directly
                logger.warning(
                    "Event loop is already running. Cannot run async function synchronously. "
                    "Please use the async version directly."
                )
                raise RuntimeError(
                    "Event loop is already running. Cannot run async function synchronously. "
                    "Please use the async version directly."
                )
        else:
            # If the loop is not running, we can use asyncio.run (Python 3.7+)
            # or loop.run_until_complete
            if sys.version_info >= (3, 7):
                return asyncio.run(func(*args, **kwargs))
            else:
                return loop.run_until_complete(func(*args, **kwargs))
    
    return wrapper 