import os
from pathlib import Path

def create_env_file():
    print("========================================")
    print("   📄 PDF Chatbot - API Config Helper")
    print("========================================\n")
    
    env_path = Path(".env")
    
    if env_path.exists():
        confirm = input(".env file pehle se mojood hai. Kya aap ise overwrite karna chahte hain? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    provider = input("LLM Provider select karen (1: OpenRouter (Default), 2: Groq, 3: OpenAI): ") or "1"
    
    mapping = {"1": "openrouter", "2": "groq", "3": "openai"}
    llm_provider = mapping.get(provider, "openrouter")
    
    api_key = input(f"Apni {llm_provider.upper()} API Key enter karen: ").strip()
    
    if not api_key:
        print("Error: API Key zaroori hai!")
        return

    env_content = f"""# PDF Chatbot - Environment Configuration
LLM_PROVIDER={llm_provider}
{llm_provider.upper()}_API_KEY={api_key}
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
        
    print(f"\n✅ .env file successfully create ho gayi hai!")
    print(f"✅ Provider set to: {llm_provider}")
    print("\nAb aap project run kar sakte hain:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    create_env_file()
