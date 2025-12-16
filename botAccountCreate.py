# ================= INSTAGRAM SIGNUP BOT (STABLE DESKTOP VERSION) =================

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import random
import logging

import accountInfoGenerator as account
import fakeMail as email
import getVerifCode as verifiCode

# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ================= HELPERS =================
def human_sleep(a=1.5, b=3.5):
    time.sleep(random.uniform(a, b))

def random_type(el, text):
    for c in text:
        el.send_keys(c)
        time.sleep(random.uniform(0.06, 0.14))

def wait_and_click_submit():
    wait = WebDriverWait(driver, 30)
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "form button[type='submit']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    human_sleep(1, 2)
    btn.click()

def force_dob(year="1998"):
    wait = WebDriverWait(driver, 30)
    selects = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
    if len(selects) >= 3:
        Select(selects[0]).select_by_index(random.randint(1, 12))
        Select(selects[1]).select_by_index(random.randint(1, 28))
        Select(selects[2]).select_by_visible_text(year)
        logging.info("✅ DOB selected")

# ================= CHROME SETUP (NO HEADLESS) =================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(60)
driver.implicitly_wait(5)

# ================= ACCOUNT DATA =================
fake_email = email.getFakeMail()
if isinstance(fake_email, list):
    fake_email = fake_email[0]

full_name = account.generatingName()
username = account.username()
password = account.generatePassword()

logging.info(f"Email: {fake_email}")
logging.info(f"Username: {username}")

# ================= SIGNUP =================
driver.get("https://www.instagram.com/accounts/emailsignup/")
human_sleep(6, 9)

random_type(driver.find_element(By.NAME, "emailOrPhone"), fake_email)
human_sleep()
random_type(driver.find_element(By.NAME, "fullName"), full_name)
human_sleep()
random_type(driver.find_element(By.NAME, "username"), username)
driver.find_element(By.NAME, "username").send_keys(Keys.TAB)

human_sleep(3, 5)
random_type(driver.find_element(By.NAME, "password"), password)
human_sleep(2, 4)

wait_and_click_submit()
human_sleep(6, 9)

# ================= DOB =================
force_dob("1998")

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
).click()

human_sleep(6, 8)

# ================= EMAIL VERIFICATION =================
mail_name, domain = fake_email.split("@")

try:
    code = verifiCode.getInstVeriCode(mail_name, domain, driver)
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "email_confirmation_code"))
    )
    input_box.send_keys(code)
    input_box.send_keys(Keys.ENTER)
    logging.info("✅ OTP auto-filled")
except Exception:
    logging.warning("⚠ Auto OTP failed — enter manually in browser")

# ================= NOTIFICATIONS =================
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))
    ).click()
except:
    pass

logging.info("🟢 Script finished — browser left open")
time.sleep(30)
