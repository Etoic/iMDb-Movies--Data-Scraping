#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from bs4 import BeautifulSoup
import requests
import re


# In[3]:


### Download Data

url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')


# In[4]:


### Get Data

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]


# In[5]:


### Store the Data

# create a empty list for storing
# movie information
list = []
 
# Iterating over movies to extract
# each movie's details
for index in range(0, len(movies)):
   
    # Separating  movie into: 'place',
    # 'title', 'year'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
     
    data = {"movie_title": movie_title,
            "year": year,
            "place": place,
            "star_cast": crew[index],
            "rating": ratings[index],
            "vote": votes[index],
            "link": links[index]}
    list.append(data)


# In[6]:


# Print
for movie in list:
    print(movie['place'], ',', movie['movie_title'], ',', movie['year'],
          ',', movie['star_cast'], ',', movie['rating'])


# In[7]:


df = pd.DataFrame(list)
df


# In[8]:


df.head(11)


# In[9]:


df[['Director','Actor1','Actor2']] = df['star_cast'].str.split(',',expand=True)
df.head()


# In[10]:


df['rating'] = pd.to_numeric(df['rating'])


# In[11]:


df['rating'] = df['rating'].round(2)


# In[12]:


df.head(5)


# In[13]:


df['year'].value_counts()


# In[14]:


df['year'].min()


# In[15]:


df['year'].max()


# In[16]:


df['year'] = pd.to_numeric(df['year'])
df.head()


# In[17]:


bins = [1920,1931,1941,1951,1961,1971,1981,1991,2001,2011,2021]

labels = ['First Decade', 'Second Decade', 'Third Decade', 'Fourth Decade', 'Fifth Decade', 'Sixth Decade', 
          'Seventh Decade', 'Eight Decade', 'Ninth Decade', 'Tenth Decade']

df['year_category'] = pd.cut(df['year'], bins=bins, labels=labels)


# In[18]:


df.head()


# In[19]:


df['year_category'].value_counts()


# In[20]:


df.tail()


# In[21]:


df['rating'].min()


# In[22]:


df['rating'].max()


# In[23]:


df['rating'].value_counts()


# In[24]:


bins1 = [0,1,2,3,4,5,6,7,8,9,10]

labels1 = ['awful', 'yikes', 'bleh', 'so so', 'average', 'decent', 
          'Good', 'very good', 'awesome', 'elite']

df['rating_category'] = pd.cut(df['rating'], bins=bins1, labels=labels1)


# In[25]:


df.head()


# In[26]:


df.tail()


# In[27]:


df['rating_category'].value_counts()


# In[28]:


duplicate_actors = df[df.duplicated(subset=['Actor1','Actor2'], keep=False)]
duplicate_actors


# In[29]:


duplicate_actors['Actor1'].value_counts()


# In[30]:


duplicate_actors['Actor2'].value_counts()


# In[31]:


duplicate_actors['year_category'].value_counts()


# In[32]:


duplicate_directors = df[df.duplicated(subset=['Director'], keep=False)]
duplicate_directors


# In[33]:


duplicate_directors['Director'].value_counts()


# In[34]:


df.head()


# In[35]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')

sns.countplot(data=df, x='year_category')
plt.title('Comparison of Year Category', fontweight = 30, fontsize = 20)
plt.xlabel('Year Category', fontweight = 30, fontsize = 20)
plt.ylabel('Count', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[36]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')

sns.countplot(data=duplicate_directors, y='Director')
plt.title('Comparison of Movie Directors', fontweight = 30, fontsize = 20)
plt.xlabel('Count', fontweight = 30, fontsize = 20)
plt.ylabel('Director', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[37]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')

sns.countplot(data=duplicate_directors, y='Director', order = duplicate_directors['Director'].value_counts().index)
plt.title('Comparison of Movie Directors', fontweight = 30, fontsize = 20)
plt.xlabel('Count', fontweight = 30, fontsize = 20)
plt.ylabel('Directors', fontweight = 30, fontsize = 20)
plt.xticks
plt.show()


# In[38]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')

sns.countplot(data=df, x='rating_category')
plt.title('Comparison of Rating Category', fontweight = 30, fontsize = 20)
plt.xlabel('Rating Category', fontweight = 30, fontsize = 20)
plt.ylabel('Count', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[39]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')
sns.scatterplot(data=df, x='year', y='rating')
plt.title('Scatterplot of Movie Rating vs Year', fontweight = 30, fontsize = 20)
plt.xlabel('Year', fontweight = 30, fontsize = 20)
plt.ylabel('Movie Ratings', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[40]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')
sns.scatterplot(data=df, x='year', y='rating', hue='year_category')
plt.title('Scatterplot of Movie Rating vs Year', fontweight = 30, fontsize = 20)
plt.xlabel('Year', fontweight = 30, fontsize = 20)
plt.ylabel('Movie Ratings', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[41]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')
sns.scatterplot(data=df, x='year', y='rating', hue='year_category', size='rating', sizes=(20, 200))
plt.title('Scatterplot of Movie Rating vs Year', fontweight = 30, fontsize = 20)
plt.xlabel('Year', fontweight = 30, fontsize = 20)
plt.ylabel('Movie Ratings', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[42]:


Top_20 = df.head(20)
Top_20


# In[43]:


plt.rcParams['figure.figsize'] = (15, 9)
plt.style.use('tableau-colorblind10')

sns.countplot(data=Top_20, x='year_category')
plt.title('Comparison of Top 20 Movies', fontweight = 30, fontsize = 20)
plt.xlabel('Year Category', fontweight = 30, fontsize = 20)
plt.ylabel('Count', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 75)
plt.show()


# In[47]:


movie_rate = df[['movie_title', 'year', 'rating']]
movie_rate.head(10)


# In[ ]:




