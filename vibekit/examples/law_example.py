#!/usr/bin/env python3
"""
Law Example

This example demonstrates VibeKit's ability to:
1. Analyze legal documents
2. Extract contract clauses
3. Identify legal risks
4. Generate legal summaries
5. Compare case precedents
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
        print("STEP 1: Analyze legal document")
        print("="*50)
        
        # Sample employment contract
        employment_contract = """
        EMPLOYMENT AGREEMENT
        
        This Employment Agreement (the "Agreement") is made and entered into as of January 1, 2023, by and between XYZ Corporation ("Employer") and John Smith ("Employee").
        
        1. EMPLOYMENT
        Employer hereby employs Employee, and Employee hereby accepts employment with Employer, upon the terms and conditions set forth in this Agreement.
        
        2. TERM
        The term of this Agreement shall commence on January 15, 2023 and shall continue until terminated in accordance with the provisions of this Agreement.
        
        3. COMPENSATION
        Employer shall pay Employee a base salary of $75,000 per year, payable in accordance with Employer's standard payroll procedures.
        
        4. NON-COMPETE
        During the term of this Agreement and for a period of two (2) years thereafter, Employee shall not, directly or indirectly, engage in any business that competes with Employer within a 100-mile radius of Employer's principal place of business.
        
        5. GOVERNING LAW
        This Agreement shall be governed by and construed in accordance with the laws of the State of California.
        """
        
        document_analysis = await client.analyze_legal_document(employment_contract)
        print("\nLegal Document Analysis:")
        print(json.dumps(document_analysis, indent=2))
        
        print("\n" + "="*50)
        print("STEP 2: Extract contract clauses")
        print("="*50)
        
        clauses = await client.extract_contract_clauses(
            employment_contract,
            clause_types=["non-compete", "compensation", "term", "governing law"]
        )
        
        print("\nExtracted Contract Clauses:")
        print(json.dumps(clauses, indent=2))
        
        print("\n" + "="*50)
        print("STEP 3: Identify legal risks")
        print("="*50)
        
        risk_assessment = await client.assess_legal_risks(
            document=employment_contract,
            jurisdiction="California"
        )
        
        print("\nLegal Risk Assessment:")
        print(json.dumps(risk_assessment, indent=2))
        
        print("\n" + "="*50)
        print("STEP 4: Generate legal summary")
        print("="*50)
        
        legal_summary = await client.generate_legal_summary(
            document=employment_contract,
            audience="non-lawyer",
            max_length=500
        )
        
        print("\nLegal Summary:")
        print(legal_summary)
        
        print("\n" + "="*50)
        print("STEP 5: Compare case precedents")
        print("="*50)
        
        # Case descriptions
        case1 = "AMF Inc. v. Brunswick Corp., 621 F. Supp. 456 (1985) - Court upheld a non-compete agreement restricting an employee from working for competitors for 2 years within a 50-mile radius."
        case2 = "Edwards v. Arthur Andersen LLP, 44 Cal.4th 937 (2008) - California Supreme Court ruled that non-compete agreements in employment contracts are void as unlawful restraints on trade."
        
        case_comparison = await client.compare_legal_precedents(
            cases=[case1, case2],
            issue="Enforceability of non-compete clauses in California"
        )
        
        print("\nCase Precedent Comparison:")
        print(json.dumps(case_comparison, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always disconnect when done
        await client.disconnect()
        print("\nDisconnected from VibeKit")


if __name__ == "__main__":
    asyncio.run(main()) 