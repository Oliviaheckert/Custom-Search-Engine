from exa_py import Exa

exa = Exa('API_KEY')

# Ask user for search query
query = input("What do you want to search for? ")

# Let user input domains, optional
domain_input = input("Enter domain(s) to filterby (comma-separated, or leave blank for no filter): ").strip()

# Process domains into a list, or None
if domain_input:
  # Make sure it starts with 'https://www.' if needed (basic normalization)
  domains = [d.strip() if d.startswith("http") else f"https://{d.strip()}" for d in domain_input.split(",")]
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

# Print results
for result in response.results:
  print(f"Title: {result.title}")
  print(f"URL: {result.url}")
  print()