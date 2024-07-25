import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Function to scrape and prettify content
def scrape_and_prettify_content(url):
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
        
        # Combine the title and content
        full_content = f"Title: {title}\n\nContent:\n{content}"
        
        # Print the content to the console
        print(full_content)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def main():
    main_url = 'https://plato.stanford.edu/index.html'

    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(main_url)
    
    # Wait for the "Random Entry" link to be clickable and click it
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Random Entry"))).click()
    
    # Wait for the new page to load
    time.sleep(5)
    
    # Get the URL of the new page
    random_entry_url = driver.current_url
    
    # Scrape and prettify the content of the new page
    scrape_and_prettify_content(random_entry_url)
    
    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()
