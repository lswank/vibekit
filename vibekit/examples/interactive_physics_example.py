#!/usr/bin/env python3
"""
Hohmann Transfer Example with Web Interface

This example demonstrates VibeKit's ability to:
1. Solve orbital mechanics problems (Hohmann transfer orbit)
2. Generate and serve a complete web interface entirely through intent
"""

import asyncio
import os
from flask import Flask, request, Response

try:
    from vibekit import VibeKitClient
except ImportError:
    print("VibeKit not found. Please run setup_uv.py first.")
    import sys
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)

# Global client and event loop
client = None
loop = None

@app.route('/')
def index():
    """Serve the main page with the calculator interface."""
    # Let VibeKit handle the entire interface generation
    async def get_page():
        response = await client.create_hohmann_transfer_calculator_html(
            page_title="Hohmann Transfer Calculator", 
            page_style="Make it look like the Apple homepage",
            description="Calculate parameters for a Hohmann transfer orbit between two circular orbits",
            form_action="/calculate",
            default_values={
                "initial_orbit_radius": 6778,
                "final_orbit_radius": 42164,
                "gravitational_parameter": 398600
            }
        )
        return response["html"] if isinstance(response, dict) and "html" in response else response
    
    result = loop.run_until_complete(get_page())
    return result

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle form submission and return results."""
    # Get form data
    initial_orbit_radius = float(request.form.get('initial_orbit_radius', 6778))
    final_orbit_radius = float(request.form.get('final_orbit_radius', 42164))
    gravitational_parameter = float(request.form.get('gravitational_parameter', 398600))
    
    # Let VibeKit handle both the calculation and result display
    async def get_results():
        response = await client.generate_hohmann_transfer_results_page_html(
            style="Make it look like the Apple homepage",
            initial_orbit_radius=initial_orbit_radius,
            final_orbit_radius=final_orbit_radius,
            gravitational_parameter=gravitational_parameter,
            include_visualization=True,
            visualization_style="ASCII ART STYLE",
            back_link_url="/"
        )
        return response["html"] if isinstance(response, dict) and "html" in response else response
    
    result = loop.run_until_complete(get_results())
    return result

async def setup_vibekit():
    """Set up the VibeKit client."""
    global client
    
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
        return False
    
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
    
    return True

def main():
    """Main function to set up the client and run the web server."""
    # Set up the event loop
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize VibeKit
    client_setup_success = loop.run_until_complete(setup_vibekit())
    
    if not client_setup_success:
        return
    
    try:
        print("Starting web server at http://localhost:8888")
        # Run Flask with standard (non-debug) settings
        app.run(host='0.0.0.0', port=8888, debug=False, use_reloader=False)
    
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        # Always disconnect when done
        if client:
            loop.run_until_complete(client.disconnect())
            print("\nDisconnected from VibeKit")

if __name__ == "__main__":
    main() 