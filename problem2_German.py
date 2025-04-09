#code for problem2_German.py 

#PREPROCESSING

import pandas as pd
import matplotlib.pyplot as plt

df_german = pd.read_csv("GermanCredit.csv")
df_german.columns


#Drop the 3 columns that contribute the least to the dataset. 
#These would be the columns with the highest number of non-zero 'none' values. 
#Break ties by going left to right in columns. 
#(Your code should be generalizable to drop n columns, but for the rest of the analysis, 
# you can call your code for n=3.)


def drop_top_n_none_columns(df_german, n):
    col_with_none = {}

   
    for idx, col in enumerate(df_german.columns):
        none_count = (df_german[col] == 'none').sum()
        if none_count > 0:
            col_with_none[col] = (none_count, idx)
            
    
    sorted_cols = sorted(col_with_none.items(), key=lambda item: (-item[1][0], item[1][1]))
    cols_to_drop = [col for col, _ in sorted_cols[:n]]
    df_german.drop(columns=cols_to_drop,inplace=True)


drop_top_n_none_columns(df_german,3)
df_german.head()


#Certain values in some of the columns contain unnecessary apostrophes (‘). Remove the apostrophes

df_german = df_german.replace("'", "", regex=True)
df_german.head()


#The checking_status column has values in 4 categories: 'no checking', '<0', '0<=X<200', and '>=200'.
#Change these to 'No Checking', 'Low', 'Medium', and 'High' respectively.

mapping1 = {
    'no checking': 'No Checking',
    '<0': 'Low',
    '0<=X<200': 'Medium',
    '>=200': 'High'
}

df_german['checking_status'] = df_german['checking_status'].replace(mapping1)
df_german.head()


#The savings_status column has values in 4 categories: 'no known savings', '<100', '100<=X<500', '500<=X<1000', and '>=1000'. 
#Change these to 'No Savings', 'Low', 'Medium', 'High', and 'High' respectively. (Yes, the last two are both 'High').

mapping2 = {

    'no known savings' : 'No Savings',
    '<100' : 'Low',
    '100<=X<500' : 'Medium',
    '500<=X<1000': 'High',
    '>=1000': 'High'

}

df_german["savings_status"] = df_german["savings_status"].replace(mapping2)
df_german.head()


#Change class column values from 'good' to '1' and 'bad' to '0'.

mapping3 = {

    'good' : '1',
    'bad' : '0'

}

df_german["class"] = df_german["class"].replace(mapping3)
df_german.head()


#Change the employment column value 'unemployed' to 'Unemployed', 
#and for the others, change to 'Amateur', 'Professional', 'Experienced' and 'Expert', depending on year range.

df_german["employment"].unique()
mapping4 = {
    'unemployed' : 'Unemployed',
    '<1' : 'Amateur',
    '1<=X<4' : 'Professional',
    '4<=X<7' : 'Experienced',
    '>=7' : 'Expert'

}

df_german["employment"] = df_german["employment"].replace(mapping4)
df_german.head()


#ANALYSIS


#Get the count of each category of foreign workers (yes and no) for each class of credit (good and bad).

crosstab_result = pd.crosstab(df_german['foreign_worker'], df_german['class'])
crosstab_result

#Similarly, get the count of each category of employment for each category of saving_status.
crosstab_result = pd.crosstab(df_german['employment'], df_german['savings_status'])
crosstab_result


#Find the average credit_amount of single males that have 4<=X<7 years of employment. 
#You can leave the raw result as is, no need for rounding

#personal_status, credit_amount, employment

single_males_df = df_german[df_german["personal_status"]== "male single"]
experienced_males_df = single_males_df[single_males_df["employment"] == "Experienced"]
experienced_males_df_avg = experienced_males_df["credit_amount"].mean()
experienced_males_df_avg


#Find the average credit duration for each of the job types. You can leave the raw result as is, no need for rounding.

df_german["job"].unique()
for job in df_german["job"].unique():
    avg_credit = df_german[df_german["job"] == job]["duration"].mean()
    print(f"{job} = {avg_credit}")



#For the purpose 'education', what is the most common checking_status and savings_status? Your code should print:

#Most common checking status: ...
#Most common savings status: ...


education_df = df_german[df_german["purpose"] == "education"]
education_df.head(5)


highest_checking = education_df["checking_status"].value_counts().iloc[0]
print(f" Most common checking status: {highest_checking}")

highest_savings = education_df["savings_status"].value_counts().iloc[0]
print(f" Most common savings status: {highest_savings}")



#VISUALIZATION


#Plot subplots of two bar charts: one for savings_status (x-axis) to 
#personal status (y-axis), and another for checking_status (x-axis) to personal_status (y-axis). 
#In each of the charts, each personal status category bar (number of people in that category) should be of a different color.


savings_vs_personal = pd.crosstab(df_german['savings_status'], df_german['personal_status'])
checking_vs_personal = pd.crosstab(df_german['checking_status'], df_german['personal_status'])

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

savings_vs_personal.plot(kind='bar', ax=axes[0])
axes[0].set_title('Savings Status vs Personal Status')
axes[0].set_xlabel('Savings Status')
axes[0].set_ylabel('Number of People')
axes[0].legend(title='Personal Status')


checking_vs_personal.plot(kind='bar', ax=axes[1])
axes[1].set_title('Checking Status vs Personal Status')
axes[1].set_xlabel('Checking Status')
axes[1].legend(title='Personal Status')

plt.tight_layout()
plt.show()



#For people having credit_amount more than 4000, plot a bar graph which maps 
#property_magnitude (x-axis) to the average customer age for that magnitude (y-axis)



high_credit_df = df_german[df_german['credit_amount'] > 4000]

avg_age_by_property = high_credit_df.groupby('property_magnitude')['age'].mean()
print(avg_age_by_property)

avg_age_by_property.plot(kind='bar')


plt.xlabel('Property Magnitude')
plt.ylabel('Average Age')
plt.title('Average Age by Property Magnitude (Credit > 4000)')
plt.show()



#For people with a "High" savings_status and age above 40, use subplots to plot the following pie charts:
#Personal status
#Credit history
#Job


#did some formstting of pie to make it look better (for myself))

filtered_df = df_german[(df_german['savings_status'] == 'High') & (df_german['age'] > 40)]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))


# Personal status
filtered_df['personal_status'].value_counts().plot.pie(
    ax=axes[0], autopct='%1.1f%%', startangle=90, title='Personal Status'
)

# Credit history
filtered_df['credit_history'].value_counts().plot.pie(
    ax=axes[1], autopct='%1.1f%%', startangle=90, title='Credit History'
)

# Job
filtered_df['job'].value_counts().plot.pie(
    ax=axes[2], autopct='%1.1f%%', startangle=90, title='Job'
)

for ax in axes:
    ax.set_ylabel('')  

plt.tight_layout()
plt.show()














