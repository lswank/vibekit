#!/usr/bin/env python3
"""
Chemistry Example

This example demonstrates VibeKit's ability to:
1. Analyze molecular formulas
2. Predict chemical properties
3. Balance chemical equations
4. Simulate chemical reactions
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
        print("STEP 1: Analyze molecular formulas")
        print("="*50)
        
        molecules = ["H2O", "C6H12O6", "C2H5OH", "CH3COOH", "NaHCO3"]
        
        for molecule in molecules:
            analysis = await client.analyze_molecular_formula(molecule)
            print(f"\nAnalysis of {molecule}:")
            print(json.dumps(analysis, indent=2))
        
        print("\n" + "="*50)
        print("STEP 2: Predict chemical properties")
        print("="*50)
        
        ethanol_properties = await client.predict_chemical_properties("C2H5OH")
        print("\nPredicted Properties of Ethanol (C2H5OH):")
        print(json.dumps(ethanol_properties, indent=2))
        
        print("\n" + "="*50)
        print("STEP 3: Balance chemical equations")
        print("="*50)
        
        equations = [
            "H2 + O2 -> H2O",
            "C + O2 -> CO2",
            "Fe + O2 -> Fe2O3",
            "C2H5OH + O2 -> CO2 + H2O"
        ]
        
        for equation in equations:
            balanced = await client.balance_chemical_equation(equation)
            print(f"\nUnbalanced: {equation}")
            print(f"Balanced: {balanced}")
        
        print("\n" + "="*50)
        print("STEP 4: Simulate a chemical reaction")
        print("="*50)
        
        reaction_simulation = await client.simulate_chemical_reaction(
            "2Na + 2H2O -> 2NaOH + H2",
            conditions={
                "temperature": 25,  # Celsius
                "pressure": 1.0,    # atm
                "catalysts": []
            }
        )
        
        print("\nReaction Simulation Results:")
        print(json.dumps(reaction_simulation, indent=2))
        
        print("\n" + "="*50)
        print("STEP 5: Generate lab protocol")
        print("="*50)
        
        lab_protocol = await client.generate_lab_protocol(
            "Synthesis of Aspirin",
            reagents=["salicylic acid", "acetic anhydride", "phosphoric acid"],
            equipment=["round-bottom flask", "heating mantle", "condenser", "thermometer", "magnetic stirrer"]
        )
        
        print("\nLab Protocol:")
        print(lab_protocol)
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 