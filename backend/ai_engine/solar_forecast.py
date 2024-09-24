import os
import pandas as pd

# Formula coefficients (you can adjust these based on your model)
alpha = 0.5   # Coefficient for solar radiation
beta = 0.3    # Coefficient for carbon footprint
gamma = 0.2   # Coefficient for electricity demand
delta = 0.1   # Coefficient for cloud coverage
epsilon = 0.4 # Coefficient for solar energy supply

# Function to calculate the dynamic price
def calculate_price(solar_radiation, carbon_footprint, electricity_demand, cloud_coverage, solar_energy_supply):
    # Avoid division by zero for solar radiation (assume minimum radiation is 0.01 kW/m²)
    if solar_radiation <= 0:
        solar_radiation = 0.01

    # Formula for dynamic pricing
    price = (alpha * (1 / solar_radiation)) + (beta * carbon_footprint) + (gamma * electricity_demand) \
            + (delta * cloud_coverage) - (epsilon * solar_energy_supply)
    
    return round(price, 4)  # Return price rounded to 4 decimal places

# Path to the dataset directory
dataset_directory = './dataset/data.csv'  # Point to the specific dataset file
csv_file = None

# Try to find a CSV file in the dataset directory
try:
    files = os.listdir(dataset_directory)
    for file in files:
        if file.endswith('.csv'):
            csv_file = file
            break
except FileNotFoundError:
    print(f"Directory {dataset_directory} not found.")
    exit()

# Check if a CSV file was found
if csv_file:
    file_path = os.path.join(dataset_directory, csv_file)

    # Read the CSV dataset
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully.")
    except Exception as e:
        print(f"Error reading dataset: {e}")
        exit()

    # Calculate the dynamic price for each row in the dataset
    df['Predicted Price ($/kWh)'] = df.apply(lambda row: calculate_price(
        solar_radiation=row['Solar Radiation (kW/m²)'],
        carbon_footprint=row['Carbon Footprint (kgCO₂)'],
        electricity_demand=row['Electricity Demand (kWh)'],
        cloud_coverage=row['Cloud Coverage (%)'],
        solar_energy_supply=row['Energy Supply from Solar (kWh)']
    ), axis=1)

    # Display the updated dataset with predicted price
    print(df[['Date', 'Time', 'Predicted Price ($/kWh)']].head())

else:
    print("No CSV file found in the dataset directory.")