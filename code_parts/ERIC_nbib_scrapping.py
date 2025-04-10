import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

articles_per_page = 200
url = "https://eric.ed.gov/?q=title%3A%22interdisciplinary%22+OR+title%3A%22interdisciplinarys%22+OR+title%3A%22interdisciplinarity%22+OR+title%3A%22interdisciplinarities%22+OR+title%3A%22interdisciplinar%22+OR+title%3A%22interdisciplinares%22+OR+title%3A%22interdiscipline%22+OR+title%3A%22interdisciplines%22+OR+title%3A%22multidisciplinary%22+OR+title%3A%22multidisciplinarys%22+OR+title%3A%22multidisciplinarity%22+OR+title%3A%22multidisciplinarities%22+OR+title%3A%22multidisciplinar%22+OR+title%3A%22multidisciplinares%22+OR+title%3A%22multidiscipline%22+OR+title%3A%22multidisciplines%22+OR+title%3A%22pluridisciplinary%22+OR+title%3A%22pluridisciplinarys%22+OR+title%3A%22pluridisciplinarity%22+OR+title%3A%22pluridisciplinarities%22+OR+title%3A%22pluridisciplinar%22+OR+title%3A%22pluridisciplinares%22+OR+title%3A%22pluridiscipline%22+OR+title%3A%22pluridisciplines%22+OR+title%3A%22transdisciplinary%22+OR+title%3A%22transdisciplinarys%22+OR+title%3A%22transdisciplinarity%22+OR+title%3A%22transdisciplinarities%22+OR+title%3A%22transdisciplinar%22+OR+title%3A%22transdisciplinares%22+OR+title%3A%22transdiscipline%22+OR+title%3A%22transdisciplines%22&ft=on"

save_dir = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(save_dir, exist_ok=True)

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", save_dir)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(options=options)
waiter = WebDriverWait(driver, 20, 0.1)  # espera por 20 segundos, com intervalo de 0.1 segundos entre as tentativas
action = ActionChains(driver) 

driver.get(url)

print('Waiting for page to load...')
waiter.until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)
print('Page loaded.')

div_text = driver.find_element(By.ID, "rr0").text.replace(',', '')
match = re.search(r'(?:all\s+)?(\d+)\s+results', div_text)
num = int(match.group(1))
print(f"Number of results: {num}")

export_link = driver.find_element(By.XPATH, '//a[@onclick="if(document.getElementById(\'divExportList\').style.display==\'block\'){document.getElementById(\'divExportList\').style.display=\'none\';}else{document.getElementById(\'divSaveList\').style.display=\'none\';document.getElementById(\'divExportList\').style.display=\'block\';}return(false);"]')
action.move_to_element(export_link).click().perform()

results_to_include = driver.find_element(By.ID, "selectExport")
select = Select(results_to_include)
select.select_by_value(str(articles_per_page))

for start in tqdm(range(1, num + 1, articles_per_page),
                  desc="Downloading files",
                  unit="file"):
    
    input_field = driver.find_element(By.ID, "inputExport")
    input_field.clear()
    input_field.send_keys(str(start))
    
    button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Create file"]')
    button.click()

driver.quit()