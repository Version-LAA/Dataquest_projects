#!/usr/bin/env python
# coding: utf-8

# # Application Audience Engagement
# 
# The purpose and goal of this app is to analyze two data sets on apps in both the Google Playstore, and the Apple App Store to identify which type of apps are likely to attract more users. The criteria used in this analysis include only free apps, apps in the english language. 
# 
# Source of Google Data: https://www.kaggle.com/lava18/google-play-store-apps
# - [ rows] and 13 columns
# 
# Source of Apple Data: https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps
# - 7,197 rows and 16 columns
# 
# Note:
# 
# This was a guided project a part of Dataquest project: Profitable App Profiles for the App Store and Google Play Market
# 
# 

# In[341]:


from csv import reader

#Open and read the apple store dataset and convert into a list.
open_apple = open('AppleStore.csv')
read_apple =reader(open_apple)
apple_dataset = list(read_apple)

#Open and read the google playstore dtaset and convert into a list
open_google = open('googleplaystore.csv')
read_google= reader(open_google)
google_dataset = list(read_google)



def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


print('Apple Data Exploration\n')
explore_data (apple_dataset,0,2,True)
print("\n")

print('Google Data Exploration\n')
explore_data (google_dataset,0,2,True)



# ### Data Exploration
# 
# Using and calling the explore_data() function, provided me with context and information on the datasets such as the column headers, number of rows, and number of columns. This data will help identify which columns can be used to accomplish our goal of identifing the apps in both app stores that are the most popular. 
# 
# explore_data (apple_dataset,0,2,True)
# explore_data (google_dataset,0,2,True)
# 
# 1. Apple Data
# - Number of rows: 7198 and Number of columns: 16
# - Columns: ['id', 'track_name', 'size_bytes', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', 'user_rating', 'user_rating_ver', 'ver', 'cont_rating', 'prime_genre', 'sup_devices.num', 'ipadSc_urls.num', 'lang.num', 'vpp_lic']
# 
# 2. Google Data
# - Number of rows: 10842; Number of columns: 13
# - ['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price', 'Content Rating', 'Genres', 'Last Updated', 'Current Ver', 'Android Ver']
# 
# ### Data Cleaning pt 1.
# 
# - Upon reading the the discussion form for the google app dataset, there was a post that discussed an error in column 10473 that was missing a filed. I performed a deletion of the row with the missing data. There was no errors identified in the discussion form for apple data.
# 
# - There were a number of duplicate apps identified within the google dataset for apps (i.e. instagram). It was identified that the reviews column can be used to identify data that was collected at different times. Therefore, I will not remove duplicates randomly, but will retain the row for that specific app with the most reviews. This can indicate the most recent update for that app.

# In[342]:




#This will delete the fow that is missing data. This was ran once, and can not be ran again w/o deleting correct data.

del google_dataset[10472]

'''Created a function called duplicate_finder which is used to identify the number 
duplicate apps within the dataset. Will return number of duplicates found for specific index and print duplicates.

'''

def duplicate_finder(dataset,column_index):
    duplicate_field = []
    unique_field= []
    
    for element in dataset:
        name = element[column_index]
        if name in unique_field:
            duplicate_field.append(name)
        else:
            unique_field.append(name)
    return print('Duplicates:', len(duplicate_field),'\n',duplicate_field[:5])
   

#calls function duplicate finder on the google dataset for apps with duplicate names.    

print('Google - with up to 5 examples')
duplicate_finder(google_dataset,0)
print("\n")


                        


# In[343]:


'''The following loops through the google dataset, identifies the app and it's corresponding
max number of reviews and adds the name and max review amount to a new dictionary.

'''
reviews_max = {}


for app in google_dataset[1:]:
    name = app[0]
    n_reviews = app[3]
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


print(len(reviews_max))


        
    


# ### Data Cleaning pt. 2
# 
# 1. Using the new dictionary we created above with the duplicate apps that had the max reviews. I created two empty list, one to store clean data, and the other to keep track of the app as we add them to the clean list.
# 
# 2. After looping through the dataset, if the number of reviews is equal to the max number of reviews for that app, and the app does not exist in the already_added list, we will append the entire row into the android_clean list. The already_added list is there to keep track of apps already added.

# In[344]:


android_clean =[]
already_added = []
count = 0

