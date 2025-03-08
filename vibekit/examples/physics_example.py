#!/usr/bin/env python3
"""
Physics Example

This example demonstrates VibeKit's ability to:
1. Solve kinematics problems
2. Analyze electrical circuits
3. Calculate quantum mechanical properties
4. Simulate gravitational systems
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
        print("STEP 1: Solve kinematics problems")
        print("="*50)
        
        # Problem: A car accelerates from rest at 3 m/s² for 10 seconds. What is its final velocity and distance traveled?
        kinematics_solution = await client.solve_kinematics_problem(
            initial_velocity=0,  # m/s
            acceleration=3,      # m/s²
            time=10              # seconds
        )
        
        print("\nKinematics Solution:")
        print(json.dumps(kinematics_solution, indent=2))
        
        print("\n" + "="*50)
        print("STEP 2: Analyze electrical circuit")
        print("="*50)
        
        # A simple circuit with resistors in series and parallel
        circuit_analysis = await client.analyze_electrical_circuit(
            components=[
                {"type": "voltage_source", "value": 12, "unit": "V", "id": "V1"},
                {"type": "resistor", "value": 100, "unit": "ohm", "id": "R1"},
                {"type": "resistor", "value": 200, "unit": "ohm", "id": "R2"},
                {"type": "resistor", "value": 300, "unit": "ohm", "id": "R3"}
            ],
            connections=[
                ["V1", "R1"],
                ["R1", "R2"],
                ["R1", "R3"],
                ["R2", "V1"],
                ["R3", "V1"]
            ]
        )
        
        print("\nElectrical Circuit Analysis:")
        print(json.dumps(circuit_analysis, indent=2))
        
        print("\n" + "="*50)
        print("STEP 3: Calculate quantum properties")
        print("="*50)
        
        # Calculate properties of a hydrogen atom
        quantum_properties = await client.calculate_quantum_properties(
            system="hydrogen_atom", 
            parameters={"principal_quantum_number": 2}
        )
        
        print("\nQuantum Properties Calculation:")
        print(json.dumps(quantum_properties, indent=2))
        
        print("\n" + "="*50)
        print("STEP 4: Simulate gravitational system")
        print("="*50)
        
        # Simulate a simple solar system with three bodies
        gravitational_simulation = await client.simulate_gravitational_system(
            bodies=[
                {"name": "Star", "mass": 1.0, "position": [0, 0, 0], "velocity": [0, 0, 0]},
                {"name": "Planet 1", "mass": 0.001, "position": [1, 0, 0], "velocity": [0, 1, 0]},
                {"name": "Planet 2", "mass": 0.0005, "position": [0, 1.5, 0], "velocity": [-0.8, 0, 0]}
            ],
            duration=1.0,  # years
            time_steps=100
        )
        
        print("\nGravitational Simulation Results:")
        print(f"Simulated {len(gravitational_simulation['trajectories'])} trajectories over {gravitational_simulation['time_steps']} time steps")
        print("Final positions:")
        for body in gravitational_simulation["final_state"]:
            print(f"  {body['name']}: {body['position']}")
        
        print("\n" + "="*50)
        print("STEP 5: Solve relativity problem")
        print("="*50)
        
        # Calculate relativistic effects for a fast-moving object
        relativity_solution = await client.calculate_relativistic_effects(
            velocity=0.8,  # as fraction of speed of light
            rest_mass=1.0  # kg
        )
        
        print("\nRelativity Calculation:")
        print(json.dumps(relativity_solution, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 