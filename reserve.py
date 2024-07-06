import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load login credentials from auth.json
with open('auth.json') as f:
    auth = json.load(f)
    username = auth['username']
    password = auth['password']

# Replace with the path to your updated ChromeDriver
driver_path = 'chromedriver-mac-arm64/chromedriver'

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

def login():
    """Log into the Club Locker website."""
    driver.get('https://clublocker.com/login')
    try:
        # Enter username
        user_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        user_field.send_keys(username)
        logging.info("Username entered.")

        # Enter password
        pass_field = driver.find_element(By.NAME, 'password')
        pass_field.send_keys(password)
        logging.info("Password entered.")

        # Submit the login form
        pass_field.send_keys(Keys.RETURN)
        logging.info("Login form submitted.")
        
        # Ensure login was successful
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Logout")]'))
        )
        logging.info("Logged in successfully.")
    except TimeoutException:
        logging.error("Login fields not found!")
        driver.quit()
        return False
    except NoSuchElementException:
        logging.error("Login failed!")
        driver.quit()
        return False
    return True

def navigate_to_reservations():
    """Navigate to the reservations page and filter for tennis courts."""
    driver.get('https://clublocker.com/organizations/13911/reservations/')
    try:
        # Wait for the reservation grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'reservation-grid'))
        )
        logging.info("Reservation grid loaded.")

        # Click the "Tennis" button to filter courts
        tennis_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[./span[text()=" Tennis "]]'))
        )
        tennis_button.click()
        logging.info("Tennis button clicked.")
    except TimeoutException:
        logging.error("Reservation grid or Tennis button not loaded!")
        driver.quit()
        return False
    return True

def move_days_ahead(days):
    """Move ahead by a specified number of days on the reservation grid."""
    try:
        for _ in range(days):
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.mat-icon-button svg[data-icon="angle-right"]'))
            )
            next_button.click()
            time.sleep(1)  # Short delay to allow the page to load
        logging.info(f"Moved {days} days ahead.")
    except TimeoutException:
        logging.error("Next day button not found!")
        driver.quit()
        return False
    except NoSuchElementException:
        logging.error("Next day button not found!")
        driver.quit()
        return False
    return True

def reserve_court():
    """Reserve a tennis court at the desired time slot."""
    try:
        # Find all available slots
        time_slots = driver.find_elements(By.XPATH, '//div[@class="slot open" and @title]')
        logging.info(f"Found {len(time_slots)} time slots.")

        # Extract and sort time slots
        slots_with_times = [(slot, slot.get_attribute('title')) for slot in time_slots]
        sorted_slots = sorted(slots_with_times, key=lambda x: time.strptime(x[1].split('-')[0].strip(), "%I:%M %p"), reverse=True)

        # Print sorted time slots for inspection
        logging.info("Sorted time slots:")
        for slot, time_text in sorted_slots:
            logging.info(f"Time slot: {time_text}")

        # Try to reserve slots after 6 PM first
        for slot, time_text in sorted_slots:
            if any(t in time_text for t in ['6:00 PM', '7:00 PM', '8:00 PM']):
                try:
                    slot.click()
                    logging.info(f"Selected time slot: {time_text}")

                    # Confirm reservation
                    confirm_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//button[@mat-raised-button and .//span[text()=" Save "]]'))
                    )
                    confirm_button.click()
                    logging.info("Reservation confirmed.")
                    time.sleep(10)  # Wait before closing
                    return True
                except (TimeoutException, NoSuchElementException):
                    logging.error(f"Confirmation button not found for slot: {time_text}")

        # If no slots after 6 PM, try earlier slots
        for slot, time_text in sorted_slots:
            if all(t not in time_text for t in ['6:00 PM', '7:00 PM', '8:00 PM']):
                try:
                    slot.click()
                    logging.info(f"Selected time slot: {time_text}")

                    # Confirm reservation
                    confirm_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//button[@mat-raised-button and .//span[text()=" Save "]]'))
                    )
                    confirm_button.click()
                    logging.info("Reservation confirmed.")
                    time.sleep(10)  # Wait before closing
                    return True
                except (TimeoutException, NoSuchElementException):
                    logging.error(f"Confirmation button not found for slot: {time_text}")

        logging.info("No available slots were successfully reserved.")
    except (TimeoutException, NoSuchElementException):
        logging.error("Time slot not found!")
    finally:
        driver.quit()
    return False

def main():
    """Main function to log in, navigate to reservations, move days ahead, and reserve a court."""
    if login():
        if navigate_to_reservations():
            if move_days_ahead(7):
                if reserve_court():
                    logging.info("Court reserved successfully!")
                else:
                    logging.info("Court reservation failed.")
            else:
                logging.error("Failed to move days ahead.")
        else:
            logging.error("Failed to navigate to reservations.")
    else:
        logging.error("Login failed. Exiting.")

if __name__ == "__main__":
    main()