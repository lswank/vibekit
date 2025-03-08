#!/usr/bin/env python3
"""
Accounting Example

This example demonstrates VibeKit's ability to:
1. Analyze financial statements
2. Calculate financial ratios
3. Generate depreciation schedules
4. Perform tax calculations
5. Create financial forecasts
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
        print("STEP 1: Analyze financial statements")
        print("="*50)
        
        # Sample financial data
        financial_data = {
            "income_statement": {
                "revenue": 1250000,
                "cost_of_goods_sold": 750000,
                "operating_expenses": 200000,
                "interest_expense": 50000,
                "taxes": 60000
            },
            "balance_sheet": {
                "assets": {
                    "current_assets": {
                        "cash": 100000,
                        "accounts_receivable": 200000,
                        "inventory": 300000
                    },
                    "non_current_assets": {
                        "property_plant_equipment": 800000,
                        "intangible_assets": 200000
                    }
                },
                "liabilities": {
                    "current_liabilities": {
                        "accounts_payable": 150000,
                        "short_term_debt": 100000
                    },
                    "non_current_liabilities": {
                        "long_term_debt": 500000
                    }
                },
                "equity": {
                    "common_stock": 400000,
                    "retained_earnings": 450000
                }
            }
        }
        
        financial_analysis = await client.analyze_financial_statements(financial_data)
        print("\nFinancial Statement Analysis:")
        print(json.dumps(financial_analysis, indent=2))
        
        print("\n" + "="*50)
        print("STEP 2: Calculate financial ratios")
        print("="*50)
        
        ratios = await client.calculate_financial_ratios(financial_data)
        print("\nFinancial Ratios:")
        print(json.dumps(ratios, indent=2))
        
        print("\n" + "="*50)
        print("STEP 3: Generate depreciation schedule")
        print("="*50)
        
        asset = {
            "name": "Manufacturing Equipment",
            "cost": 120000,
            "salvage_value": 20000,
            "useful_life": 10,  # years
            "acquisition_date": "2023-01-15"
        }
        
        depreciation_schedule = await client.generate_depreciation_schedule(
            asset=asset,
            method="straight_line",
            periods=10  # years
        )
        
        print("\nDepreciation Schedule:")
        print(json.dumps(depreciation_schedule, indent=2))
        
        print("\n" + "="*50)
        print("STEP 4: Calculate taxes")
        print("="*50)
        
        tax_calculation = await client.calculate_business_taxes(
            income=1250000,
            expenses=1000000,
            deductions=50000,
            tax_year=2023,
            business_type="corporation",
            state="California"
        )
        
        print("\nTax Calculation:")
        print(json.dumps(tax_calculation, indent=2))
        
        print("\n" + "="*50)
        print("STEP 5: Generate financial forecast")
        print("="*50)
        
        # Generate a 3-year financial forecast
        forecast = await client.generate_financial_forecast(
            historical_data=financial_data,
            forecast_years=3,
            growth_assumptions={
                "revenue": 0.05,  # 5% annual growth
                "expenses": 0.03   # 3% annual growth
            }
        )
        
        print("\nFinancial Forecast:")
        print(json.dumps(forecast, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 