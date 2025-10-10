import requests

def fetch_data(url):
  """Fetches data from a given URL."""
  response = requests.get(url)
  response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
  return response.json()