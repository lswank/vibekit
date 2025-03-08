# VibeKit Examples

This directory contains examples demonstrating how to use VibeKit in various scenarios.

## Running the Examples

Before running the examples, ensure you have installed VibeKit:

```bash
# Install VibeKit
pip install vibekit

# Or if you're developing locally
pip install -e ..
```

Most examples require an API key for either OpenAI or Anthropic. Set it as an environment variable:

```bash
# For OpenAI
export OPENAI_API_KEY=your_openai_api_key

# For Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

Then run the example you want:

```bash
# Run the simple example
python simple_example.py

# Run the data analysis example
python data_analysis_example.py

# Run domain-specific examples
python chemistry_example.py
python biology_example.py
python physics_example.py
python law_example.py
python accounting_example.py

# Run advanced meta-example (VibeKit orchestrating VibeKit)
python meta_example.py
```

## Available Examples

### General Examples

- **simple_example.py**: Demonstrates basic usage of VibeKit for various types of functions including math operations, string manipulation, data transformation, creative generation, and complex logic.
- **data_analysis_example.py**: Shows more advanced usage with data generation, analysis, forecasting, and visualization in the terminal.

### Domain-Specific Examples

- **chemistry_example.py**: Demonstrates analyzing molecular formulas, predicting chemical properties, balancing chemical equations, and simulating reactions.
- **biology_example.py**: Shows DNA sequence analysis, protein structure prediction, phylogenetic tree generation, and cellular pathway simulation.
- **physics_example.py**: Covers kinematics problems, electrical circuit analysis, quantum mechanical calculations, and gravitational simulations.
- **law_example.py**: Illustrates legal document analysis, contract clause extraction, legal risk assessment, and case precedent comparison.
- **accounting_example.py**: Features financial statement analysis, ratio calculations, depreciation scheduling, tax calculations, and financial forecasting.

### Advanced Meta-Example

- **meta_example.py**: Demonstrates recursive capabilities where VibeKit uses VibeKit to solve complex problems through multi-stage orchestration:
  - Implements a two-tier architecture with a meta-level client for task planning and a worker client for execution
  - Showcases dynamic workflow generation where the system designs its own processing pipeline
  - Demonstrates cross-domain problem solving by coordinating specialists from different domains
  - Features a self-improving system that evaluates and refines its own outputs iteratively

## Creating Your Own Examples

Feel free to create your own examples by copying and modifying the existing ones. The key steps are:

1. Import `VibeKitClient` from `vibekit`
2. Initialize the client with your API key
3. Connect to the service with `await client.connect()`
4. Call any function you can imagine using `await client.your_function_name(...)`
5. Disconnect when you're done with `await client.disconnect()`

Remember that VibeKit is async, so your functions should be defined with `async def` and called with `await`. 