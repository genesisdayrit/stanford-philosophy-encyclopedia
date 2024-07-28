# stanford-philosophy-encyclopedia random entry scraper

## 1. Introduction

### 1.1 Purpose

The purpose of this README is to outline the design, implementation, and usage of a Python script that uses Selenium to interact with a web page, specifically to click on a "Random Entry" link on the Stanford Encyclopedia of Philosophy (SEP) main page, scrape the resulting page, and format the content for display in the console.

### 1.2 Scope

This script is designed to perform the following tasks:
- Navigate to the SEP main page.
- Click on the "Random Entry" link.
- Scrape the content of the resulting page.
- Format the content and print it to the console.

## 2. Design

### 2.1 Overview

The script uses Selenium WebDriver to automate the browser interaction, Requests to fetch the HTML content, and BeautifulSoup to parse and format the HTML content.

### 2.2 Components

#### 2.2.1 Libraries Used

- requests: To send HTTP requests.
- selenium: To control the web browser.
- webdriver_manager: To manage the WebDriver binaries.
- bs4 (BeautifulSoup): To parse and format the HTML content.
- time: To add delays for page loading.

#### 2.2.2 Functions

- scrape_and_format_content(url): Fetches and formats content from a given URL.
- main(): The main function to set up the WebDriver, navigate to the SEP main page, click the "Random Entry" link, and call the scraping function.

### 2.3 Detailed Design

#### 2.3.1 scrape_and_format_content(url)

- Input: URL of the webpage to scrape.
- Process:
  1. Sends a GET request to the provided URL.
  2. Checks if the request was successful.
  3. Parses the HTML content using BeautifulSoup.
  4. Extracts the title from the h1 tag.
  5. Extracts the main content from the div with id='main-text'.
  6. Combines the title and content into a formatted string.
  7. Prints the formatted content to the console.
- Output: None (prints content to the console).

#### 2.3.2 main()

- Input: None
- Process:
  1. Sets the URL of the SEP main page.
  2. Sets up the Selenium WebDriver.
  3. Navigates to the SEP main page.
  4. Waits for the "Random Entry" link to be clickable and clicks it.
  5. Waits for the new page to load.
  6. Retrieves the URL of the new page.
  7. Calls scrape_and_format_content(url) with the new page URL.
  8. Closes the WebDriver.
- Output: None (calls the scraping function and prints content).

## 3. Implementation

### 3.1 Prerequisites

- Python 3.x
- Required Python libraries: requests, selenium, beautifulsoup4, webdriver_manager

### 3.2 Installation

Install the required libraries using pip:

```sh
pip install requests selenium beautifulsoup4 webdriver_manager
```

### 3.3 Script

```python
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Function to scrape and format content
def scrape_and_format_content(url):
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
    
    # Scrape and format the content of the new page
    scrape_and_format_content(random_entry_url)
    
    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()
```

## 4. Usage

1. Ensure all prerequisites are met and required libraries are installed.
2. Run the script using a Python interpreter:

```sh
python scrape_random_entry.py
```

3. The script will navigate to the SEP main page, click the "Random Entry" link, scrape the resulting page, and print the formatted content to the console.

## 5. Future Enhancements

- Add error handling for Selenium WebDriver actions.
- Implement logging for better traceability.
- Enhance the script to handle different page structures if necessary.
- Extend the functionality to save the scraped content to a file.

## 6. Conclusion

This README provides a detailed overview of the web scraping and content formatting script. The script automates the process of navigating to a webpage, interacting with elements, and extracting useful information for display in the console.
