#!/usr/bin/env python
# coding: utf-8

# 

# In[1]:


# standard imports
import pandas as pd
import numpy as np

# Do not change this option; This allows the CodeGrade auto grading to function correctly
pd.set_option('display.max_columns', None)
import warnings
warnings.filterwarnings("ignore")


# In[2]:


import os
print("Current working directory:", os.getcwd())


# In[3]:


import os

fileName = "survivor.xlsx"
print(f"Looking for file: {os.path.abspath(fileName)}")
if not os.path.exists(fileName):
    print("File does not exist.")
else:
    print("File found!")


# In[4]:


import os
os.getcwd()


# First, import the data from the `survivor.xlsx` file, calling the respective DataFrames the same as the sheet name but with lowercase and [snake case](https://en.wikipedia.org/wiki/Snake_case).  For example, the sheet called `Castaway Details` should be saved as a DataFrame called `castaway_details`.  Make sure that the data files are in the same folder as your notebook.
# 
# Note:  You may or may not need to install [openpyxl](https://openpyxl.readthedocs.io/en/stable/) for the code below to work.  You can use: `$ pip install openpyxl`

# In[5]:


# import data from Excel
import pandas as pd
import os

# Define file path
fileName = "survivor.xlsx"

# Check if the file exists
if not os.path.exists(fileName):
    raise FileNotFoundError(f"The file '{fileName}' does not exist in the current directory.")

# Load the Excel file
xls = pd.ExcelFile(fileName)

# Load the castaways sheet into a DataFrame
castaways = pd.read_excel(xls, 'Castaways')

# Print columns to verify
print(castaways.columns)


# setup Filename and Object
fileName = "survivor.xlsx"
xls = pd.ExcelFile(fileName)

# import individual sheets
castaway_details = pd.read_excel(xls, 'Castaway Details')
castaways = pd.read_excel(xls, 'Castaways')
challenge_description = pd.read_excel(xls, 'Challenge Description')
challenge_results = pd.read_excel(xls, 'Challenge Results')
confessionals = pd.read_excel(xls, 'Confessionals')
hidden_idols = pd.read_excel(xls, 'Hidden Idols')
jury_votes = pd.read_excel(xls, 'Jury Votes')
tribe_mapping = pd.read_excel(xls, 'Tribe Mapping')
viewers = pd.read_excel(xls, 'Viewers')
vote_history = pd.read_excel(xls, 'Vote History')
season_summary = pd.read_excel(xls, 'Season Summary')
season_palettes = pd.read_excel(xls, 'Season Palettes')
tribe_colours = pd.read_excel(xls, 'Tribe Colours')


# **Exercise1:** Change every column name of every DataFrame to lowercase and snake case.  This is a standard first step for some programmers as lowercase makes it easier to write and snake case makes it easier to copy multiple-word column names.
# 
# For example, `Castaway Id` should end up being `castaway_id`.  You should try doing this using a `for` loop instead of manually changing the names for each column.  It should take you no more than a few lines of code.  Use stackoverflow if you need help.

# In[6]:


import openpyxl
print("openpyxl is installed and working!")


# In[7]:


### 
# List of all DataFrames
dfs = [castaway_details, castaways, challenge_description, challenge_results,
       confessionals, hidden_idols, jury_votes, tribe_mapping, viewers, vote_history,
       season_summary, season_palettes, tribe_colours]

# Change column names to lowercase and snake case
for df in dfs:
    df.columns = df.columns.str.lower().str.replace(' ', '_')


print (castaways)
print(castaway_details)

###


# **Q2:** What contestant was the oldest at the time of their season?  We want to look at their age at the time of the season and NOT their current age.  Select their row from the `castaway_details` DataFrame and save this as `Q2`.  This should return a DataFrame and the index and missing values should be left as is.

# In[8]:


# Drop 'age_at_season' column if it exists
if 'age_at_season' in castaway_details.columns:
    castaway_details = castaway_details.drop(columns=['age_at_season'])

# Find the row where the age is the maximum in the castaways DataFrame
oldest_contestant_id = castaways.loc[castaways['age'].idxmax(), 'castaway_id']

# Select only the relevant row from a fresh copy of castaway_details
Q2 = castaway_details.loc[castaway_details['castaway_id'] == oldest_contestant_id].copy()

# Print the result
print(Q2)


# **Q3:** What contestant played in the most number of seasons? Select their row from the `castaway_details` DataFrame and save this as `Q3`.  This should return a DataFrame and the index and missing values should be left as is.

