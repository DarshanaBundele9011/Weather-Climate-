import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Generate random weather data
num_days = 365  # One year of data
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami"]
weather_conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy"]

data = []
start_date = datetime(2023, 1, 1)

for i in range(num_days):
    for city in cities:
        date = start_date + timedelta(days=i)
        avg_temp = round(random.uniform(-5, 35), 1)  # Avg temperature in °C
        max_temp = avg_temp + round(random.uniform(1, 5), 1)
        min_temp = avg_temp - round(random.uniform(1, 5), 1)
        humidity = round(random.uniform(30, 90), 1)  # Percentage
        rainfall = round(random.uniform(0, 50), 1) if random.random() < 0.3 else 0  # mm
        snowfall = round(random.uniform(0, 20), 1) if avg_temp < 0 else 0  # cm
        wind_speed = round(random.uniform(5, 40), 1)  # km/h
        condition = random.choice(weather_conditions)

        data.append([date.strftime('%Y-%m-%d'), city, avg_temp, max_temp, min_temp,
                     humidity, rainfall, wind_speed, snowfall, condition])

# Create DataFrame
df = pd.DataFrame(data, columns=["Date", "City", "Average Temperature (°C)", "Max Temperature (°C)",
                                 "Min Temperature (°C)", "Humidity (%)", "Rainfall (mm)", "Wind Speed (km/h)",
                                 "Snowfall (cm)", "Weather Condition"])

# Data Cleaning
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Save cleaned data to Excel
excel_filename = "weather_data.xlsx"
df.to_excel(excel_filename, index=False)
print(f"Cleaned dataset saved as {excel_filename}")

# Visualizations (displayed instead of saving to PDF)

# 1. Temperature Trends Over Time
"""plt.figure(figsize=(12, 6))
plt.title("Temperature Trends Over Time")
for city in cities:
    city_data = df[df["City"] == city]
    plt.plot(city_data["Date"], city_data["Average Temperature (°C)"], label=city)
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.show()"""
plt.figure(figsize=(12, 6))

# Main Title
plt.suptitle("Weather Data Analysis", fontsize=18, fontweight="bold")

# Subheading
plt.title("Temperature Trends Over Time (Top 10 Records)", fontsize=14)

# Get top 10 rows
df_top10 = df.groupby("City").head(10)  # Selecting top 10 records per city

for city in cities:
    city_data = df_top10[df_top10["City"] == city]
    plt.plot(city_data["Date"], city_data["Average Temperature (°C)"], label=city, marker='o')

plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid()
plt.show()


# 2. Humidity vs. Temperature Scatter Plot
#plt.figure(figsize=(8, 6))
#sns.scatterplot(data=df, x="Average Temperature (°C)", y="Humidity (%)", hue="City")
#plt.title("Humidity vs. Temperature")
#plt.show()

# Filter the top 10 records per city
df_top10 = df.groupby("City").head(10)

# 2. Humidity vs. Temperature Scatter Plot (Top 10 Records)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_top10, x="Average Temperature (°C)", y="Humidity (%)", hue="City")
plt.title("Humidity vs. Temperature (Top 10 Records)")
plt.show()



# 3. Rainfall Distribution by City
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x="City", y="Rainfall (mm)", estimator=np.mean)
plt.title("Average Rainfall Distribution by City")
plt.show()

# 4. Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df.drop(columns=["Date", "City", "Weather Condition"]).corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix of Weather Factors")
plt.show()

# 5. Wind Speed & Rainfall Impact Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="City", y="Wind Speed (km/h)", hue="Weather Condition")
plt.title("Wind Speed Distribution by Weather Condition")
plt.xticks(rotation=45)
plt.show()

# 6. Top 5 Max Temperatures
top_max_temps = df.nlargest(5, "Max Temperature (°C)")
plt.figure(figsize=(8, 6))
sns.barplot(data=top_max_temps, x="City", y="Max Temperature (°C)", hue="Weather Condition")
plt.title("Top 5 Maximum Temperatures")
plt.show()

# 7. Top 5 Min Temperatures
top_min_temps = df.nsmallest(5, "Min Temperature (°C)")
plt.figure(figsize=(8, 6))
sns.barplot(data=top_min_temps, x="City", y="Min Temperature (°C)", hue="Weather Condition")
plt.title("Top 5 Minimum Temperatures")
plt.show()

# 8. Monthly Average Temperature Trends
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime('%Y-%m')
monthly_avg_temp = df.groupby(["Month", "City"])["Average Temperature (°C)"].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_avg_temp, x="Month", y="Average Temperature (°C)", hue="City", marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Average Temperature Trends")
plt.show()

# 9. Weather Condition Distribution (Pie Chart)
plt.figure(figsize=(8, 8))
df["Weather Condition"].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='viridis')
plt.title("Weather Condition Distribution")
plt.ylabel("")
plt.show()




# Top 5 Humidity Levels
plt.figure(figsize=(10, 5))
top_humidity = df.nlargest(5, "Humidity (%)")
sns.barplot(data=top_humidity, x="City", y="Humidity (%)", hue="City")
plt.title("Top 5 Humidity Levels")
plt.show()

# Top 5 Rainfall Amounts
plt.figure(figsize=(10, 5))
top_rainfall = df.nlargest(5, "Rainfall (mm)")
sns.barplot(data=top_rainfall, x="City", y="Rainfall (mm)", hue="City")
plt.title("Top 5 Rainfall Amounts")
plt.show()

# Top 5 Snowfall Amounts
plt.figure(figsize=(10, 5))
top_snowfall = df.nlargest(5, "Snowfall (cm)")
sns.barplot(data=top_snowfall, x="City", y="Snowfall (cm)", hue="City")
plt.title("Top 5 Snowfall Amounts")
plt.show()

# Top 5 Wind Speeds
plt.figure(figsize=(10, 5))
top_windspeed = df.nlargest(5, "Wind Speed (km/h)")
sns.barplot(data=top_windspeed, x="City", y="Wind Speed (km/h)", hue="City")
plt.title("Top 5 Wind Speeds")
plt.show()



