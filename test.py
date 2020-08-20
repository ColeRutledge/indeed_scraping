from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

dataframe = pd.DataFrame(columns=['Title','Location','Company','Salary','Description','Link'])

# config selenium and point to driver
PATH = r"C:\Users\Cole Rutledge\scraping\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# indeed search
driver.get('https://www.indeed.com')
search = driver.find_element_by_name("q")
search.clear()
search.send_keys('javascript engineer')
search = driver.find_element_by_name("l")
search.send_keys(Keys.CONTROL + 'a')
search.send_keys(Keys.DELETE)
search.send_keys('28211')
search.send_keys(Keys.RETURN)

# driver.find_element_by_class_name('popover-x-button-close').click()

url = driver.current_url

for i in range(0,300,10):
  current_url = url+f'&start={i}'
  driver.get(current_url)
  driver.implicitly_wait(4)


  for job in driver.find_elements_by_class_name('result'):

    soup = bs(job.get_attribute('innerHTML'), 'html.parser')

    try:
      title = soup.find('a', class_='jobtitle').text.replace('\n','').strip()
      # print(title)
    except:
      title = 'None'

    try:
      link = 'http://www.indeed.com' + soup.find('a', class_='jobtitle')['href']
      # print(link)
      # print()
    except:
      link = 'None'

    try:
      location = soup.find(class_='location').text
      # print(location)
      # print()
    except:
      location = 'None'
    try:
      company = soup.find(class_='company').text.replace('\n','').strip()
      # print(company)
      # print()
    except:
      company = 'None'
    try:
      salary = soup.find(class_='salary').text.replace('\n','').strip()
      # print(salary)
      # print()
    except:
      salary = 'None'

    sum_div = job.find_elements_by_class_name('summary')[0]
    # sum_div = job.find_element_by_xpath('./div[3]')
    try:
      sum_div.click()
    except:
      driver.find_element_by_class_name('popover-x-button-close').click()
      sum_div.click()

    # time.sleep(2)
    driver.switch_to.frame(driver.find_element_by_id('vjs-container-iframe'))
    job_desc = driver.find_element_by_id('jobDescriptionText').text
    # job_desc = driver.find_element_by_id('vjs-desc').text
    # print(job_desc)
    # print()

    dataframe = dataframe.append({
      'Title': title,
      'Location': location,
      'Company': company,
      'Salary': salary,
      'Description': job_desc,
      'Link': link,
    }, ignore_index=True)

    # driver.switch_to.window(driver.window_handles.last)
    driver.switch_to.default_content()

dataframe.to_csv('indeed_test.csv', index=False)


# for i in driver.find_elements_by_xpath("//a[@title]"):
#   print(i.get_attribute('title'))

# for i in driver.find_elements_by_class_name('jobtitle'):
#   print(i.get_attribute('title'))

# for i in driver.find_elements_by_class_name('recJobLoc'):
#   print(i.get_attribute('data-rc-loc'))

# for i in driver.find_elements_by_class_name('summary'):
#   print(i.get_attribute('title'))
# summaries = driver.find_elements_by_class_name('summary')
# for i in summaries:


# for i in driver.find_elements_by_xpath('//div//li'):
#   # print(i.get_attribute('innerHTML'))
#   print(i.text)


driver.quit()
