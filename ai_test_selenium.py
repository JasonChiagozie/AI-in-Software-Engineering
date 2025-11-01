from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.google.com")
assert "Google" in driver.title
print("✅ Test Passed: Google title verified!")

driver.quit()