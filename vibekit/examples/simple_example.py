#!/usr/bin/env python3
"""
Simple example of using VibeKit.

This example demonstrates basic usage of VibeKit for various types of functions.
"""

import asyncio
import os
from typing import Dict, List

from vibekit import VibeKitClient


async def main():
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
        return
    
    # Initialize the client
    client = VibeKitClient(
        api_key=api_key,
        debug=True  # Enable debug logging
    )
    
    print("Connecting to VibeKit...")
    await client.connect()
    
    # Check the status
    status = client.get_status()
    print(f"Connected using {status['provider']} provider")
    
    try:
        # Example 1: Simple math
        print("\n--- Example 1: Simple Math ---")
        result = await client.calculate_sum(5, 10)
        print(f"5 + 10 = {result}")
        
        # Example 2: String manipulation
        print("\n--- Example 2: String Manipulation ---")
        result = await client.reverse_string("hello world")
        print(f"Reversed: {result}")
        
        # Example 3: Data transformation
        print("\n--- Example 3: Data Transformation ---")
        users = [
            {"name": "John", "age": 25},
            {"name": "Jane", "age": 32},
            {"name": "Bob", "age": 18}
        ]
        result = await client.filter_users_by_age(users, min_age=21)
        print(f"Filtered users: {result}")
        
        # Example 4: Creative generation
        print("\n--- Example 4: Creative Generation ---")
        result = await client.create_short_poem_about("artificial intelligence")
        print(f"Poem:\n{result}")
        
        # Example 5: Function with complex logic
        print("\n--- Example 5: Complex Logic ---")
        scores = [85, 90, 78, 92, 88, 76, 95, 89]
        result = await client.analyze_scores(scores)
        print(f"Score analysis: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 