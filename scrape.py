from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

# PATH = r"C:\Users\Cole Rutledge\scraping\chromedriver.exe"
# PATH = "/usr/bin/chromedriver"
PATH = "/opt/selenium/chromedriver-84.0.4147.30"
driver = webdriver.Chrome(PATH)
dataframe = pd.DataFrame(columns=['Title','Location','Company','Salary','Description'])
# driver.get('https://www.indeed.com/jobs?q=react%20developer&l=Charlotte%2C%20NC&ts=1597684854766&rq=1&rsIdx=0&vjk=08da742a5c8fc094')
driver.get('https://www.indeed.com')
# print(driver.title)

search = driver.find_element_by_name("q")
search.clear()
search.send_keys('javascript developer')
time.sleep(2)
search = driver.find_element_by_name("l")
search.send_keys(Keys.CONTROL + 'a')
search.send_keys(Keys.DELETE)
# search.clear()
search.send_keys('28211')
search.send_keys(Keys.RETURN)

time.sleep(1)

# driver.find_element_by_class_name('popover-x-button-close').click()

# time.sleep(2)
url = driver.current_url
# print(url)

for i in range(0,100,10):
  current_url = url+f'&start={i}'
  driver.get(current_url)
  driver.implicitly_wait(4)


  all_jobs = driver.find_elements_by_class_name('result')

  for job in all_jobs:

    result_html = job.get_attribute('innerHTML')
    soup_result = soup(result_html, 'html.parser')

    try:
      title = soup_result.find('a', class_='jobtitle').text.replace('\n','')
      print(title)
    except:
      title = 'None'
    try:
      location = soup_result.find(class_='location').text
      # print(location)
    except:
      location = 'None'
    try:
      company = soup_result.find(class_='company').text.replace('\n','').strip()
      print(company)
    except:
      company = 'None'
    try:
      salary = soup_result.find(class_='salary').text.replace('\n','').strip()
      # print(salary)
    except:
      salary = 'None'

    sum_div = job.find_elements_by_class_name('summary')[0]
    try:
      sum_div.click()
    except:
      driver.find_element_by_class_name('popover-x-button-close').click()
      sum_div.click()
    time.sleep(2)
    # job_desc = driver.find_element_by_id('jobDescriptionText').text
    dataframe = dataframe.append({
      'Title': title,
      'Location': location,
      'Company': company,
      'Salary': salary,
      'Description': None,
    }, ignore_index=True)

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


# sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
# sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
# CMD [ "-p", '4444:4444', '-v', '/dev/shm:/dev/shm' ]
