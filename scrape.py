from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

searches = [
  ('javascript developer', 'Charlotte, NC'),
  ('javascript developer', 'New York, NY'),
  ('javascript developer', 'Austin, TX'),
  ('javascript developer', 'San Francisco, CA'),
  ('javascript developer', 'Washington, DC')
]
dataframe = pd.DataFrame(columns=['Title','Location','Company','Salary','Description','Link'])

# config selenium and point to driver
PATH = r"C:\Users\Cole Rutledge\scraping\chromedriver.exe"
driver = webdriver.Chrome(PATH)

for keywords, location in searches:
  # indeed search
  driver.get('https://www.indeed.com')
  search = driver.find_element_by_name("q")
  search.clear()
  search.send_keys(keywords)
  search = driver.find_element_by_name("l")
  search.send_keys(Keys.CONTROL + 'a')
  search.send_keys(Keys.DELETE)
  search.send_keys(location)
  search.send_keys(Keys.RETURN)

  url = driver.current_url

  for i in range(0,10,10):
    current_url = url+f'&start={i}'
    driver.get(current_url)
    driver.implicitly_wait(4)

    for job in driver.find_elements_by_class_name('result'):

      soup = bs(job.get_attribute('innerHTML'), 'html.parser')

      try:
        title = soup.find('a', class_='jobtitle').text.replace('\n','').strip()
      except:
        title = 'None'

      try:
        link = 'http://www.indeed.com' + soup.find('a', class_='jobtitle')['href']
      except:
        link = 'None'

      try:
        location = soup.find(class_='location').text
      except:
        location = 'None'
      try:
        company = soup.find(class_='company').text.replace('\n','').strip()
      except:
        company = 'None'
      try:
        salary = soup.find(class_='salary').text.replace('\n','').strip()
      except:
        salary = 'None'

      sum_div = job.find_elements_by_class_name('summary')[0]
      try:
        sum_div.click()
      except:
        driver.find_element_by_class_name('popover-x-button-close').click()
        sum_div.click()

      driver.switch_to.frame(driver.find_element_by_id('vjs-container-iframe'))
      job_desc = driver.find_element_by_id('jobDescriptionText').text

      dataframe = dataframe.append({
        'Title': title,
        'Location': location,
        'Company': company,
        'Salary': salary,
        'Description': job_desc,
        'Link': link,
      }, ignore_index=True)

      driver.switch_to.default_content()

dataframe.to_csv('indeed_test.csv', index=False)


driver.quit()
