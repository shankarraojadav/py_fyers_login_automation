from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open Google
driver.get("https://www.google.com/")

# Assert that "Google" is in the title (instead of "Python")
assert "Google" in driver.title

# Find the search box using the name attribute and clear it
elem = driver.find_element(By.NAME, "q")
elem.clear()

# Send the search query "pycon" and hit ENTER
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

# Assert that there are results (ensure "No results found." is not on the page)
assert "No results found." not in driver.page_source

# Close the browser
driver.close()
