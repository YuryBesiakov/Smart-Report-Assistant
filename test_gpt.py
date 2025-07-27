#!/usr/bin/env python3
"""
test_gpt_integration.py
-----------------------

Test script to validate GPT integration functionality.
Run this to test if your OpenAI API key is working correctly.
"""

import os
import sys
sys.path.append('app')

from report_generator import generate_summary_gpt, read_csv
from dotenv import load_dotenv

def test_gpt_integration():
    """Test the GPT integration with the example dataset."""
    print("🧪 Testing GPT Integration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is configured
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ No valid OpenAI API key found in .env file")
        print("📝 Please set up your API key following GPT_SETUP.md")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test with example data
    try:
        print("📊 Loading example dataset...")
        df = read_csv('data/beispiel.csv')
        print(f"✅ Dataset loaded: {len(df)} records")
        
        print("🤖 Testing GPT analysis...")
        result = generate_summary_gpt(df)
        
        print("✅ GPT Analysis Results:")
        print("-" * 50)
        print("📋 Summary:")
        print(result.get('summary', 'No summary generated'))
        print("\n💡 Recommendations:")
        print(result.get('recommendations', 'No recommendations generated'))
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during GPT analysis: {e}")
        return False

if __name__ == "__main__":
    success = test_gpt_integration()
    sys.exit(0 if success else 1)
