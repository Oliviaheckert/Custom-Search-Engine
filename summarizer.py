import os
import openai

openai.api_key = =os.getend("OPENAI_API_KEY")

def summarize_with_openai(text, max_tokens=150):
    """
    Summarizes the given text using OpenAi's GPT model.
    
    Parameters:
    - text (str): The raw content to summarize
    - max_tokens (int): Maxx output length
    
    Returns:
    - str: AI-generated summary
    """
    try:
    	print = (
        	"Summarize the following webpage content in a concise paragraph:\n\n"
            + text
        )
        
        response = openai.ChatCompletion.create(
        	model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.5
        )
        
        summary = response.choice[0].message['content'].strip()
        return summary
        
    except Exception as e:
    	print("AI summarization failed:", e)
        return "Could not summarize with AI."
        
        
        
        
        
        
        
        
        