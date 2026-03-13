"""🔍 Debug Script - Check Configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 60)
print("  Configuration Debug Tool")
print("=" * 60)
print()

# Check .env file location
env_paths = [
    Path("../.env"),
    Path("../../.env"),
    Path(".env"),
]

env_file_found = False
for env_path in env_paths:
    if env_path.exists():
        print(f"✅ .env file found: {env_path.absolute()}")
        env_file_found = True
        load_dotenv(env_path)
        break

if not env_file_found:
    print("❌ .env file NOT found!")
    print("\nSearched locations:")
    for p in env_paths:
        print(f"  - {p.absolute()}")
    print("\n⚠️  Create .env file in project root with:")
    print("""
GROQ_API_KEY=your_key_here
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
""")
else:
    print()
    print("-" * 60)
    print("Environment Variables:")
    print("-" * 60)
    
    # Check API Keys
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if groq_key:
        print(f"✅ GROQ_API_KEY: {groq_key[:10]}...{groq_key[-4:]}")
    else:
        print("❌ GROQ_API_KEY: Not set")
    
    if openai_key:
        print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...{openai_key[-4:]}")
    else:
        print("⚠️  OPENAI_API_KEY: Not set")
    
    if openrouter_key:
        print(f"✅ OPENROUTER_API_KEY: {openrouter_key[:10]}...{openrouter_key[-4:]}")
    else:
        print("⚠️  OPENROUTER_API_KEY: Not set")
    
    print()
    
    # Check Provider
    provider = os.getenv("LLM_PROVIDER", "groq")
    print(f"LLM_PROVIDER: {provider}")
    
    # Check Model
    model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    print(f"LLM_MODEL: {model}")
    
    print()
    print("-" * 60)
    print("Validation:")
    print("-" * 60)
    
    # Validate configuration
    if provider == "groq" and not groq_key:
        print("❌ ERROR: LLM_PROVIDER is 'groq' but GROQ_API_KEY is not set!")
    elif provider == "openai" and not openai_key:
        print("❌ ERROR: LLM_PROVIDER is 'openai' but OPENAI_API_KEY is not set!")
    elif provider == "openrouter" and not openrouter_key:
        print("❌ ERROR: LLM_PROVIDER is 'openrouter' but OPENROUTER_API_KEY is not set!")
    else:
        print("✅ Configuration looks good!")
        
        # Test API connection
        print()
        print("-" * 60)
        print("Testing API Connection:")
        print("-" * 60)
        
        try:
            if provider == "groq":
                from groq import Groq
                client = Groq(api_key=groq_key)
                print("✅ Groq client initialized successfully")
                
                # Test API call
                print("Testing API call...")
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say 'test'"}],
                    max_tokens=10
                )
                print(f"✅ API call successful! Response: {response.choices[0].message.content}")
                
            elif provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)
                print("✅ OpenAI client initialized successfully")
                
            elif provider == "openrouter":
                from openai import OpenAI
                client = OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1")
                print("✅ OpenRouter client initialized successfully")
                
        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
            print("\nPossible issues:")
            print("  1. Invalid API key")
            print("  2. No internet connection")
            print("  3. API service down")
            print("  4. Rate limit exceeded")

print()
print("=" * 60)
print()
