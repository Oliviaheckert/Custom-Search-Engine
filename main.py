from exa_py import Exa

exa = Exa('API_KEY')

// holds repsonse to the input of what we want to search
query = input('Search here: ')

response = exa.search(
	'Best New York bagel',
    num_results=10,
)