# In[9]:


# Count the number of seasons each contestant participated in
season_counts = castaways.groupby('castaway_id').size()

# Find the contestant with the maximum number of seasons played
most_seasons_id = season_counts.idxmax()

# Select their details from castaway_details
Q3 = castaway_details[castaway_details['castaway_id'] == most_seasons_id]

# Print the result
print(Q3)



# In[10]:


print(most_seasons_id)


# **Q4:** Create a DataFrame of all the contestants that won their season (aka their final result in the `castaways` DataFrame was the 'Sole Survivor').  Call this DataFrame `sole_survivor`.  Note that contestants may appear more than one time in this DataFrame if they won more than one season.  Make sure that the index goes from 0 to n-1 and that the DataFrame is sorted ascending by season number.
# 
# The DataFrame should have the same columns, and the columns should be in the same order, as the `castaways` DataFrame.

# In[11]:


### 

sole_survivor = castaways[castaways['result'] == 'Sole Survivor'].copy()
sole_survivor = sole_survivor.sort_values(by='season').reset_index(drop=True)

sole_survivor
###


# **Q5:** Have any contestants won more than one time?  If so, select their records from the `sole_survivor` DataFrame, sorting the rows by season.  Save this as `Q5`.  If no contestant has won twice, save `Q5` as the string `None`.

# In[12]:


winner_counts = sole_survivor['castaway_id'].value_counts()
repeat_winners_ids = winner_counts[winner_counts > 1].index

if len(repeat_winners_ids) > 0:
    
    Q5 = sole_survivor[sole_survivor['castaway_id'].isin(repeat_winners_ids)].sort_values(by='season').copy()
else:
   
    Q5 = None

print(Q5)


# **Q6:** What is the average age of contestants when they appeared on the show?  Save this as `Q6`.  Round to nearest integer.

# In[13]:


### 
Q6 = round(castaways['age'].mean())
Q6

###


# **Q7:** Who played the most total number of days of Survivor? If a contestant appeared on more than one season, you would add their total days for each season together. Save the top five contestants in terms of total days played as a DataFrame and call it `Q7`, sorted in descending order by total days played.  
# 
# The following columns should be included: `castaway_id`, `full_name`, and `total_days_played` where `total_days_played` is the sum of all days a contestant played. The index should go from 0 to n-1.
# 
# Note:  Be careful because on some seasons, the contestant was allowed to come back into the game after being voted off.  Take a look at [Season 23's contestant Oscar Lusth](https://en.wikipedia.org/wiki/Ozzy_Lusth#South_Pacific) in the `castaways` DataFrame as an example.  He was voted out 7th and then returned to the game.  He was then voted out 9th and returned to the game a second time.  He was then voted out 17th the final time.  Be aware of this in your calculations and make sure you are counting the days according to the last time they were voted off or won. 

# In[14]:


last_days = castaways.groupby(['castaway_id', 'season'])['day'].max().reset_index()

total_days = last_days.groupby('castaway_id')['day'].sum().reset_index()

total_days_played = total_days.merge(
    castaway_details[['castaway_id', 'full_name']],
    on='castaway_id',
    how='left'
)

total_days_played.rename(columns={'day': 'total_days_played'}, inplace=True)

Q7 = total_days_played.sort_values(by='total_days_played', ascending=False).head(5)

Q7.reset_index(drop=True, inplace=True)

Q7 = Q7[['castaway_id', 'full_name', 'total_days_played']]



print(Q7)


# **Q8A & Q8B**: Using the `castaway_details` data, what is the percentage of total extroverts and introverts that have played the game (count players only once even if they have played in more than one season).  Do not count contestants without a personality type listed in your calculations.  Save these percentages as `Q8A` and `Q8B` respectively.  Note: Round all percentages to two decimal points and write as a float (example: 55.57).  
# 
# For more information on personality types check this [Wikipedia article](https://en.wikipedia.org/wiki/Myers%E2%80%93Briggs_Type_Indicator).

# In[15]:


### 

personality_counts = castaway_details['personality_type'].dropna().str[0].value_counts()
total = personality_counts.sum()
E = personality_counts.get('E', 0) / total * 100
I = personality_counts.get('I', 0) / total * 100
Q8A = round(E, 2)
Q8B = round(I, 2)


###


# In[ ]:





# In[16]:


### 
print(Q8A)

print(Q8B)

###


