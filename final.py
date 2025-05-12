# COVID-19 Global Data Analysis Notebook
# File: covid_global_tracker.ipynb


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

try:
    # Load dataset from Our World in Data
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url, parse_dates=['date'])
    
    # Check essential columns
    required_cols = ['date', 'location', 'total_cases', 'total_deaths', 'new_cases', 'people_vaccinated']
    assert all(col in df.columns for col in required_cols), "Missing required columns"
    
except Exception as e:
    print(f"Error loading data: {str(e)}")
    raise


# Select key countries
countries = ['Kenya', 'United States', 'India', 'Germany', 'Brazil']
df_filtered = df[df['location'].isin(countries)].copy()

# Handle missing values
df_filtered['total_cases'] = df_filtered['total_cases'].fillna(0)
df_filtered['total_deaths'] = df_filtered['total_deaths'].fillna(0)
df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases'].replace(0, 1)


# Time series analysis
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_filtered, x='date', y='total_cases', hue='location')
plt.title('COVID-19 Cases Evolution')
plt.ylabel('Total Cases')
plt.xlabel('Date')
plt.show()

# Death rate comparison
latest_data = df_filtered[df_filtered['date'] == df_filtered['date'].max()]
plt.figure(figsize=(10, 6))
sns.barplot(data=latest_data, x='location', y='death_rate')
plt.title('Current Death Rate by Country')
plt.ylabel('Death Rate (%)')
plt.xticks(rotation=45)
plt.show()


# Vaccination progress
vacc_df = df_filtered.dropna(subset=['people_vaccinated'])
plt.figure(figsize=(12, 6))
sns.lineplot(data=vacc_df, x='date', y='people_vaccinated', hue='location')
plt.title('Vaccination Rollout Progress')
plt.ylabel('People Vaccinated')
plt.show()


# Create global map
world_df = df[df['date'] == df['date'].max()]
fig = px.choropleth(world_df, 
                    locations="iso_code",
                    color="total_cases",
                    hover_name="location",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Global COVID-19 Case Distribution")
fig.show()

