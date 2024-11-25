# Yusuf Ismail bin Shukor 20 Nov 2024

import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com'

response = requests.get(url)

# parse the web page using BS4
soup = BeautifulSoup(response.text, 'html5lib')

articles = []

for item in soup.find_all('tr', class_='athing'):
  span = item.find('span', class_='titleline')
  title_tag = span.find('a')
  
  title = title_tag.text
  link = title_tag.get('href', 'N/A')
  
  new_article = {
    'title': title,
    'link': link
  }

  articles.append(new_article)

for index, item in enumerate(soup.find_all('span', class_='score')):
  articles[index]['upvotes'] = item.text

# now that we have some data, let's clean it to be shown in matplotlib
# we want the upvote text to be actual numbers we can represent in a graph/chart

for index, item in enumerate(articles):
  if 'upvotes' in item:
    item['upvotes'] = int(item['upvotes'].replace(' points', ''))
  else: 
    # the article has no upvotes, so we default it to 0
    item['upvotes'] = 0


import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(articles)

# I want to display the bars in different colors depending on the popularity
# red for unpopular, blue for normal, and green for popular
# with red being 0 - 50, blue being 50 - 100, and green being 100+

df['color'] = df['upvotes'].apply(lambda x: 'red' if x < 50 else ('blue' if x < 100 else 'green'))

# given this output, we'll be able to determine if Y Combinator's main page articles
# are very popular or duds by visually inspecting it
plt.bar(df.index, df['upvotes'], tick_label=df.index, color=df['color'])

# labeling
plt.xlabel('Articles')
plt.ylabel('Upvotes')
plt.title('Y Combinator Article Popularity')
plt.legend()

plt.show()