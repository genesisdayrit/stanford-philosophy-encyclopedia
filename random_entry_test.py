from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Update this path to your chromedriver location
webdriver_service = Service('/Users/Genesis/Downloads/chromedriver_mac_arm64/chromedriver')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Function to scrape content
def scrape_random_entry():
    try:
        # Open the Stanford Encyclopedia of Philosophy main page
        driver.get('https://plato.stanford.edu/')
        
        # Wait for the Random Entry button to be clickable
        random_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Random Entry"))
        )
        
        # Click the Random Entry button
        random_button.click()
        
        # Wait for the new page to load
        time.sleep(3)  # Adjust sleep time if necessary
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract the current URL
        current_url = driver.current_url
        
        # Extract the title of the article
        title = soup.find('h1').get_text()
        
        # Extract the main content
        content = soup.find('div', {'id': 'main-text'}).get_text(separator='\n')
        
        # Print the URL, title, and content
        print(f"URL: {current_url}\n")
        print(f"Title: {title}\n")
        print(f"Content:\n{content}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()

# Call the function to scrape a random entry
scrape_random_entry()
