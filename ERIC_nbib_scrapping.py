from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
import time
from selenium.webdriver.support.ui import Select
import os

save_dir = os.path.join(os.path.dirname(__file__), "scrap1")
os.makedirs(save_dir, exist_ok=True)

options = webdriver.FirefoxOptions()
options.headless = True

options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", save_dir)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(options=options)

url = "https://eric.ed.gov/?q=%28%22science+teaching%22+OR+%22science+education%22%29+AND+%28interdisciplinary+OR+interdisciplinarity+OR+interdisciplinar+interdiscipline+OR+multidisciplinary+OR+multidisciplinarity+OR+multidisciplinar+OR+multidiscipline+OR+pluridisciplinary+OR+pluridisciplinarity+OR+pluridisciplinar+OR+pluridiscipline+OR+transdisciplinary+OR+transdisciplinarity+OR+transdisciplinar+OR+transdiscipline%29&pr=on"

driver.get(url)

time.sleep(1)

div_text = driver.find_element(By.ID, "rr0").text
print(div_text)

num = div_text.split("of")[-1].split("results")[0].strip().replace(",", "")
num = num.split("all")[-1].strip()

export_link = driver.find_element(By.XPATH, '//a[@onclick="if(document.getElementById(\'divExportList\').style.display==\'block\'){document.getElementById(\'divExportList\').style.display=\'none\';}else{document.getElementById(\'divSaveList\').style.display=\'none\';document.getElementById(\'divExportList\').style.display=\'block\';}return(false);"]')
ActionChains(driver).move_to_element(export_link).click().perform()

results_to_include = driver.find_element(By.ID, "selectExport")
select = Select(results_to_include)
select.select_by_value("200")

for start in range(1, int(num) + 1, 200):
    input_field = driver.find_element(By.ID, "inputExport")
    input_field.clear()
    input_field.send_keys(str(start))
    
    button_y = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Create file"]')
    button_y.click()
    
    time.sleep(1)

time.sleep(1)

driver.quit()