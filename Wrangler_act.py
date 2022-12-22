#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

# In[3]:


#Import required packages
import pandas as pd
import numpy as np
import time as t
import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# # Data Gathering
# In the cell below, gather **all** three pieces of data for this project and load them in the notebook. **Note:** the methods required to gather each data are different.
# 1. Directly download the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[4]:


# Downloading WeRateDogs Twitter archive dataset directly
twitter_archive = pd.read_csv('./twitter-archive-enhanced.csv')


# 2. Use the Requests library to download the tweet image prediction (image_predictions.tsv)

# In[5]:


# Downloading image_predictions.tsv using requests library 

image_URL = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
res = requests.get(image_URL)

with open('image_predictions.tsv', mode ='wb') as outfile:
    outfile.write(res.content)

#Read TSV file
image_predictions = pd.read_csv('image_predictions.tsv', sep='\t')
image_predictions.head()


# 3. Use the Tweepy library to query additional data via the Twitter API (tweet_json.txt)

# In[6]:


# install tweepy
pip install tweepy


# In[7]:


# Downloading tweet_json.txt via the Twitter API

import tweepy
from tweepy import OAuthHandler
from timeit import default_timer as timer

# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = 'HIDDEN'
consumer_secret = 'HIDDEN'
access_token = 'HIDDEN'
access_secret = 'HIDDEN'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# NOTE TO STUDENT WITH MOBILE VERIFICATION ISSUES:
# df_1 is a DataFrame with the twitter_archive_enhanced.csv file. You may have to
# change line 17 to match the name of your DataFrame with twitter_archive_enhanced.csv
# NOTE TO REVIEWER: this student had mobile verification issues so the following
# Twitter API code was sent to this student from a Udacity instructor
# Tweet IDs for which to gather additional data via Twitter's API
tweet_ids = twitter_archive.tweet_id.values

len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepyException as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# In[8]:



List = []
with open('tweet-json.txt') as file:
    lns = file.readlines()
    for line in lns:
        Pjson = json.loads(line)
        List.append({'tweet_id': Pjson['id'],
                        'retweet_count': Pjson['retweet_count'],
                        'favorite_count': Pjson['favorite_count']})
        
json_T = pd.DataFrame(List, columns = ['tweet_id', 'retweet_count', 'favorite_count'])

json_T.head()

        


# ## Assessing Data
# In this section, detect and document at least **eight (8) quality issues and two (2) tidiness issue**. You must use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** pay attention to the following key points when you access the data.
# 
# * You only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate your skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * You do not need to gather the tweets beyond August 1st, 2017. You can, but note that you won't be able to gather the image predictions for these tweets since you don't have access to the algorithm used.
# 
# 

# In[9]:


# Display twitter archive

twitter_archive


# In[10]:


twitter_archive.describe()


# In[11]:


twitter_archive.info()


# In[12]:



# Check for missing values in twitter_archive
twitter_archive.isnull().sum()


# In[13]:


# Check for duplicated values in twitter_archive 
twitter_archive.duplicated().sum()


# In[14]:


# Check for name missing values in twitter_archive

twitter_archive.name.isnull().sum()


# In[15]:


# Count doggo values in twitter_archive
twitter_archive.doggo.value_counts()


# In[16]:


# Count floofer values in twitter_archive

twitter_archive.floofer.value_counts()


# In[17]:


# Count pupper values in twitter_archive

twitter_archive.pupper.value_counts()


# In[18]:


# Count puppo values in twitter_archive

twitter_archive.puppo.value_counts()


# In[19]:


# Count the rating_denominator values in twitter_archive

twitter_archive.rating_denominator.value_counts()


# In[20]:


# Count the rating_numerator values in twitter_archive

twitter_archive.rating_numerator.value_counts()


# In[21]:


# Check and count the source in twitter_archive
twitter_archive.source.value_counts()


# In[22]:


# Display image predictions

image_predictions


# In[23]:


image_predictions.describe()


# In[24]:


image_predictions.info()


# In[25]:


# Check for missing values
image_predictions.isnull().sum()


# In[26]:


