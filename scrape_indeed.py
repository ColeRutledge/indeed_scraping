from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import datetime
import re
import pandas as pd
import numpy as np
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
  ('javascript developer', 'Charlotte, NC'),
  ('javascript developer', 'New York, NY'),
  ('javascript developer', 'Austin, TX'),
  ('javascript developer', 'San Francisco, CA'),
  ('javascript developer', 'Washington, DC'),
  ('javascript developer', 'Boston, MA'),
  ('javascript developer', 'Seattle, WA'),
  ('python developer', 'Charlotte, NC'),
  ('python developer', 'New York, NY'),
  ('python developer', 'Austin, TX'),
  ('python developer', 'San Francisco, CA'),
  ('python developer', 'Washington, DC'),
  ('python developer', 'Boston, MA'),
  ('python developer', 'Seattle, WA'),
  ('ruby developer', 'Charlotte, NC'),
  ('ruby developer', 'New York, NY'),
  ('ruby developer', 'Austin, TX'),
  ('ruby developer', 'San Francisco, CA'),
  ('ruby developer', 'Washington, DC'),
  ('ruby developer', 'Boston, MA'),
  ('ruby developer', 'Seattle, WA'),
  ('java developer', 'Charlotte, NC'),
  ('java developer', 'New York, NY'),
  ('java developer', 'Austin, TX'),
  ('java developer', 'San Francisco, CA'),
  ('java developer', 'Washington, DC'),
  ('java developer', 'Boston, MA'),
  ('java developer', 'Seattle, WA'),
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
  last_page = url + f'&start=50000'
  driver.get(last_page)
  # driver.implicitly_wait(4)

  try:
    search_count = driver.find_element_by_id('searchCountPages').text
    re_search = re.search(r'\b\d\d?\b', search_count)
    max_pages = int(re_search[0]) * 10
  except:
    max_pages = 0

  print(f'{datetime.datetime.now()}\t Scraping results for "{search_terms}" from {max_pages // 10} pages in "{search_loc}"')
  # print(max_pages, type(max_pages))


  for i in range(0,max_pages,10):
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

      try:
        sum_div = job.find_elements_by_class_name('summary')[0]
        sum_div.click()
      except:
        try:
          driver.find_element_by_class_name('popover-x-button-close').click()
        except:
          continue
        sum_div.click()

      try:
        driver.switch_to.frame(driver.find_element_by_id('vjs-container-iframe'))
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

  dataframe.to_csv('scraped_data.csv',index=False,encoding='utf-8-sig')
  print(f'{datetime.datetime.now()}\t {search_loc} updated with search: "{search_terms}".\n')

driver.quit()


# FORMATTING AND CREATING NEW COLUMNS ['js_count','python_count','formatted_sal'] WITH PANDAS

# %%
# import pandas as pd
# import numpy as np

# %%
df = pd.read_csv('scraped_data.csv')

# %%
# drops duplicates by finding matches from the combined ['company','title'] columns
df = df.drop_duplicates(subset=['company', 'title'])


# %%
# create ['js_count','python_count'] columns with counts of each showing up in job descriptions
descriptions = df['description']
df['js_count'] = descriptions.str.count(r'[jJ]ava[sS]cript\b')
df['python_count'] = descriptions.str.count(r'[Pp]ython\b')
df['ruby_count'] = descriptions.str.count(r'[Rr]uby\b')
df['java_count'] = descriptions.str.count(r'[Jj]ava\b')
df[['js_count', 'python_count', 'ruby_count', 'java_count']] = \
    df[['js_count', 'python_count', 'ruby_count', 'java_count']].fillna(0).astype(int)


# %%
# recategorizes 'search_terms' for each posting based on highest tech count in description
highest_tcount = df[['js_count', 'python_count', 'ruby_count', 'java_count']].idxmax(axis=1)
mapper = {
    'js_count': 'javascript developer',
    'python_count': 'python developer',
    'ruby_count': 'ruby developer',
    'java_count': 'java developer'
}
df['search_terms'] = highest_tcount.map(lambda x: mapper[x])


# %%
def format_hourly(rate):
    '''Returns annual salaries converted from hourly rates'''
    return rate * 2000 if rate > 0 and rate < 1000 else rate


# %%
# creates the 'formatted_sal' column by finding and formatting high range of scraped salary data
sal_cap_groups = df['salary'].str.extract(r'\d\d\d?,\d\d\d\s-\s\$(\d\d\d?,\d\d\d)|\d\d\s-\s\$(\d\d)')
combined_sal_groups = sal_cap_groups[0].combine_first(sal_cap_groups[1]).str.replace(',', '')
df['formatted_sal'] = combined_sal_groups.fillna(0).astype(int).map(format_hourly).replace(0, np.nan).astype('Int64')
# df_dd['formatted_sal'] = combined.fillna(0).astype(int).map(lambda num: num * 2000 if num > 0 and num < 1000 else num).replace(0, np.nan)


# %%
# groups the data by city and technology and returns average salaries for each
grouped = df.groupby(['search_loc', 'search_terms'])
market_sals = grouped['formatted_sal'].mean().sort_values(ascending=False).astype(int)

# %%
# counts the overall metrics for position counts by tech and amount of total positions per market
pcount_by_tech = df['search_terms'].value_counts()
pcount_by_loc = df['search_loc'].value_counts()

# %%
# creates new dataframe with position counts per market, position % breakdown per market, & overall marketshare of tech by market
pos_metrics_mkt = pd.DataFrame(columns=['pos_counts_mkt', 'pos_pcts_mkt', 'pos_overall_mkt_pct'])
pos_metrics_mkt['pos_pcts_mkt'] = round(df.groupby(['search_loc'])['search_terms'].value_counts(normalize=True) * 100, 2)
pos_metrics_mkt['pos_counts_mkt'] = df.groupby(['search_loc'])['search_terms'].value_counts()
pos_metrics_mkt['pos_overall_mkt_pct'] = round(pos_metrics_mkt['pos_counts_mkt'] / pos_metrics_mkt['pos_counts_mkt'].sum() * 100, 2)
pos_metrics_mkt.reset_index(inplace=True)

# %%
pos_metrics_mkt.to_csv('seed_pos_metrics_mkt.csv', encoding='utf-8-sig')
print('seed_pos_metrics_mkt.csv created.')

# %%
market_sals.to_csv('seed_market_sals.csv', encoding='utf-8-sig')
print('seed_market_sals.csv created.')

# %%
df.to_csv('seed_positions.csv',index=False,encoding='utf-8-sig')
print('seed_positions.csv created.')

print()
print('Scraping complete!')
print()
