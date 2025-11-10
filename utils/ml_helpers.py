"""
ML Helpers for Money Matrix
Provides integration with Gemini API for financial predictions and insights
"""

import os
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from config import Config

def initialize_gemini():
    """Initialize Gemini API with the configured API key"""
    if not GEMINI_AVAILABLE:
        raise ValueError("Google Generative AI library not installed. Run 'pip install google-generativeai'")
    
    api_key = Config.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY not configured in environment variables")
    
    if genai:
        genai.configure(api_key=api_key)
    return genai

def get_financial_insights(user_data, transaction_history):
    """
    Get financial insights using Gemini AI
    
    Args:
        user_data (dict): User profile information
        transaction_history (list): List of transaction records
        
    Returns:
        str: Financial insights and recommendations
    """
    try:
        # Initialize Gemini
        genai_lib = initialize_gemini()
        
        # Create the model
        if genai_lib:
            model = genai_lib.GenerativeModel('gemini-pro')
        else:
            return "Gemini AI not available"
        
        # Prepare the prompt
        prompt = f"""
        As a personal finance advisor, analyze the following user data and provide insights:
        
        User Profile:
        {user_data}
        
        Transaction History:
        {transaction_history}
        
        Please provide:
        1. Spending patterns analysis
        2. Budget recommendations
        3. Potential savings opportunities
        4. Financial health score (1-100)
        5. Personalized advice for improving financial health
        
        Keep the response concise and actionable.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Unable to generate insights at this time. Error: {str(e)}"

def predict_future_spending(transaction_history, months_ahead=3):
    """
    Predict future spending patterns using Gemini AI
    
    Args:
        transaction_history (list): List of transaction records
        months_ahead (int): Number of months to predict ahead
        
    Returns:
        str: Predicted spending patterns and recommendations
    """
    try:
        # Initialize Gemini
        genai_lib = initialize_gemini()
        
        # Create the model
        if genai_lib:
            model = genai_lib.GenerativeModel('gemini-pro')
        else:
            return "Gemini AI not available"
        
        # Prepare the prompt
        prompt = f"""
        Based on the following transaction history, predict spending patterns for the next {months_ahead} months:
        
        Transaction History:
        {transaction_history}
        
        Please provide:
        1. Predicted monthly expenses
        2. Categories likely to see spending increases
        3. Categories where spending might decrease
        4. Recommendations for managing predicted expenses
        5. Alerts for any concerning spending trends
        
        Keep the response concise and focused on actionable insights.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Unable to generate predictions at this time. Error: {str(e)}"

# Example usage function
def example_usage():
    """Example of how to use the ML features"""
    # This would typically be called from your Flask routes
    user_data = {
        "age": 30,
        "income": 5000,
        "dependents": 2
    }
    
    transaction_history = [
        {"date": "2023-01-15", "amount": -150, "category": "Groceries"},
        {"date": "2023-01-20", "amount": -80, "category": "Entertainment"},
        {"date": "2023-02-01", "amount": -1200, "category": "Rent"},
        # ... more transactions
    ]
    
    insights = get_financial_insights(user_data, transaction_history)
    predictions = predict_future_spending(transaction_history)
    
    return {
        "insights": insights,
        "predictions": predictions
    }