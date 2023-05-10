#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pickle


# In[2]:


movies=pd.read_csv(r'C:\Users\Tharu\OneDrive\Desktop\project\collegeproject\gs22\modelanddata\movies.csv')
movies.head()


# In[3]:


ratings=pd.read_csv(r'C:\Users\Tharu\OneDrive\Desktop\project\collegeproject\gs22\modelanddata\ratings.csv',usecols=['userId','movieId','rating'])
ratings.head()


# In[4]:


ratings.shape


# In[5]:


movies.shape


# In[6]:


movies_users=ratings.pivot(index='movieId',columns='userId',values='rating').fillna(0)
movies_users.head()


# In[7]:


from scipy.sparse import csr_matrix


# In[8]:


mat_movies=csr_matrix(movies_users.values)


# In[9]:


from sklearn.neighbors import NearestNeighbors


# In[10]:


model=NearestNeighbors(metric='cosine',algorithm='brute',n_neighbors=20)
model.fit(mat_movies)


# In[12]:


from fuzzywuzzy import process


# In[15]:


def recommender(movie_name,data,n):
    idx=process.extractOne(movie_name,movies['title'])[2]
    print('Movie Selected :',movies['title'][idx],'Index:',idx)
    print('Searching for recommendation.................')
    distance,indices=model.kneighbors(data[idx],n_neighbors=n)
    for i in indices:
        print(movies['title'][i].where(i!=idx))


# In[18]:
pickle.dump(recommender,open("recommender_model.sav","wb"))
recommender('forrest gump',mat_movies,20)




# In[ ]:




