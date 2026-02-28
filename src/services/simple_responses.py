"""Simple offline responses when API is unavailable."""

def get_simple_response(question: str, context: str = "") -> dict:
    """Generate basic responses without API."""
    
    question_lower = question.lower()
    
    # Extract key information from context if available
    if context:
        # Simple keyword extraction
        words = context.lower().split()
        common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an']
        keywords = [word for word in words if len(word) > 3 and word not in common_words][:10]
        
        if 'summarize' in question_lower or 'summary' in question_lower:
            return {
                "answer": f"📄 **Document Summary**\n\nThis document discusses: {', '.join(keywords[:5])}\n\n*Note: This is a basic summary. Full AI analysis unavailable due to rate limits.*",
                "sources": ["1"],
                "confidence": "low"
            }
        
        elif any(word in question_lower for word in ['what', 'about', 'topic']):
            return {
                "answer": f"📋 **Document Content**\n\nKey topics mentioned: {', '.join(keywords[:7])}\n\n*Note: Limited analysis due to API rate limits.*",
                "sources": ["1"],
                "confidence": "low"
            }
    
    # Generic responses
    return {
        "answer": "⚠️ **Service Temporarily Limited**\n\n🔄 **Status**: API rate limit reached\n⏰ **Wait**: ~11 minutes for reset\n💡 **Tip**: Try again later or upgrade plan\n🔗 **Upgrade**: https://console.groq.com/settings/billing",
        "sources": [],
        "confidence": "low"
    }