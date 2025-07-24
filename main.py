from exa_py import Exa
import os
import json
import requests
from bs4 import BeautifulSoup

exa = Exa(os.getenv'API_KEY')  # Replace with os.getenv('EXA_API_KEY') if using env var

def get_summary_from_url(url, char_limit=300):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        text_content = ' '.join(p.get_text() for p in paragraphs)

        return text_content.strip()[:char_limit] + '...'
    except Exception as e:
        return "Could not retrieve summary."

# Step 1: Get query & optional domain filters
query = input("What do you want to search for? ")
domain_input = input("Enter domain(s) to filter by (comma-separated, or leave blank for no filter): ").strip()

if domain_input:
    # Normalize domain input
    domains = [
        d.strip() if d.startswith("http") else f"https://{d.strip()}"
        for d in domain_input.split(",")
    ]
    response = exa.search(
        query,
        num_results=10,
        type="keyword",
        include_domains=domains,
    )
else:
    response = exa.search(
        query,
        num_results=10,
        type="keyword"
    )

# Step 2: Print results
for result in response.results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    
    # Try using Exa's .text field first, otherwise scrape summary
    summary = result.text if hasattr(result, 'text') and result.text else get_summary_from_url(result.url)
    print(f"Summary: {summary}\n")

# Step 3: Prompt user for save option
save_choice = input("Save results? Enter 'json', 'md' (Markdown), or leave blank to skip: ").strip().lower()
if save_choice not in ('json', 'md'):
    print("No save selected. Done.")
    exit()

# Step 4: Prepare data
results_data = [
    {'title': r.title, 'url': r.url}
    for r in response.results
]

# Step 5: Save to desired format
if save_choice == 'json':
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    print("Results saved to results.json")

elif save_choice == 'md':
    with open('results.md', 'w', encoding='utf-8') as f:
        f.write(f"# Search Results for \"{query}\"\n\n")
        for item in results_data:
            f.write(f"- [{item['title']}]({item['url']})\n")
    print("Results saved to results.md")