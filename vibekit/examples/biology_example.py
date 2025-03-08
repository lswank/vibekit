#!/usr/bin/env python3
"""
Biology Example

This example demonstrates VibeKit's ability to:
1. Analyze DNA sequences
2. Predict protein structures
3. Generate phylogenetic trees
4. Simulate cellular processes
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
        print("STEP 1: Analyze DNA sequences")
        print("="*50)
        
        # Sample DNA sequence (insulin gene fragment)
        dna_sequence = "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGA"
        
        dna_analysis = await client.analyze_dna_sequence(dna_sequence)
        print("\nDNA Sequence Analysis:")
        print(json.dumps(dna_analysis, indent=2))
        
        print("\n" + "="*50)
        print("STEP 2: Transcribe DNA to RNA and translate to protein")
        print("="*50)
        
        protein_result = await client.transcribe_and_translate(dna_sequence)
        print("\nTranscription and Translation Results:")
        print(json.dumps(protein_result, indent=2))
        
        print("\n" + "="*50)
        print("STEP 3: Predict protein structure properties")
        print("="*50)
        
        # Sample protein sequence (insulin)
        protein_sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKA"
        
        structure_prediction = await client.predict_protein_properties(protein_sequence)
        print("\nPredicted Protein Properties:")
        print(json.dumps(structure_prediction, indent=2))
        
        print("\n" + "="*50)
        print("STEP 4: Generate phylogenetic relationships")
        print("="*50)
        
        species = [
            "Homo sapiens (Human)",
            "Pan troglodytes (Chimpanzee)",
            "Gorilla gorilla (Gorilla)",
            "Pongo pygmaeus (Orangutan)",
            "Macaca mulatta (Rhesus macaque)"
        ]
        
        phylogenetic_tree = await client.generate_phylogenetic_tree(species)
        print("\nPhylogenetic Relationships:")
        print(phylogenetic_tree)
        
        print("\n" + "="*50)
        print("STEP 5: Simulate cellular pathway")
        print("="*50)
        
        pathway_simulation = await client.simulate_cellular_pathway(
            "Glycolysis",
            starting_molecules={"glucose": 10.0},  # mmol
            duration=60,  # seconds
            temperature=37.0  # Celsius
        )
        
        print("\nCellular Pathway Simulation Results:")
        print(json.dumps(pathway_simulation, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 