import os
import openai

# ✅ Set up your API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_with_openai(text, max_tokens=150):
    """
    Summarizes the given text using OpenAI's GPT model.

    Parameters:
    - text (str): The raw content to summarize.
    - max_tokens (int): Max output length.

    Returns:
    - str: AI-generated summary or fallback message.
    """
    try:
        prompt = (
            "Summarize the following webpage content in a concise, clear paragraph:\n\n"
            + text
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.5
        )

        summary = response.choices[0].message['content'].strip()
        return summary

    except Exception as e:
        print("⚠️ AI summarization failed:", e)
        return "Could not summarize with AI."