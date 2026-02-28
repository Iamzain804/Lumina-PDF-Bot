"""Offline mode responses when API is unavailable."""

def get_offline_response(question: str, context: str = "") -> dict:
    """Generate basic responses without API when rate limited."""
    
    question_lower = question.lower()
    
    # Basic keyword-based responses
    if any(word in question_lower for word in ['summarize', 'summary', 'what is']):
        return {
            "answer": "📄 **Document Summary Available**\n\nThis document contains information that can be analyzed. Due to API rate limits, I cannot provide a detailed summary right now. Please wait 7 minutes for the API to reset, or upgrade your Groq plan for unlimited access.",
            "sources": [],
            "confidence": "low"
        }
    
    elif any(word in question_lower for word in ['main', 'key', 'important', 'topics']):
        return {
            "answer": "🔑 **Key Information**\n\nThe document contains important information that would normally be extracted and analyzed. Currently experiencing API rate limits. Please try again in 7 minutes.",
            "sources": [],
            "confidence": "low"
        }
    
    elif any(word in question_lower for word in ['how', 'why', 'when', 'where']):
        return {
            "answer": "❓ **Question Received**\n\nYour question has been received and would normally be answered using the document content. Due to API rate limits, please wait 7 minutes or upgrade your plan.",
            "sources": [],
            "confidence": "low"
        }
    
    else:
        return {
            "answer": "🤖 **AI Assistant Temporarily Limited**\n\n⏰ **Rate Limit Reached**: Daily token limit exceeded\n⏳ **Wait Time**: ~7 minutes\n💡 **Tip**: Try shorter questions to save tokens\n🔗 **Upgrade**: https://console.groq.com/settings/billing",
            "sources": [],
            "confidence": "low"
        }