# Interactive Hohmann Transfer Calculator

This example demonstrates using VibeKit to create a web interface for calculating Hohmann transfer orbits.

## Features

- Web-based interface for calculating Hohmann transfer parameters
- Dynamically generated HTML
- Interactive form for changing orbital parameters
- Visualization of the transfer orbit

## Requirements

- Python 3.9+
- Flask
- VibeKit

## Setup
1. Set up the environment:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   
   # Install dependencies
   ./setup_uv.py  # This will install VibeKit
   uv install flask
   ```

2. Set your API key as an environment variable:
   ```
   # For OpenAI
   export OPENAI_API_KEY=your_openai_api_key

   # For Anthropic
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Running the Example

Run the script:
```
python interactive_physics_example.py
```

The web server will start at: http://localhost:8888

## How It Works

This example uses:

1. **Flask** to serve the web interface
2. **VibeKit** to order an LLM to:
   - Generate HTML for the interface
   - Calculate Hohmann transfer parameters
   - Generate visualization of the results

VibeKit is used not only to farm out the orbital mechanics calculations but also to outsource generating the entire user interface HTML - no manual HTML coding required!
(Is this horribly inefficient? Of course.)