for app in google_dataset[1:]:
    name = app[0]
    n_reviews = app[3]
    count +=1
    if n_reviews == reviews_max[name] and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
    
  

print(len(android_clean))

#explore_data



        


# ### Data Cleaning pt. 3
# 
# - Next step in cleaning the data will be filtering out non- english apps. I approached this by creating a function to help identify if a character is a non english using the char() function. Majority of english characters will return a char value between 0 - 127. But because some apps have/use emoji's , I created a function that allowed no more than 3 consecutive characters out of range to ensure we do not miss a lot of apps.
# 
# - Final data cleaning effort will be to filter out free apps. So I created two new final list that appended only apps that were free.
# 

# In[345]:



def eng_char(string):
    count = 0
    for char in string:
        if ord(char) > 127 :
            count += 1
            
    if count > 3:
        return False
    else:
        return True

filtered_google =[]
filtered_apple = []

for app in android_clean:
    name = app[0]
    if eng_char(name)is True:
        filtered_google.append(app)
    
for app in apple_dataset:
    name = app[2]
    if eng_char(name)is True:
        filtered_apple.append(app)
        
# explored new filtered list of english apps.
        
explore_data(filtered_google,0,0,True)

explore_data(filtered_apple,0,0,True)
        
    


# In[346]:


#isolate free apps from filtered data

final_apple =[]
final_google=[]

print(type(filtered_apple[1][4]))

#apple

for app in filtered_apple[1:]:
    price = float(app[4])
    
    if price == 0:
        final_apple.append(app)
        
for app in filtered_google[1:]:
    price = app[6]
    
    if price == 'Free':
        final_google.append(app)

print('apple', len(final_apple))
print('google ',len(final_google))


# ## Analysis Pt1: Most Common Apps by Genre:
# 
# Now that I have cleaned the data, below I Identified some fields from each dataset that may be helpful in accomplishing my goal of idenifying the most popular apps for both app stors. Will create frequency tables using some of these columns.
# 
# Apple data key fields to use
# - track_name
# - ratingcountot
# - primary genre
# - user_rating
# 
# google dta key fields to use
# - app
# - category
# - genre
# - rating
# - reviews
# - installs
# 
# 

# In[347]:


#This function will help put tables in order.

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
#This function will create a frequency table based on a dataset, and column of choice. It will then return the table in percentages.

def freq_table(dataset,index):
    f_table = {}
    f_table_percentage = {}
    f_table_proportions={}
    total = 0
    
   
    for item in dataset[1:]:
        value = item[index]
        if value in f_table:
            f_table[value] +=1
        else:
            f_table[value]=1
    
    for item in f_table:
        f_table_proportions[item] = f_table[item] / len(dataset[1:])
        f_table_percentage[item] = f_table_proportions[item] * 100

    
    
    return f_table_percentage




#Google frequency table by Genre 
print('Google - Genre\n')

freq_table(final_google,8)

display_table(final_google,8)


#Google frequency table by Category 
print('\n')

print('Google - Category\n')

freq_table(final_google,1)

display_table(final_google,1)


#Apple frequency table by Category
print('\n')

print('Apple - Category\n')

freq_table(final_apple,11)

display_table(final_apple,11)


# In[348]:


'''This section will find out which genre are the most popular, and calculate the avg number of installs 
for each app genre for the apple app store
'''

table = freq_table(final_apple,11)

rec_app = {}

for element in table:
    total = 0
    len_genre = 0
    for item in final_apple:
        genre_app = item[11]
        
        if genre_app == element:
            sum_user = float(item[5])
            total +=sum_user
            len_genre +=1
    
    rec_app[element]= total/len_genre

print(rec_app)


    
    


# In[349]:


'''This section will find out which genre are the most popular, and calculate the avg number of installs 
for each app genre for the google app store
'''

unique_google = freq_table(final_google,1)

for element in unique_google:
    category = element
    total = 0
    len_category = 0
    
    for item in final_google[1:]:
        category_name = item[1]
        
        
        if category_name == category:
            num_installs = item[5]
            num_installs = num_installs.replace('+','')
            num_installs = num_installs.replace(',','')
            
            total += float(num_installs)
            len_category +=1
    avg = total/len_category
    print(category,'','avg: ', avg)
        

    
    


# 

# In[ ]:




