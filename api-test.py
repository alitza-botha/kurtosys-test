from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the desired webpage
driver.get('https://www.kurtosys.com')

# Make the API request and measure response time
api_url = 'https://www.kurtosys.com/' 

start_time = time.time()  # Start timing
response = requests.get(api_url)
end_time = time.time()  # End timing

# Calculate response time
response_time = end_time - start_time

try:
    # Assert that the response status is 200
    assert response.status_code == 200, f"Failure: Expected status code 200, but got {response.status_code} instead."
    
    # Assert that the response time is less than 2 seconds
    assert response_time < 2, f"Response time is too long: {response_time:.2f} seconds"
    
    # Assert that the Server header has a value of 'Cloudflare'
    server_header = response.headers.get('Server', '')
    assert 'Cloudflare' in server_header, f"Server header value is not 'Cloudflare': {server_header}"

    print("All checks passed successfully.")
    
except AssertionError as e:
    print(e)

# Close the browser
driver.quit()