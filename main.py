from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the desired webpage
driver.get('https://www.kurtosys.com')

# Locate the tab or menu item by its ID
try:
    tab = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'kurtosys-menu-item-75710'))
    )

    # Create an ActionChains object
    actions = ActionChains(driver)

    # Hover over the element
    actions.move_to_element(tab).perform()

    # Wait for the dropdown to be visible
    dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-elementor-id="75716"]'))
    )

    # Locate all items in the dropdown menu
    items = dropdown.find_elements(By.CSS_SELECTOR, '.elementor-icon-list-item')

    # Check if there are at least three items
    if len(items) >= 3:
        third_item = items[2]
        third_item.click()
    else:
        print("The dropdown does not have at least three items.")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
except TimeoutException:
    print("Timed out waiting for element.")

# Wait for the new page to load and verify the title contains 'White Papers'
try:
    WebDriverWait(driver, 10).until(EC.title_contains("White Papers"))
    print("Title verification successful: The page title contains 'White Papers'.")
except TimeoutException:
    print("Title verification failed: The page title does not contain 'White Papers'.")
    print(f"Current page title: {driver.title}")
    driver.quit()
    exit()

# Wait for the cookie consent button to be visible and click it
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
    )
    cookie_button.click()
    print("Cookies accepted.")
except TimeoutException:
    print("Cookie consent button not found.")

# Wait for the paper titled “UCITS White Paper” to be visible and hover over it
try:
    paper = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "UCITS White Paper")]'))
    )
    actions.move_to_element(paper).perform()
    WebDriverWait(driver, 2).until(lambda driver: True)  # Custom wait with a brief delay
    paper.click()
    print("Hovered over and clicked on the paper titled 'UCITS White Paper'.")
except TimeoutException:
    print("The paper titled 'UCITS White Paper' was not found or not clickable.")
    print(f"Current page URL: {driver.current_url}")
    print(f"Page source snippet: {driver.page_source[:1000]}")  # Print a snippet of the page source for debugging
except NoSuchElementException:
    print("Element was not found on the page.")

# Switch to the iframe if the form is inside one
try:
    iframe = WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe'))
    )
    print("Switched to iframe.")

    # Wait for the form to be present
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pardot-form'))
    )
    print("Form is present on the page.")

    # Enter information into the form
    first_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, '18882_231669pi_18882_231669'))
    )
    last_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, '18882_231671pi_18882_231671'))
    )
    company_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, '18882_231675pi_18882_231675'))
    )
    industry_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, '18882_231677pi_18882_231677'))
    )
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"]'))
    )

    # Submit the form
    first_name_input.send_keys('Alitza')
    last_name_input.send_keys('Botha')
    company_input.send_keys('Company')
    industry_input.send_keys('Technology')
    submit_button.click()

    print("Form submitted. Without Email.")

    # Validate that the email field is required
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'p.error.no-label'))
        )
        print("Error message validated: 'This field is required.'")
        print(f"Error message: {error_message.text}")
    except TimeoutException:
        print("Error message for the email field was not found.")

    # Take a screenshot after submitting the form
    driver.save_screenshot('c:/Users/User-PC/Downloads/form_submission_screenshot.png')
    print("Screenshot taken and saved as 'form_submission_screenshot.png'.")

except TimeoutException:
    print("The form was not found in time.")
except NoSuchElementException as e:
    print(f"An element was not found: {e}")
except StaleElementReferenceException as e:
    print(f"Stale element reference exception: {e}")

driver.quit()