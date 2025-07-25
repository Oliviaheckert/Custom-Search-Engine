from exa_py import Exa
import os
import json
import requests
from bs4 import BeautifulSoup
from summarizer import summarize_with_openai

# ✅ --- Constants ---
NUM_RESULTS = 10
SCRAPE_CHAR_LIMIT = 1000

# ✅ --- API Key Setup ---
EXA_API_KEY = os.getenv('EXA_API_KEY')
if not EXA_API_KEY:
    raise ValueError("❌ Missing EXA_API_KEY. Set it in your environment variables.")
exa = Exa(EXA_API_KEY)


# ✅ --- Helper Function ---
def get_summary_from_url(url, char_limit=300):
    """Scrapes a web page and returns the first `char_limit` characters of paragraph text."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        text_content = ' '.join(p.get_text() for p in paragraphs)

        return text_content.strip()[:char_limit] + '...'
    except Exception as e:
        print(f"⚠️ Could not retrieve summary for {url}: {e}")
        return "Could not retrieve summary."


# ✅ --- Main Function ---
def main():
    # Step 1: Get query & optional domain filters
    query = input("🔎 What do you want to search for? ")
    domain_input = input("🌐 Enter domain(s) to filter by (comma-separated, or leave blank for no filter): ").strip()

    # Ask if AI should summarize (✅ asked once, not inside the loop)
    use_ai_summary = input("🤖 Use AI to summarize results? (yes/no): ").strip().lower() == 'yes'

    try:
        # Handle search with or without domain filters
        if domain_input:
            domains = [
                d.strip() if d.startswith("http") else f"https://{d.strip()}"
                for d in domain_input.split(",")
            ]
            response = exa.search(query, num_results=NUM_RESULTS, type="keyword", include_domains=domains)
        else:
            response = exa.search(query, num_results=NUM_RESULTS, type="keyword")

    except Exception as e:
        print("❌ Search failed:", e)
        return

    # Step 2: Print results
    results_data = []
    for result in response.results:
        print(f"\n📄 Title: {result.title}")
        print(f"🔗 URL: {result.url}")

        # Use Exa’s text if available, else scrape
        if hasattr(result, 'text') and result.text:
            raw_content = result.text
        else:
            raw_content = get_summary_from_url(result.url, char_limit=SCRAPE_CHAR_LIMIT)

        # Summarize using AI (truncate long content first for cost/efficiency)
        if use_ai_summary:
            trimmed_content = raw_content[:2000]
            summary = summarize_with_openai(trimmed_content)
        else:
            summary = raw_content.strip()[:300] + "..."

        print(f"📝 Summary: {summary}")

        # Add to results list (✅ includes summary for saving)
        results_data.append({
            'title': result.title,
            'url': result.url,
            'summary': summary
        })

    # Step 3: Prompt user for save option
    save_choice = input("\n💾 Save results? Enter 'json', 'md' (Markdown), or leave blank to skip: ").strip().lower()
    if save_choice not in ('json', 'md'):
        print("✅ No save selected. Done.")
        return

    # Step 4: Save to desired format
    if save_choice == 'json':
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        print("✅ Results saved to results.json")

    elif save_choice == 'md':
        with open('results.md', 'w', encoding='utf-8') as f:
            f.write(f"# 🔎 Search Results for \"{query}\"\n\n")
            for item in results_data:
                f.write(f"## {item['title']}\n")
                f.write(f"[{item['url']}]({item['url']})\n\n")
                f.write(f"**Summary:** {item['summary']}\n\n")
        print("✅ Results saved to results.md")


# ✅ Only run main() if this file is run directly (best practice)
if __name__ == "__main__":
    main()