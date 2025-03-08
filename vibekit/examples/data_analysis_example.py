#!/usr/bin/env python3
"""
Data Analysis Example

This example demonstrates VibeKit's ability to:
1. Generate synthetic data
2. Perform analysis on the data
3. Present results in a simple visualization (in the terminal)
"""

import asyncio
import os
import json
from typing import Dict, List, Any

try:
    from vibekit import VibeKitClient
except ImportError:
    print("VibeKit not found. Please run setup_uv.py first.")
    import sys
    sys.exit(1)


async def main():
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
        return
    
    # Initialize the client
    client = VibeKitClient(
        api_key=api_key,
        debug=False  # Set to True for more detailed logging
    )
    
    print("Connecting to VibeKit...")
    await client.connect()
    
    # Check the status
    status = client.get_status()
    print(f"Connected using {status['provider']} provider with model: {status.get('model', 'unknown')}")
    
    try:
        print("\n" + "="*50)
        print("STEP 1: Generate synthetic sales data")
        print("="*50)
        
        # Generate synthetic sales data for different products
        data = await client.generate_sales_data(
            products=["Widget A", "Widget B", "Widget C"],
            months=6,
            include_random_fluctuations=True
        )
        
        # Pretty print the data
        print("\nGenerated Sales Data:")
        print(json.dumps(data, indent=2))
        
        print("\n" + "="*50)
        print("STEP 2: Analyze the sales data")
        print("="*50)
        
        # Analyze the data to find trends and insights
        analysis = await client.analyze_sales_trends(data)
        
        # Pretty print the analysis
        print("\nSales Analysis:")
        print(json.dumps(analysis, indent=2))
        
        print("\n" + "="*50)
        print("STEP 3: Forecast future sales")
        print("="*50)
        
        # Forecast the next 3 months based on the trends
        forecast = await client.forecast_sales(data, months_ahead=3)
        
        # Pretty print the forecast
        print("\nSales Forecast for Next 3 Months:")
        print(json.dumps(forecast, indent=2))
        
        print("\n" + "="*50)
        print("STEP 4: Generate a simple ASCII chart visualization")
        print("="*50)
        
        # Generate a simple ASCII chart for visualization
        chart = await client.generate_ascii_chart(
            title="Monthly Sales by Product",
            data=data
        )
        
        # Print the ASCII chart
        print("\nASCII Chart:")
        print(chart)
        
        print("\n" + "="*50)
        print("STEP 5: Generate actionable recommendations")
        print("="*50)
        
        # Generate recommendations based on the analysis and forecast
        recommendations = await client.generate_recommendations(
            data=data,
            analysis=analysis,
            forecast=forecast
        )
        
        # Print the recommendations
        print("\nActionable Recommendations:")
        print(json.dumps(recommendations, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 