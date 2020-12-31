#!/usr/bin/env python
# coding: utf-8

# # Hacker News Post Analysis
# 
# The purpose of this project is to analyze a subset of submissions to the Hacker News website who's post were either specific questions to the Hacker News community, or post submitted related to projects products, or something interesting. I will compare the two following
# 
# - Which post recives more comments on average.
# - Do posts created at a certain times receive more comments on average.

# In[1]:


from csv import reader
import datetime as dt

open_file = open('hacker_news.csv')
read_file = reader(open_file)
hn = list(read_file)

print(hn[:5])


# In[2]:


# Creating a list of just headers, and creating new dataset withouth headers
headers = hn[0]

hn = hn[1:]

print(hn[:5])


# In[5]:


'''Creating new list to filter out post that were questions,
vs post that were interesting projects/content vs others'''

ask_posts = []

show_posts = []

other_posts = []

for row in hn:
    title = row[1]
    title = title.lower()
    if title.startswith('ask hn'):
        ask_posts.append(row)
    elif title.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
        


# In[6]:


print("Ask post: ", len(ask_posts))


print("show post: ", len(show_posts))


print("Other post: ", len(other_posts))


# In[14]:


''' Next will find the total number of comments for both ask
and show post to determine which post recived more comments
avg'''



def avg_comments(post_name):
    total_ask_comments = 0
    for post in post_name:
        comments = int(post[4])
        total_ask_comments += comments
    avg_ask_comments = total_ask_comments / len(post_name)
    return (avg_ask_comments)

print("avg ask comments: ", avg_comments(ask_posts))
print("avg show comments: ", avg_comments(show_posts))
    


# Analysis show that on average,Ask Post recieve 14.04 comments per post, while Show post recived 10.32 comments per post. Showing that Ask post are a slightly more popular.  
# 
# I will now focus the remaining analysis on ask post to identify if ask posts created at a certain time more likely to attack comments.

# In[19]:


# change date field to datetime object to make parsing easier.

d1_format = "%m/%d/%Y %H:%M"
results_list = []

for row in ask_posts:
    date = row[-1]
    comments= int(row[4])
    new_date = dt.datetime.strptime(date,d1_format)
    results_list.append([new_date, comments])

print("example of results list: \n", results_list[:5])


# In[26]:


counts_by_hour = {}
comments_by_hour = {}


for row in results_list: 
    hour = row[0].strftime('%H')
    comments = row[1]
    if hour in counts_by_hour:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += comments
    else:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = comments
        
        
print(counts_by_hour)

print(comments_by_hour)


# In[27]:


''' Below shows the number of ask posts created during each
hour of the day. Then a second frequency table that contains 
the number of comments asks posts created at each hour received'''

        
print(counts_by_hour)

print('\n')

print(comments_by_hour)


# In[28]:


''' Next I will create a list of a list to show the average 
number of comments per posts created during each hour of the 
day'''

avg_by_hour = []

for item in comments_by_hour:
    avg_by_hour.append([item,comments_by_hour[item]/counts_by_hour[item]])
    
    
print(avg_by_hour)


# In[44]:


#final sorting

swap_avg_by_hour = []

for item in avg_by_hour:
    swap_avg_by_hour.append([item[1],item[0]])

print(swap_avg_by_hour)

print('\n')

sorted_swap = sorted(swap_avg_by_hour,reverse=True)

print("top 5 Hours for Ask Posts Comments \n", sorted_swap[:5])
print('\n')
print("top 5 Hours for Ask Posts Comments - Formatted \n")
for item in sorted_swap[:5]:
    time = int(item[1])
    avg = item[0]
    date_obj = dt.time(hour=time)
    f_time= date_obj.strftime("%H:%S")
    
    
    print("{}:{:,.2f} average comments per post".format(f_time,avg))
    


# # Final Analysis
# 
# Based on my , the top five hours that a post will acquire the most comments is the 5 PM hour with the average number of comments are 38.59. I believe this could be attributed to the average time user's are off work.
# 
# top 5 Hours for Ask Posts Comments - Formatted 
# 
# 15:00:38.59 average comments per post
# 02:00:23.81 average comments per post
# 20:00:21.52 average comments per post
# 16:00:16.80 average comments per post
# 21:00:16.01 average comments per post