# **Q9A & Q9B**: Now that we know the percentages of total players that are extroverted and introverted, let's see if that made a difference in terms of who actually won their season.
# 
# What is the percentage of total extroverts and introverts that have won the game (count players only once even if they have won more than one season)?  Save these percentages as `Q9A` and `Q9B` respectively.  Note: Round all percentages to two decimal points and write as a float (example: 55.57).

# In[17]:


unique_winners = sole_survivor.drop_duplicates(subset='castaway_id')

known_personality_winners = unique_winners.dropna(subset=['personality_type'])

extroverts_count = known_personality_winners['personality_type'].str.startswith('E').sum()

introverts_count = known_personality_winners['personality_type'].str.startswith('I').sum()

total_winners_with_personality = len(known_personality_winners)

Q9A = round((extroverts_count / total_winners_with_personality) * 100, 2)
Q9B = round((introverts_count / total_winners_with_personality) * 100, 2)

print(Q9A)



# In[18]:


print(Q9B)


# **Q10:** Which contestants have never received a tribal council vote (i.e. a vote to be voted out of the game as shown in the `vote_id` column in the `vote_history` DataFrame)? Note that there are various reasons for a contestant to not receive a tribal vote: they quit, made it to the end, medical emergency, etc.  Select their rows from the `castaway_details` DataFrame and save this as `Q10` in ascending order by `castaway_id`.  This should return a DataFrame and the index and missing values should be left as is.

# In[21]:


# Step 1: Extract castaway_ids from vote_history where votes were cast
contestants_with_votes = vote_history['castaway_id'].dropna().unique()

# Step 2: Identify contestants who never received any votes
contestants_no_votes = castaway_details[~castaway_details['castaway_id'].isin(contestants_with_votes)]

# Step 3: Sort by castaway_id and keep the original index as is
Q10 = contestants_no_votes.sort_values(by='castaway_id')

# Print the result
print(Q10)



# 

# In[235]:


print(castaway_details.columns)
print(challenge_results.columns)


# In[236]:


challenge_wins = challenge_results.groupby('winner_id').size()

most_wins_id = challenge_wins.idxmax()

Q11 = castaway_details[castaway_details['castaway_id'] == most_wins_id]

# Q11
print(Q11)


# **Q12:** Let's see how many winners ended up getting unanimous jury votes to win the game.  Create a Dataframe that shows the survivors that got unanimous jury votes with these columns in the final output: `season`, `season_name`, `winner_id`, `full_name`.  The DataFrame should be sorted by season and the index should go from 0 to n-1.  Save this as `Q12`. 

# In[237]:


print(jury_votes.columns)


# In[29]:


total_votes_per_season = jury_votes.groupby('season')['castaway'].nunique().reset_index()
total_votes_per_season = total_votes_per_season.rename(columns={'castaway': 'total_jury_votes'})
finalist_votes = jury_votes.groupby(['season', 'finalist']).agg({'vote': 'sum'}).reset_index()
finalist_votes = finalist_votes.merge(total_votes_per_season, on='season')
unanimous_winners = finalist_votes[finalist_votes['vote'] == finalist_votes['total_jury_votes']]
unanimous_winners = unanimous_winners.merge(jury_votes[['season', 'season_name']], on='season', how='left')

unanimous_winners = unanimous_winners.merge(castaways[['castaway', 'full_name']], 
                                            left_on='finalist', right_on='castaway', 
                                            how='left')

Q12 = unanimous_winners[['season', 'season_name', 'finalist', 'full_name']]
Q12 = Q12.sort_values(by='season').reset_index(drop=True)
Q12 = Q12.drop_duplicates(subset=['season', 'finalist'])
Q12 = Q12.sort_values(by='season').reset_index(drop=True)
# Rename the 'finalist' column to 'castaway_id' and the 'castaway_id' to 'winner_id'

Q12 = Q12.rename(columns={'finalist': 'winner_id'})





# Display the final DataFrame
Q12


Q12


# In[ ]:





# In[ ]:





# **Q13:** For the `castaway_details` DataFrame, there is a `full_name` column and a `short_name` column.  It would be helpful for future analysis to have the contestants first and last name split into separate columns.  First copy the `castaway_details` DataFrame to a new DataFrame called `Q13` so that we do not change the original DataFrame.  
# 
# Create two new columns and add the contestant's first name to a new column called `first_name` and their last name to a new column called `last_name`.  Add these columns to the `Q13` DataFrame.  Put the `first_name` and `last_name` columns between the `full_name` and `short_name` columns.
# 
# Note:  Be careful as some players have last names with multiple spaces.  For example, `Lex van den Berghe`.  You should code `Lex` as his first name and `van den Berghe` as his last name.

