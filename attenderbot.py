from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# MEETING LINK (Replace with your actual meeting link)
MEETING_LINK = "https://meet.google.com/your-meeting-link"
HOST_NAME = "Host Name"  # Replace with the actual host's name

# SETUP BROWSER
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# OPEN BROWSER
driver = webdriver.Chrome(options=options)

try:
    # GO TO MEETING LINK
    driver.get(MEETING_LINK)
    print("Opened meeting link.")

    # TURN OFF CAMERA AND MICROPHONE
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Turn off camera"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Turn off microphone"]'))).click()
    print("Turned off camera and microphone.")

    # CLICK "JOIN NOW" BUTTON
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Join now')]"))).click()
    print("Joined the meeting!")

    # WAIT UNTIL HOST LEAVES (Smart Detection)
    print("Waiting for host to leave...")
    while True:
        try:
            # Check if "Host has left" message appears
            host_left_message = driver.find_elements(By.XPATH, "//div[contains(text(), 'host has left')]")
            if host_left_message:
                print("Host has left. Exiting meeting...")
                break
        except:
            pass

        try:
            # Open participant list
            participants_button = driver.find_element(By.XPATH, "//div[@aria-label='Show everyone']")
            participants_button.click()
            time.sleep(2)

            # Check if host name is missing
            host_in_list = driver.find_elements(By.XPATH, f"//div[contains(text(), '{HOST_NAME}')]")
            if not host_in_list:
                print("Host has left. Exiting meeting...")
                break
        except:
            pass  # If participant list isn't available, keep checking

        time.sleep(10)  # Check every 10 seconds

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # EXIT MEETING
    driver.quit()
    print("Left the meeting!")
