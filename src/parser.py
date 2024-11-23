from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import hues
import json
import chromedriver_autoinstaller
hues.log("Auto-install")
chromedriver_autoinstaller.install() 
driver = webdriver.Chrome()
hues.log("")


def find_inn(inn):
    """
    Fetches details about an organization using its INN from the EGRUL website.
    
    Args:
        inn (str): The INN (Taxpayer Identification Number) of the organization to search for.
    
    Returns:
        str: A JSON string containing the search results.
    """
    results = []  
    try:
        driver.get("https://egrul.nalog.ru/index.html")
        time.sleep(3)
        
        search_input = driver.find_element(By.ID, "query")
        search_input.send_keys(inn)
        search_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Allow time for search results to load

        rows = driver.find_elements(By.CSS_SELECTOR, ".res-row")
        
        for row in rows:
            try:
                title_element = row.find_element(By.CSS_SELECTOR, ".res-caption a")
                organization_title = title_element.get_attribute("title")  # Organization name
                organization_link = title_element.get_attribute("href")  # Link to more details
                
                details_element = row.find_element(By.CSS_SELECTOR, ".res-text")
                organization_details = details_element.text  # Additional details
                
                results.append({
                    "title": organization_title,
                    "details": organization_details,
                    "link": organization_link if organization_link else None
                })
            except Exception as row_error:
                print(f"Error processing a row: {row_error}")
    
    except Exception as e:
        print(f"Error fetching data: {e}")
    
    finally:
        driver.quit()
    
    return json.dumps(results, ensure_ascii=False, indent=4)
