#code for problem3_Playstore.py 


import pandas as pd


google_df = pd.read_excel("GooglePlaystore.xlsx")
google_df.head()


#Often there are outliers which do not match the overall data type. There is one record in this data where the "Reviews" has value "3.0M" which does not match the rest of the data. Remove that record.

google_index = google_df[google_df["Reviews"] == "3.0M"].index
google_df = google_df.drop(google_index)


#Double check
google_df[google_df["Reviews"] == "3.0M"]


#Remove rows where any of the columns has the value "Varies with device".

google_df = google_df[~google_df.isin(["Varies with device"]).any(axis=1)]
google_df


#The values in the Android version column should be floats. 
#Strip the trailing non-numeric characters from all values (ie. the words " and up"), so the result is a number. 
#If there are multiple decimal places (eg. "x.y.z"), keep only the first two parts (eg "x.y"). 
#For example, the value "4.1 and up" should be changed to "4.1". 
#The value "4.5.6 and up" should be changed to "4.5". 
#The value "5.6.7" should be changed to "5.6".


#DID NOT COMPLETE YET!!! Still figuring it out 
import re

# andrroid CLEANING preprocess
def clean_android_version(val):
    if pd.isna(val):
        return None
    val = str(val)
    
    # REGEX look up regex again
    val = val.split('-')[0].strip()
    
    # "and up"
    val = re.sub(r'[^0-9\.]', '', val)
    
    # correct decimal formatting FITHT TRY
    parts = val.split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    elif len(parts) == 1:
        return parts[0]
    else:
        return None

google_df["Android Ver"] = google_df["Android Ver"].apply(clean_android_version)
google_df

# Clean installs column: remove commas and '+'; keep valid integers only
def clean_installs(val):
    if pd.isna(val):
        return None
    val = str(val).replace(",", "").replace("+", "")
    return val if val.isdigit() else None

google_df["Installs"] = google_df["Installs"].apply(clean_installs)

# Drop rows with invalid installs
google_df = google_df[google_df["Installs"].notna()]
google_df["Installs"] = google_df["Installs"].astype(int)
google_df


# 1. Handle missing rating values
# If reviews < 100 and installs < 50000, remove the row
# Otherwise, fill with average rating for that category

missing_ratings = google_df['Rating'].isna()

# reviews < 100 AND installs < 50000
remove_condition = (google_df['Reviews'].astype(float) < 100) & (google_df['Installs'] < 50000)

# remove: missing rating AND meets the removal condition
rows_to_remove = missing_ratings & remove_condition

# remove
google_df = google_df[~rows_to_remove]

#  average rating by category (rounded to 2 decimal places)
category_avg_rating = google_df.groupby('Category')['Rating'].mean().round(2)

for category in google_df['Category'].unique():
    category_mask = (google_df['Category'] == category) & (google_df['Rating'].isna())
    google_df.loc[category_mask, 'Rating'] = category_avg_rating[category]

google_df

# Convert Size values to integers (M to millions, K to thousands)
# Using .loc to avoid the SettingWithCopyWarning
#CONFUSING......... FIX THIS LATER. REMINDER: WHY DO WE GET THAT WARNING? TRY WITHOUT WARNING FIX, ALSO WHY DOES RATINGS BECOME NAN AGAIN

def convert_size_to_int(size):
    
    size = str(size).strip()
    
    #  M to millions
    if 'M' in size:
        try:
            return int(float(size.replace('M', '')) * 1000000)
        except ValueError:
            return None
    
    #  k to thousands
    elif 'k' in size:
        try:
            return int(float(size.replace('k', '')) * 1000)
        except ValueError:
            return None
    
    elif size.isdigit():
        return int(size)
    
    return None




#WEIRD WARNING STUFF:
# Create a copy of the DataFrame to ensure we're not working with a view
google_df = google_df.copy()

# Apply the conversion using .loc to avoid the warning
google_df.loc[:, 'Size'] = google_df['Size'].apply(convert_size_to_int)

google_df



#start ANALYSIS here
# Describe category-wise rating statistics
# Group by Category and then use describe() on the Rating column

google_df['Rating'] = pd.to_numeric(google_df['Rating'], errors='coerce')

category_rating_stats = google_df.groupby('Category')['Rating'].describe()

category_rating_stats = category_rating_stats.round(2)

print("Category-wise Rating Statistics:")
category_rating_stats


free_apps = google_df[google_df['Type'] == 'Free'].copy()

def get_top3_by_category(df, column):
    sorted_df = df.sort_values(by=[column], ascending=False)
    
    top3 = sorted_df.groupby('Category').head(3)
    
    result = top3[['Category', 'App', column]]
    
    
    return result

# a. Top 3 most highly rated applications in each category
top3_rating = get_top3_by_category(free_apps, 'Rating')
print("Top 3 Apps by Rating for each Category:")
print(top3_rating.head(3))

# b. Top 3 most installed applications in each category
top3_installs = get_top3_by_category(free_apps, 'Installs')
print("\nTop 3 Apps by Installs for each Category:")
print(top3_installs.head(3))

# c. Top 3 most reviewed applications in each category
top3_reviews = get_top3_by_category(free_apps, 'Reviews')
print("\nTop 3 Apps by Reviews for each Category:")
print(top3_reviews.head(3))

paid_apps = google_df[google_df['Type'] == 'Paid']

avg_price = paid_apps['Price'].mean()
max_price = paid_apps['Price'].max()
min_price = paid_apps['Price'].min()

print(f"Paid Applications Price Statistics:")
print(f"Average Price: ${avg_price:.2f}")
print(f"Maximum Price: ${max_price:.2f}")
print(f"Minimum Price: ${min_price:.2f}")


# VISUALIZATIONNNN  TRY REMOVING THE COMMENTED OUT TOP 15 PARTS AND RUN TO SEE IF WE DONT GET WARNING OR ERROR

import matplotlib.pyplot as plt

google_df['Genres'] = google_df['Genres'].str.split(';')

# explode the DataFrame so each genre gets its own row
exploded_df = google_df.explode('Genres')

exploded_df['Genres'] = exploded_df['Genres'].str.strip()

genre_counts = exploded_df['Genres'].value_counts()

print("Number of Applications per Genre:")
print(genre_counts)  

plt.figure(figsize=(12, 8))

top_genres = genre_counts

plot_data = top_genres.copy()

# the pie chart
plt.pie(plot_data, labels=plot_data.index, autopct='%1.1f%%', 
        startangle=90, shadow=True)
plt.axis('equal')  
plt.title(f'Distribution of Applications by Genre')

plt.legend(plot_data.index, loc="best", bbox_to_anchor=(1, 0.5))

plt.show()


#LAST PART
import matplotlib.pyplot as plt

#  include only Business and Education categories
business_ratings = google_df[google_df['Category'] == 'BUSINESS']['Rating'].dropna()
education_ratings = google_df[google_df['Category'] == 'EDUCATION']['Rating'].dropna()


plt.figure(figsize=(10, 6))

# boxplot
boxplot = plt.boxplot([business_ratings, education_ratings], 
                      tick_labels=['BUSINESS', 'EDUCATION'],
                      patch_artist=True)


# title and labels
plt.title('Comparison of Ratings: Business vs Education Apps', fontsize=16)
plt.xlabel('Category', fontsize=14)
plt.ylabel('Rating', fontsize=14)

# gridlines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

#  y-axis limits to show full rating scale
plt.ylim(0, 5.5)

plt.tight_layout()
plt.show()