# In[32]:


# Copy the original DataFrame to a new one to preserve the original data
Q13 = castaway_details.copy()

# Split the full_name column into first_name and last_name
Q13['first_name'] = Q13['full_name'].str.split().str[0]  # Get the first word as first name
Q13['last_name'] = Q13['full_name'].str.split().str[1:].str.join(' ')  # Join the remaining words as last name

# Reorder the columns so that first_name and last_name are between full_name and short_name
Q13 = Q13[['castaway_id','full_name', 'first_name', 'last_name', 'short_name'] + [col for col in Q13.columns if col not in ['castaway_id','full_name', 'first_name', 'last_name', 'short_name']]]

# Display the updated DataFrame
Q13


# **Q14:** Let's say that we wanted to predict a contestants personality type based on the information in the data files.  Your task is to create a DataFrame that lists the `castaway_id`, `full_name` and `personality_type` for each castaway contestant.  However, since most machine learning algorithms use numeric data, you want to change the personality types to the following numbers:
# - ISTJ - 1
# - ISTP - 2
# - ISFJ - 3
# - ISFP - 4
# - INFJ - 5
# - INFP - 6
# - INTJ - 7
# - INTP - 8
# - ESTP - 9
# - ESTJ - 10
# - ESFP - 11
# - ESFJ - 12
# - ENFP - 13
# - ENFJ - 14
# - ENTP - 15
# - ENTJ - 16
# - Missing values - 17
# 
# Save this new DataFrame as `Q14` and sort based on `castaway_id` in ascending order.

# In[47]:


castcopy2 = castaways.copy()
castcopy2['personality_type'].replace(['ISTJ', 'ISTP','ISFJ','ISFP','INFJ','INFP','INTJ','INTP','ESTP','ESTJ','ESFP','ESFJ','ENFP','ENFJ','ENTP','ENTJ'],
                                     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], inplace=True)
castcopy2['personality_type'] = castcopy2['personality_type'].fillna(17).astype(int)
castcopy2['personality_type'] = castcopy2['personality_type'].astype(int)
Q14 = castcopy2[['castaway_id','full_name','personality_type']].sort_values(by=['castaway_id'], ascending=True).reset_index(drop=True)
Q14


# #**Q15:** After thinking about this some more, you realize that you don't want to code the personality traits as you did in problem 14 since the data is not ordinal.  Some machine learning algorithms will assume that numbers close to each other are more alike than those that are away from each other and that is not the case with these personality types.
# 
# Let's create a new DataFrame called `Q15` that does the following: 
# - creates dummy columns (using `get_dummies`) for the original personality type column 
# - adds a prefix called "type"
# - drops the first column to help prevent multicollinearity
# - uses the `dtype=int` argument
# 
# The columns should be `castaway_id`, `full_name` followed by the various dummy columns for the personality types.  Don't worry about any missing values in this step.
# 
# Remember: Don't change any of the original DataFrames or CodeGrade will not work correctly for this assignment.  Make sure you use `copy()` if needed.

# In[48]:


### 

Q15 = castaway_details[['castaway_id', 'full_name', 'personality_type']].copy()

dummies = pd.get_dummies(Q15['personality_type'], prefix='type', dtype=int)
dummies = dummies.iloc[:, 1:]

Q15 = pd.concat([Q15[['castaway_id', 'full_name']], dummies], axis=1)
Q15



###


# **Q16:** After running your data above through your machine learning model, you determine that a better prediction might come from breaking the personality type into its four parts (one part for each character in the type).  Your task is now to create a DataFrame called `Q16` that splits the personality type into the various parts and creates a new column for each part (these columns should be called `interaction` that will represent the first letter in the personality type, `information` for the second letter, `decision` for the third, and `organization` for the fourth).
# 
# Again, since most machine learning algorithms work with numeric data, perform the following on the four new columns:
# - `interaction` --> code all `I`'s as `0` and `E`'s as `1`
# - `information` --> code all `S`'s as `0` and `N`'s as `1`
# - `decision` --> code all `T`'s as `0` and `F`'s as `1`
# - `organization` --> code as `J`'s with `0` and `P`'s as `1`
# - Any missing values should be coded with a `2`
# - Double check that all of the above columns are an integer type.  Some students have a problem with CodeGrade because one of their columns ends up being a string instead of an int.
# 
# For example, if a contestant's personality type was `ENTJ`, your columns for that row would be:
# - `1` for `interaction` because of the `E`
# - `1` for `information` because of the `N`
# - `0` for `decision` because of the `T` 
# - `0` for `organization` because of the `J`
# 
# The new DataFrame should be sorted in `castaway_id` order and have the following columns in this order: `castaway_id`, `full_name`, `personality_type`, `interaction`, `information`, `decision`, `organization`.
# 
# Remember: Don't change any of the original DataFrames or CodeGrade will not work correctly for this assignment.  Make sure you use `copy()` if needed.