# Check for duplicated values
image_predictions.duplicated().sum()


# In[27]:


# Check for duplicated jpg_url

image_predictions.jpg_url.duplicated().sum()


# In[28]:


image_predictions.p1.value_counts()


# In[29]:


image_predictions.p2.value_counts()


# In[30]:


image_predictions.p3.value_counts()


# In[31]:


json_T


# In[32]:


json_T.info() # No missing values 


# In[33]:


json_T.duplicated().sum()


# ### Quality issues
# 
# **Twitter Archive**
# 
# 1. Retweets and replies should be deleted because original ratings with images are all that we really need.
# 
# 2. Missing values in columns: in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp, and expanded_urls.
# 
# 3. timestamp should be date instaed of str.
# 
# 4. tweet_id should be object instaed of int64.
# 
# **Image Predictions**
# 
# 5. jpg_url has 66 duplicated values
# 
# 6. P1, P2, and P3's type of dog breeds contained both capital and lowercase letters.
# 
# 7. Names column need cleaning in Tarchive_clean .
# 8. No rating standard.

# ### Tidiness issues
# 9. json_T should be part of the twitter_archive table.
# 10.  All tables should be part of one dataset.

# ## Cleaning Data
# In this section, clean **all** of the issues you documented while assessing. 
# 
# **Note:** Make a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# In[74]:


# Make copies of original pieces of data
Tarchive_clean = twitter_archive.copy()
image_predictions_clean = image_predictions.copy()
jsonT_clean = json_T.copy()


# #### **Quality issues**

# ### Issue #1:
# Retweets and replies should be deleted because original ratings with images are all that we really need in Tarchive_clean.

# #### Define:
# Remove retweeted status id and reply to status id columns, using isnull().

# #### Code

# In[76]:


# Remove retweets and replies  
Tarchive_clean = Tarchive_clean[Tarchive_clean.retweeted_status_id.isnull()]
Tarchive_clean = Tarchive_clean[Tarchive_clean.in_reply_to_status_id.isnull()]


# #### Test

# In[77]:


Tarchive_clean.info()


# ### Issue #2:  
# Missing values in columns: in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp, and expanded_urls in Tarchive_clean.
# 

# #### Define 
# Remove these columns and the useless coulmuns in the analysis using dropna() method.
# 

# #### Code

# In[89]:


Tarchive_clean.dropna(axis='columns',how='any', inplace=True)


# #### Test

# In[91]:


Tarchive_clean.info()


# ### Issue #3 & #4:
# 
# timestamp should be date instaed of str in Tarchive_clean.
# 
# tweet_id should be object instaed of int64 in Tarchive_clean & image_predictions_clean.

# #### Define 
# fixing datatyps using astype() method.
# 

# #### Code

# In[94]:


Tarchive_clean['timestamp'] = pd.to_datetime(Tarchive_clean['timestamp'])
Tarchive_clean['tweet_id'] = Tarchive_clean['tweet_id'].astype('str')
image_predictions_clean['tweet_id'] = image_predictions_clean['tweet_id'].astype('str')


# #### Test:

# In[95]:


Tarchive_clean.info()


# In[96]:


image_predictions_clean.info()


# ### Issue #5: 
# jpg_url has 66 duplicated values in image_predictions_clean.
# 

# #### Define 
# Drop duplicates usinf drop_duplicates() method

# #### Code

# In[97]:


image_predictions_clean = image_predictions_clean.drop_duplicates(subset=['jpg_url'], keep='last')


# #### Test

# In[43]:


image_predictions_clean.duplicated().sum()


# ### Issue #6: 
# P1, P2, and P3's type of dog breeds contained both capital and lowercase letters in image_predictions_clean.

# #### Code

# In[44]:


image_predictions_clean['p1'] = image_predictions_clean['p1'].str.lower()
image_predictions_clean['p2'] = image_predictions_clean['p2'].str.lower()
image_predictions_clean['p3'] = image_predictions_clean['p3'].str.lower()


# #### Test

# In[45]:


image_predictions_clean.p1.head()


# In[98]:


image_predictions_clean.p2.head()


# In[99]:


image_predictions_clean.p3.head()


# #### Issue #7:  
# names column need cleaning in Tarchive_clean. 

# In[185]:


Tarchive_clean.name.value_counts()


# #### Define
# Using drop() method  

# #### Code

# In[186]:


#Using the drop() function
Tarchive_clean.drop(Tarchive_clean.index[Tarchive_clean['name'] == 'None'], inplace=True)
Tarchive_clean.drop(Tarchive_clean.index[Tarchive_clean['name'] == 'a'], inplace=True)


# #### Test

# In[187]:


Tarchive_clean.name.value_counts()


# ### Issue #8: 
# No rating standard 

# #### Define 
# Devide rating_numerator by rating_denominator to get standardized rating.

# #### Code

# In[188]:


# Create a  column called rating
Tarchive_clean['SD_rate'] = Tarchive_clean['rating_numerator'] / Tarchive_clean['rating_denominator']


# #### Test

# In[189]:


Tarchive_clean.info()


# #### Tidiness issues
# 

# #### Issue #9:
# jsonT_clean should be part of the Tarchive_clean table

# #### Define:
# Using merge() method, and joining on tweet id.
# 

# #### Code

# In[190]:


jsonT_clean.info()


# In[191]:


# Converting tweet id in jsonT_clean to a object datatype

jsonT_clean['tweet_id']= jsonT_clean['tweet_id'].astype(str)


# In[192]:


jsonT_clean.info()


# In[240]:


# Merging the datasets
Tarchive_clean = pd.merge(Tarchive_clean, jsonT_clean,on = ['tweet_id'], how = 'left')


# #### Test

# In[241]:


Tarchive_clean.info()


# #### Issue #10:
# All tables should be part of one dataset

# #### Define:
# Merging tables using merge() method.
# 

# #### Code

# In[244]:


#dataframe that merge Tarchive_clean and image_predictions_clean
NewDf = pd.merge(Tarchive_clean, image_predictions_clean,on = ['tweet_id'], how = 'left')


# In[249]:


NewDf.info()


# #### Test

# In[253]:


NewDf.head()


# In[308]:


# Merging seprate columns into one column to ease the analyze
NewDf['dogs'] = NewDf['text'].str.extract('(doggo|floofer|pupper|puppo)')


# In[309]:


NewDf.dogs.value_counts()


# ## Storing Data
# Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[310]:


# Storing the new df
NewDf.to_csv('twitter_archive_master.csv')
archive_master = pd.read_csv('twitter_archive_master.csv')


# In[311]:


archive_master.info()


# In[312]:


# Removing Unnamed: 0 column
archive_master= archive_master.drop(['Unnamed: 0'],1)


# In[313]:


archive_master.info()


# ## Analyzing and Visualizing Data
# In this section, analyze and visualize your wrangled data. You must produce at least **three (3) insights and one (1) visualization.**

# ### Insights:
# 1. Pupper is the most famous dog stage
# 
# 2. Charlie is the most common name
# 
# 3. Golden_retriever takes the 1st place popular dog

# In[314]:


archive_master.dogs.value_counts() #Pupper is the most famous dog stage


# In[376]:


# pie chart for most famous dog stage
label = ['No favourite stage', 'pupper', 'doggo', 'puppo', 'floofer']
newV = archive_master.dogs.value_counts()
colors = ['grey', 'green', 'lightblue' ,'y', 'pink']
plt.pie(newV, colors = colors, radius = 3, autopct='%1.5f%%')## autopct to calculate the percentage 
plt.legend(label)
plt.title('Famous dog stage');


# In[261]:


archive_master.name.value_counts()  # Charlie is the most popular name 


# In[277]:


archive_master.p1.value_counts()


# ### Visualization

# In[386]:


#setting the DataFrame to index the timestamp column
archive_master = archive_master.set_index('timestamp')


# In[387]:


archive_master.head()


# In[388]:


archive_master.corr()


# In[391]:


sns.pairplot(archive_master, vars=["SD_rate", "retweet_count_x", "favorite_count_x"]);

