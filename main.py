#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime

import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import re
import datetime


# Load the datasets
dataset_path = r"E:\datamining\GooglePlay.csv"
dataSourceBase_path = r"E:\datamining\Playstore_final.csv"
df = pd.read_csv(dataset_path)
dfSource = pd.read_csv(dataSourceBase_path,low_memory=False)

def calculate_quality(attribute):
    null_counts = df[attribute].isnull().sum()
    record_numbers = len(df)
    alphanumeric_count = 0
    valid_count = 0  # Number of valid values
    numeric_count = 0  # Number of numeric values
    # Valid range for numeric data
    min_valid_numeric = 0
    max_valid_numeric = 100  # You can adjust this range as needed

    for value in df[attribute]:
        str_value = str(value)
        # Check if the data is of type object
        if str_value.isalpha():
            alphanumeric_count += 1
            # Check if the data contains alphanumeric characters
            if str_value.isalnum():
                valid_count += 1
        # Check if the data is numeric
        elif str_value.isdigit():
            numeric_count += 1
            numeric_value = int(str_value)
            # Check the valid range for numeric data
            if min_valid_numeric <= numeric_value <= max_valid_numeric:
                valid_count += 1

    completeness = 1 - (null_counts / record_numbers)
    # Calculate the validity of the data
    validity = valid_count / record_numbers
    currentness = None  # You need to define this for each specific attribute
    consistency = len(df[attribute].unique()) / record_numbers

    if (attribute == 'App'):
        accuracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Category'):
        accuracy = 0
        validity = 1
        currentness = 0
    elif (attribute == 'Rating'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in df['Rating']:
            if(isinstance(value, float)):
                if (value >= 0):
                    if(value <= 5):
                        v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Reviews'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in df['Reviews']: 
            if (value.isdigit()):
                if (int(value) >= 0):
                    if (int(value) <= 1000000):
                        v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Size'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in df['Size']:
            if (re.match(r'^.*M$', str(value))):
                value = pd.to_numeric(str(value).replace('M', ''), errors='coerce')
                if (int(value) >= 20):
                    if (int(value) <= 100):
                        v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Installs'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in df['Installs']:
            if (str(value).endswith("+")):
                value = str(value).replace('+', '')
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Type'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in df['Type']:
            if(value == 'Free'):
                v_count += 1
            elif(value == 'Paid'):
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Price'):    
        accuracy = 0
        currentness = 0
        v_count =0
        for value in df['Price']:
            if (str(value).startswith("$")):
                value = str(value).replace('$', '')
                v_count += 1
            elif(value == '0'):
                v_count +=1
        validity = v_count / record_numbers
    elif (attribute == 'Content Rating'):
        accuracy = 0
        currentness = 0
        v_count=df[attribute].isin(['Everyone', 'Teen', 'Mature 17+']).sum()
        validity = v_count / record_numbers
    elif (attribute == 'Genres'):
        accuracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Last Updated'): 
        accuracy = 0
        currentness = calculate_last_updated_currentness()
        v_count = 0
        for value in df['Last Updated']:
            try:
                datetime.datetime.strptime(value, "%d-%b-%y")
                v_count += 1
            except ValueError:
               pass
        validity = v_count/record_numbers
    elif (attribute == 'Current Ver'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in df['Current Ver']:
            if (value == 'Varies with device'):
                v_count += 1
        validity =  (record_numbers - v_count) / record_numbers
    elif (attribute == 'Android Ver'):  
        currentness = 0
        v_count = 0
        for value in df['Android Ver']:
            if (value == 'Varies with device'):
                v_count += 1
        validity =  (record_numbers - v_count) / record_numbers

    accuracy = validity + null_counts/record_numbers
    return record_numbers, null_counts, accuracy, completeness, validity, currentness, consistency

def calculate_last_updated_currentness():
    current_date = datetime.date.today()
    acceptable_year = 18
    total_days = 0
    valid_dates = 0

    month_dict = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    for value in df['Last Updated']:
        try:
            # Extract day, month, and year from the string
            day, month, year = value.split('-')
            month_number = month_dict.get(month)  # Get the corresponding month number

            # Create a datetime object using the extracted values
            last_updated_date = datetime.date(int(year), month_number, int(day))

            days_elapsed = (current_date - last_updated_date).days
            total_days += days_elapsed
            if (int(year) >= acceptable_year):
                valid_dates += 1
        except (ValueError, KeyError):
            pass

        currentness = (valid_dates / len(df))
        return currentness


# Define the list of attributes
attributes = ['App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price',
              'Content Rating', 'Genres', 'Last Updated', 'Current Ver', 'Android Ver']

# Create a dictionary to store the quality measures for each attribute
quality_measures = []

# Calculate quality measures for each attribute
for attribute in attributes:
    measures = calculate_quality(attribute)
    quality_measures.append([attribute] + list(measures))

# Print the quality measures as a table
headers = ['Attribute', 'Record Counts', 'Null Counts', 'Accuracy', 'Completeness', 'Validity', 'Currentness', 'Consistency']
print(tabulate(quality_measures, headers=headers, tablefmt='grid'))


# In[7]:


def calculate_quality(attribute):
    null_counts = dfSource[attribute].isnull().sum()
    record_numbers = len(dfSource)
    alphanumeric_count = 0
    valid_count = 0  # Number of valid values
    numeric_count = 0  # Number of numeric values
    # Valid range for numeric data
    min_valid_numeric = 0
    max_valid_numeric = 100  # You can adjust this range as needed

    for value in dfSource[attribute]:
        str_value = str(value)
        # Check if the data is of type object
        if str_value.isalpha():
            alphanumeric_count += 1
            # Check if the data contains alphanumeric characters
            if str_value.isalnum():
                valid_count += 1
        # Check if the data is numeric
        elif str_value.isdigit():
            numeric_count += 1
            numeric_value = int(str_value)
            # Check the valid range for numeric data
            if min_valid_numeric <= numeric_value <= max_valid_numeric:
                valid_count += 1

    completeness = 1 - (null_counts / record_numbers)
    # Calculate the validity of the data
    validity = valid_count / record_numbers
    currentness = None  # You need to define this for each specific attribute
    consistency = len(dfSource[attribute].unique()) / record_numbers

    if (attribute == 'App Name'):
        accuracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'App Id'):
        accuracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Category'):
        accuracy = 0
        validity = 1
        currentness = 0
    elif (attribute == 'Rating'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Rating']:
            if (isinstance(value, float)):
                if (value >= 0):
                    if (value <= 5):
                        v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Rating Count'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Rating Count']:
            if str(value) != 'N/A':  # ???????????????????????????????????????????????????????????????????????????????????
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Reviews'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Reviews']:
            if isinstance(value, str) and value.isdigit():
                if int(value) >= 0 and int(value) <= 1000000:
                    v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Size'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Size']:
            if isinstance(value, str) and re.match(r'^.*M$', value):
                value = pd.to_numeric(value.replace('M', ''), errors='coerce')
                if not pd.isna(value) and int(value) >= 20:
                    v_count += 1
        validity = v_count / record_numbers

    elif (attribute == 'Installs'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Installs']:
            if (str(value).endswith("+")):
                value = str(value).replace('+', '')
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Minimum Installs'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Minimum Installs']:
            if (isinstance(value, float)):
                if (value >= 5000):
                    if (value <= 5000000):
                        v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Free'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Free']: #????????????????????????????????????????????????????????????????????????????????
            if (str(value) == 'TRUE'):
                v_count += 1
            elif (str(value) == 'FALSE'):
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Price'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Price']:
            if (str(value).startswith("$")):
                value = str(value).replace('$', '')
                v_count += 1
            elif (value == '0'):
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Currency'):
        accuracy = 0
        currentness = 0
        v_count = 0
        if(value == 'USD'):
            v_count += 1
        validity = v_count / record_numbers # the result is weird!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    elif (attribute == 'Content Rating'):
        accuracy = 0
        currentness = 0
        v_count = dfSource[attribute].isin(['Everyone', 'Teen', 'Mature 17+']).sum()
        validity = v_count / record_numbers
    elif (attribute == 'Last update'):
        accuracy = 0
        currentness = calculate_last_updated_currentness()
        v_count = 0
        for value in dfSource['Last update']:
            try:
                datetime.datetime.strptime(value, "%d-%b-%y")
                v_count += 1
            except ValueError:
                pass
        validity = v_count / record_numbers
    elif (attribute == 'Verion'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Version']:
            if (value == 'Varies with device'):
                v_count += 1
        validity = (record_numbers - v_count) / record_numbers
    elif (attribute == 'Android version Text'):
        currentness = 0
        v_count = 0
        for value in dfSource['Android version Text']:
            if (value == 'Varies with device'):
                v_count += 1
        validity = (record_numbers - v_count) / record_numbers
    elif (attribute == 'Minimum Android'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Minimum Android']:
            if (value == 'Varies with device'):
                v_count += 1
            elif (str(value).startswith('3')):
                v_count += 1
            elif (str(value).startswith('5')):
                v_count += 1
        validity = (record_numbers - v_count) / record_numbers
    elif (attribute == 'Developer Id'):
        accuaracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Developer Website'):
        accuracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Developer Website']:
            if str(value).startswith('h'):
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Developer Email'):
        accuaracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Released'):
        accuaracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Released']:
            try:
                datetime.datetime.strptime(str(value), "%d-%b-%y")
                v_count += 1
            except  ValueError:
               pass
        validity = v_count/record_numbers
    elif (attribute == 'Last update'):
        accuracy = 0
        currentness = calculate_last_updated_currentness()
        v_count = 0
        for value in dfSource['Last update']:
            try:
                datetime.datetime.strptime(value, "%d-%b-%y")
                v_count += 1
            except ValueError:
               pass
        validity = v_count/record_numbers
    elif (attribute == 'Privacy Policy'):
        accuaracy = 0
        currentness = 0
        v_count = 0
        for value in dfSource['Privacy Policy']:
            if str(value).startswith('h'):
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Ad Supported'):
        accuaracy = 0
        currentness = 0
        v_count=0
        for value in dfSource['Ad Supported']:#????????????????????????????????????????????
            if str(value)=="TRUE" or str(value)=="FALSE":
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'In app purchases'):
        accuaracy = 0
        currentness = 0
        v_count=0
        for value in dfSource['In app purchases']:#????????????????????????????????????????????
            if str(value)=="TRUE" or str(value)=="FALSE":
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Editor Choice'):
        accuaracy = 0
        currentness = 0
        v_count=0
        for value in dfSource['Editor Choice']:#????????????????????????????????????????????
            if str(value)=="TRUE" or str(value)=="FALSE":
                v_count += 1
        validity = v_count / record_numbers
    elif (attribute == 'Summary'):
        accuaracy = 0
        currentness = 0
        validity = 1

    elif (attribute == 'Developer'):
        accuaracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Developer Address'):
        accuaracy = 0
        currentness = 0
        validity = 1
    elif (attribute == 'Developer Internal ID'):
        accuaracy = 0
        currentness = 0
        validity = 1

    accuracy = validity + null_counts / record_numbers
    return record_numbers, null_counts, accuracy, completeness, validity, currentness, consistency


def calculate_last_updated_currentness():
    current_date = datetime.date.today()
    acceptable_year = 18
    total_days = 0
    valid_dates = 0

    month_dict = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    for value in dfSource['Last update']:
        try:
            # Extract day, month, and year from the string
            day, month, year = value.split('-')
            month_number = month_dict.get(month)  # Get the corresponding month number

            # Create a datetime object using the extracted values
            last_updated_date = datetime.date(int(year), month_number, int(day))

            days_elapsed = (current_date - last_updated_date).days
            total_days += days_elapsed
            if (int(year) >= acceptable_year):
                valid_dates += 1
        except (ValueError, KeyError):
            pass

        currentness = (valid_dates / len(dfSource))
        return currentness


# Define the list of attributes
attributes = ['App Name', 'App Id', 'Category', 'Rating', 'Rating Count', 'Reviews', 'Size', 'Installs',
              'Minimum Installs', 'Free', 'Price', 'Currency',
              'Content Rating', 'Last update', 'Version', 'Android version Text', 'Minimum Android',
              'Developer Id', 'Developer Website', 'Developer Email','Released','Last update','Privacy Policy','Content Rating','Ad Supported','In app purchases','Editor Choice','Summary','Reviews','Android version Text','Developer','Developer Address','Developer Internal ID','Version']

# Create a dictionary to store the quality measures for each attribute
quality_measures = []

# Calculate quality measures for each attribute
for attribute in attributes:
    measures = calculate_quality(attribute)
    quality_measures.append([attribute] + list(measures))

# Print the quality measures as a table
headers = ['Attribute', 'Record Counts', 'Null Counts', 'Accuracy', 'Completeness', 'Validity', 'Currentness',
           'Consistency']
print(tabulate(quality_measures, headers=headers, tablefmt='grid'))


# In[16]:


# Numeric features analysis
numeric_features = ['Rating', 'Reviews', 'Size', 'Installs', 'Price']
table = {
    "Name": [],
    "Type": [],
    "Range": [],
    "Min": [],
    "Max": [],
    "Mean": [],
    "Mode": [],
    "Median": [],
    "Outlier": []
}
dataFrame = pd.DataFrame(table)
for column in numeric_features:
    if column == 'Installs':
        df['Installs'] = df['Installs'].str.replace('+', '')
        df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    elif column == 'Size':
        df['Size'] = df['Size'].replace('Varies with device', '')
        df['Size'] = pd.to_numeric(df['Size'].str.replace('M', ''), errors='coerce')
    elif column == 'Reviews':
        df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    elif column == 'Price':
        df['Price'] = df['Price'].str.replace('$', '')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    median_value = df[column].median()
    type_value = df[column].dtype
    mode_value = df[column].mode()[0]
    mean_value = df[column].mean()
    max_value = df[column].max()
    min_value = df[column].min()
    data_range = max_value - min_value
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    outliers_count = len(outliers)

    new_row = pd.DataFrame({
        "Name": [column],
        "Type": [type_value],
        "Range": [data_range],
        "Min": [min_value],
        "Max": [max_value],
        "Mean": [mean_value],
        "Mode": [mode_value],
        "Median": [median_value],
        "Outlier": [outliers_count]
    })
    #dataFrame = pd.concat([dataFrame, new_row], ignore_index=True)

headers = ['Name', 'Type', 'Range', 'Min', 'Max', 'Mean', 'Mode', 'Median', 'Outliers']
#print(tabulate(dataFrame, headers=headers, tablefmt='grid'))

#for column in numeric_features:
 #   plt.figure(figsize=(8, 6))
  #  df.boxplot(column=[column])
   # plt.title(f"Box Plot of {column}")
    #plt.ylabel("Values")
    #plt.show()

