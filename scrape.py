from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import os


dataframe = pd.DataFrame(columns=[
  'search_terms',
  'search_loc',
  'title',
  'location',
  'company',
  'salary',
  'date',
  'description',
  'link',
])

searches = [
  # ('javascript developer', 'Charlotte, NC'),
  ('javascript developer', 'New York, NY'),
  ('javascript developer', 'Austin, TX'),
  ('javascript developer', 'San Francisco, CA'),
  # ('javascript developer', 'Washington, DC'),
  # ('python developer', 'Charlotte, NC'),
  # ('python developer', 'New York, NY'),
  # ('python developer', 'Austin, TX'),
  # ('python developer', 'San Francisco, CA'),
  # ('python developer', 'Washington, DC'),
]

# config selenium and point to driver
PATH = os.path.dirname(os.path.realpath(__file__))  + '\chromedriver.exe'
driver = webdriver.Chrome(PATH)

for search_terms, search_loc in searches:
  # indeed search
  driver.get('https://www.indeed.com')
  search = driver.find_element_by_name("q")
  search.clear()
  search.send_keys(search_terms)
  search = driver.find_element_by_name("l")
  search.send_keys(Keys.CONTROL + 'a')
  search.send_keys(Keys.DELETE)
  search.send_keys(search_loc)
  search.send_keys(Keys.RETURN)

  url = driver.current_url

  for i in range(0,10,10):
    current_url = url + f'&start={i}'
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
      try:
        date = soup.find(class_='date').text
      except:
        date = 'None'

      sum_div = job.find_elements_by_class_name('summary')[0]
      try:
        sum_div.click()
      except:
        driver.find_element_by_class_name('popover-x-button-close').click()
        sum_div.click()

      driver.switch_to.frame(driver.find_element_by_id('vjs-container-iframe'))

      try:
        job_desc = driver.find_element_by_id('jobDescriptionText').text
      except:
        job_desc = 'None'


      dataframe = dataframe.append({
        'search_terms': search_terms,
        'search_loc': search_loc,
        'title': title,
        'location': location,
        'company': company,
        'salary': salary,
        'date': date,
        'description': job_desc,
        'link': link,
      }, ignore_index=True)

      driver.switch_to.default_content()

  dataframe.to_csv('indeed_seed.csv',index=False,encoding='utf-8-sig')

driver.quit()
