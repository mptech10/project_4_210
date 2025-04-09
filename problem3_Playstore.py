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


DID NOT COMPLETE YET!!! Still figuring it out 
