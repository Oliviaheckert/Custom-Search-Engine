from exa_py import Exa

exa = Exa('API_KEY')

# holds repsonse to the input of what we want to search
query = input('Search here: ')

response = exa.search(
	query,
  num_results=10,
  type='keyword',
  include_domains=['https://www.tiktok.com'],
)

for result in response.results:
  print(f'Title: {result.title}')
  print(f'URL: {result.url}')
  print()