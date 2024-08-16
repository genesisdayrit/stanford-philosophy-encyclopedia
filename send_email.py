import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
from openai import OpenAI
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown2

# Load environment variables from .env file
load_dotenv()

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

        return full_content, title
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None, None

def send_email(subject, message_body, to_email, from_email, password):
    try:
        # Set up the SMTP server
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(from_email, password)

        # Create a message
        msg = MIMEMultipart()

        # Set up the parameters of the message
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add in the message body
        msg.attach(MIMEText(message_body, 'html'))

        # Send the message via the server
        s.send_message(msg)

        s.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred while sending email: {e}")

def call_openai_api(scraped_content):
    # Set up OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    system_prompt = """
        You are an expert in philosophy and have been asked to provide insights on a random entry 
        from the Stanford Encyclopedia of Philosophy.
    """

    prompt = f"""
    The following is a random entry from the Stanford Encyclopedia of Philosophy. 
    Please highlight in bullet points key ideas, people, and concepts as well as the outline of the entry.
    Also give recommendations for further reading or consumption to learn more about the topic(s) covered in the entry
    as well as reflective questions that are good to have conversations about.
    Scraped Content:
    {scraped_content}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    )
    openai_response = completion.choices[0].message.content

    return openai_response

def markdown_to_html(markdown_text):
    # Convert markdown text to HTML
    html = markdown2.markdown(markdown_text)
    return html

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
    scraped_content, entry_tile = scrape_and_prettify_content(random_entry_url)
    
    if scraped_content:
        # Call OpenAI API with the scraped content
        openai_response = call_openai_api(scraped_content)
        
        # Format the response for HTML
        formatted_content = markdown_to_html(f"URL: {random_entry_url}\n\n{openai_response}")
        
        # Send the OpenAI response via email
        email = os.getenv('GMAIL_ACCOUNT')
        password = os.getenv('GMAIL_PASSWORD')
        subject = f"Plato Random Entry: {entry_title}"
        send_email(subject, formatted_content, "genesisdayrit@gmail.com", email, password)
    
    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()
