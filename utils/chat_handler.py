import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ChatHandler:
    """Handle chat interactions using Groq API"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.3-70b-versatile"
        else:
            self.client = None
    
    def get_response(self, user_message, context=""):
        """Get AI response for user query"""
        
        if not self.client:
            return "Please add your GROQ_API_KEY to the .env file to enable AI responses."
        
        system_prompt = """You are Finbot, an expert Indian investment advisor. 
        You help users with investment advice for Indian markets (NSE/BSE), 
        mutual funds, debt funds, and bonds. Provide clear, practical advice 
        tailored to Indian investors. Be concise and helpful."""
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            if context:
                messages.insert(1, {"role": "assistant", "content": f"Context: {context}"})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error getting response: {str(e)}"
