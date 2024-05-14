import requests
from bs4 import BeautifulSoup

# Function to scrape content
def scrape_sep_article(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title of the article
        title = soup.find('h1').get_text()
        
        # Extract the main content
        content = soup.find('div', {'id': 'main-text'}).get_text(separator='\n')
        
        # Print the title and content
        print(f"Title: {title}\n")
        print(f"Content:\n{content}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# URL of the SEP article
url = 'https://plato.stanford.edu/entries/plato-cratylus/'

# Call the function with the URL
scrape_sep_article(url)