# In[49]:


### 

Q16 = castaway_details[['castaway_id', 'full_name', 'personality_type']].copy()

def encode_personality_type(personality_type):
    interaction, information, decision, organization = 2, 2, 2, 2
    
    if pd.notnull(personality_type):  
        interaction = 0 if personality_type[0] == 'I' else 1
        information = 0 if personality_type[1] == 'S' else 1  
        decision = 0 if personality_type[2] == 'T' else 1     
        organization = 0 if personality_type[3] == 'J' else 1  
    
    return interaction, information, decision, organization

Q16[['interaction', 'information', 'decision', 'organization']] = Q16['personality_type'].apply(
    lambda x: pd.Series(encode_personality_type(x))
)

Q16[['interaction', 'information', 'decision', 'organization']] = Q16[['interaction', 'information', 'decision', 'organization']].astype(int)

Q16 = Q16.sort_values(by='castaway_id', ascending=True)
Q16 = Q16[['castaway_id', 'full_name', 'personality_type', 'interaction', 'information', 'decision', 'organization']]

Q16


###


# **Q17:** Using data from `castaways`, create a DataFrame called `Q17` that bins the contestant ages (their age when they were on the season, not their current age) into the following age categories:
# - 18-24
# - 25-34
# - 35-44
# - 45-54
# - 55-64
# - 65+
# 
# The final DataFrame should have the following columns in this order: `season`, `castaway_id`, `full_name`, `age`, and `age_category`.  The DataFrame should be sorted by age and then castaway_id.  The index should be 0 through n-1.  You should have the same amount of rows as in the `castaways` DataFrame.
# 
# Remember: Don't change any of the original DataFrames or CodeGrade will not work correctly for this assignment.  Make sure you use `copy()` if needed.

# In[51]:


Q17 = castaways.copy()

bins = [17, 25, 35, 45, 55, 65, 120]
labels = ['18-24','25-34','35-44','45-54','55-64','65+']

Q17['age_category'] = pd.cut(Q17['age'], bins=bins, labels=labels)

Q17 = Q17.sort_values(by=['age','castaway_id'])
Q17 = Q17.reset_index(drop=True)
Q17 = Q17[['season','castaway_id','full_name','age','age_category']]
Q17


# **Q18:** Based on the age categories you created above, what are the normalized percentages for the various age categories using `value_counts()`.  Sort the value counts by index.  Save this as `Q18`.

# In[55]:


Q18 = Q17['age_category'].value_counts(normalize=True).sort_index()
Q18


# #**Q19:** Which contestant(s) played a perfect game?  A perfect game is considered when the contestant:
# - didn't receive any tribal council votes all season (this is different than Q10 since some players played multiple times.  They got voted out in one season so they would not show in Q10 but they came back for another season and didn't receive any tribal council votes)
# - won the game
# - got unanimous jury votes (see question 12)
# 
# Save this DataFrame as `Q19` with the following columns: `season_name`, `season`, `castaway_id`, `full_name`, `tribal_council_votes`, `jury_votes`.  The DataFrame should be sorted by season and the index should be 0 to n-1.  Note that you may have to rename columns such as renaming the original `total_votes_received`column to `tribal_council_votes`.

# In[58]:


# Print column names to find the correct one for winners
print(castaways.columns)


# In[ ]:





# <span style="color:maroon;">This material is for enrolled students' academic use only and protected under U.S. Copyright Laws. This content must not be shared outside the confines of this course, in line with Eastern University's academic integrity policies. Unauthorized reproduction, distribution, or transmission of this material, including but not limited to posting on third-party platforms like GitHub, is strictly prohibited and may lead to disciplinary action. You may not alter or remove any copyright or other notice from copies of any content taken from BrightSpace or Eastern University’s website.</span>
# 
# <span style="color:maroon;"> © Copyright Notice 2024, Eastern University - All Rights Reserved </span>
