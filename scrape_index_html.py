import requests
import pyperclip

# Function to scrape raw HTML content
def scrape_sep_main_page(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the raw HTML content
        raw_html = response.text
        
        # Copy the raw HTML content to the clipboard
        pyperclip.copy(raw_html)
        
        print("Raw HTML content copied to clipboard successfully.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# URL of the SEP main page
url = 'https://plato.stanford.edu/index.html'

# Call the function with the URL
scrape_sep_main_page(url)
