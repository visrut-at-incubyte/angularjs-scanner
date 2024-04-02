### ------------------------------ BOX PLOT -----------------------------------

import pandas as pd

# Load the CSV file to examine its contents
df = pd.read_csv('/mnt/data/codebase.csv')

# Display the first few rows of the dataframe to understand its structure
df.head()

import matplotlib.pyplot as plt
import seaborn as sns

# Since the user requested to use only 'type' and 'loc' columns for the box chart
# and to avoid paths, we proceed to create the box chart accordingly.

plt.figure(figsize=(10, 6))
sns.boxplot(x='type', y='loc', data=df)
plt.title('Box Chart of LOC by Type')
plt.xlabel('Type')
plt.ylabel('LOC (Lines of Code)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


### ------------------------------ PROPOTION PLOT -----------------------------------

# Define the function for categorizing effort based on the provided logic
def categorize_effort(row, mean, std):
    if row < mean - 0.5 * std:
        return 'Very Low Effort'
    elif mean - 0.5 * std <= row < mean:
        return 'Low Effort'
    elif mean <= row < mean + 0.5 * std:
        return 'Medium Effort'
    else:
        return 'High Effort'

# Apply the function to categorize effort for each 'loc' within its 'type'
df['Effort'] = df.groupby('type')['loc'].transform(lambda x: x.apply(categorize_effort, args=(x.mean(), x.std())))

# Count the number of files in each effort category by type
effort_counts = df.groupby(['type', 'Effort']).size().unstack(fill_value=0)

# Normalize the counts to get proportions
effort_proportions = effort_counts.div(effort_counts.sum(axis=1), axis=0)

# Plotting the stacked bar chart for the proportion of files by effort category and component type
plt.figure(figsize=(12, 8))
effort_proportions.plot(kind='bar', stacked=True)
plt.title('Proportion of Files by Effort Category and Component Type')
plt.xlabel('Component Type')
plt.ylabel('Proportion of Files')
plt.legend(title='Effort Category')
plt.grid(axis='y')
plt.show()


### ------------------------------ CDF PLOT -----------------------------------

import numpy as np

# Correcting the code for generating a CDF plot
plt.figure(figsize=(12, 8))

# Iterate over each unique type in the dataframe to plot the CDF
for component_type in df['type'].unique():
    # Filter LOC values by component type and sort them
    loc_values = df[df['type'] == component_type]['loc'].sort_values()
    
    # Generate CDF values for the sorted LOC values
    cdf = np.arange(1, len(loc_values) + 1) / len(loc_values)
    
    # Plotting the CDF for each type
    plt.plot(loc_values, cdf, label=component_type)

plt.title('Cumulative Distribution of LOC by Component Type')
plt.xlabel('Lines Of Code (LOC)')
plt.ylabel('CDF (Percentage of Files)')
plt.grid(True)
plt.legend()
plt.show()
