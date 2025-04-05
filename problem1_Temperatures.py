#code for problem1_Temperatures 
import pandas as pd
import matplotlib.pyplot as plt
#loading the csv into a pandas df
df = pd.read_csv('EuCitiesTemperatures.csv')
#df.head #check

#preprocssing
#1: filling missng vals for lat and long
# missing latitudes
df['latitude'] = df['latitude'].fillna(df.groupby('country')['latitude'].transform(lambda x: round(x.mean(), 2)))

# missing longitudes
df['longitude'] = df['longitude'].fillna(df.groupby('country')['longitude'].transform(lambda x: round(x.mean(), 2)))

#PREPROCESSING 2:  Find out the subset of cities that lie between latitudes 40 to 60 (both inclusive) and longitudes 15 to 30 (both inclusive). 
#Find out which countries have the maximum number of cities in this geographical band. (More than one country could have the maximum number of values.)
# cities in the geographic band
band_df = df[(df['latitude'] >= 40) & (df['latitude'] <= 60) & (df['longitude'] >= 15) & (df['longitude'] <= 30)]

# count of the number of cities per country
country_counts = band_df['country'].value_counts()
max_count = country_counts.max()
countries_with_max = country_counts[country_counts == max_count]

countries_with_max

#PREPROOCRESSING 3:  Fill in the missing temperature values by the average temperature value of the similar region type. 
#A region type would be a combinaton of whether it is in EU (yes/no) and whether it has a coastline (yes/no).
#For example, if we have a missing temperature value for Bergen, Norway, which is not in the EU but lies on the coast, 
#we will fill it with the average temperature of cities with EU='no' and coastline='yes')

df['RegionType'] = df['EU'].astype(str) + '+' + df['coastline'].astype(str)

# average temperature per region type
region_avg_temp = df.groupby('RegionType')['temperature'].mean()

# filling in the missing temperature vals using region type average calculated
def fill_temp(row):
    if pd.isna(row['temperature']):
        return region_avg_temp[row['RegionType']]
    return row['temperature']

df['temperature'] = df.apply(fill_temp, axis=1)
# testing, delete later:      print("Missing temperatures left:", df['temperature'].isna().sum())


#VISUALIZATION 1 Plot a bar chart for the number of cities belonging to each of the regions described in Preprocessing/Analysis #3 above
# count of cities per region type... coastline yes or no
import matplotlib.pyplot as plt #idk if we need this here again, cuz it wasnt working without it in juptyer notebeook
region_counts = df['RegionType'].value_counts()

# bar chart
plt.figure(figsize=(7, 4))
region_counts.plot(kind='bar', color='lightblue')

plt.title('Number of Cities by Region Type (EU + Coastline)')
plt.xlabel('Region Type (EU+Coastline)')
plt.ylabel('Number of Cities')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()







