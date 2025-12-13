import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.ticker import FuncFormatter

dt1=pd.read_csv(r"C:\Users\fatemeh\OneDrive\Desktop\learning_pro\Cars_Datasets_2025.csv",encoding="cp1252")

#getting columns name
column_names=dt1.columns.tolist()
print(column_names)

#filing null spaces with not given
for col in dt1.columns:
    if not pd.api.types.is_numeric_dtype(dt1[col]):
        dt1[col] = dt1[col].fillna("not given")

#reading information but first converting numeric column into numeric values because most of them have string suffixes
#speed part
dt1["Total Speed"] = dt1["Total Speed"].str.extract(r"(\d+)")
#\d+ : Matches one or more digits (0–9)
dt1["Total Speed"] = pd.to_numeric(dt1["Total Speed"], errors='coerce')
# the errors='coerce' part tells Pandas how to handle values that can't be converted 
# into numbers.Converts unconvertible values to NaN (missing value)

#car prices
def parse_price(value):
    if isinstance(value, str):
        value = value.replace("$", "").replace(",", "").strip()
        # Check for hyphen or slash as a range separator
        if "-" in value or "/" in value:
            # below when you run this line, it checks whether the string contains a hyphen.
            # If it does, it assumes it’s a range like "$12,000-$15,000" and sets sep = "-". 
            # If not, it goes with a slash—like "55000 / 65000"—and sets sep = "/" and then seperate them using split for the right seperator
            if "-" in value:
                sep = "-"
            else:
                sep = "/"
            parts = value.split(sep)
            # here try and except gives us the median number for the ranged values
            try:
                return (float(parts[0].strip()) + float(parts[1].strip())) / 2
            except:
                return np.nan  # If any part can't be converted
        #here esle means if we do not have informations like 15000-16000(ranges)and only one number values
        else:
            try:
                return float(value)
            except:
                return np.nan
    return np.nan
dt1["Cars Prices"] = dt1["Cars Prices"].apply(parse_price)
print("\nAverage Car Price:", dt1["Cars Prices"].mean())

#cc battery part
dt1["CC/Battery Capacity"] = (
    dt1["CC/Battery Capacity"]
      .astype(str)
      .str.replace(",", "", regex=False)
      .str.extract(r"(\d+(?:\.\d+)?)")[0]
      .astype(float)
)

#Performance(0 - 100 )KM/H part
dt1["Performance(0 - 100 )KM/H"] = dt1["Performance(0 - 100 )KM/H"].str.extract(r"(\d+\.?\d*)")
#\d+ : Matches one or more digits (0–9)
dt1["Performance(0 - 100 )KM/H"] = pd.to_numeric(dt1["Performance(0 - 100 )KM/H"], errors='coerce')

#seats part
dt1["Seats"] = dt1["Seats"].str.extract(r"(\d+)")
#\d+ : Matches one or more digits (0–9)
dt1["Seats"] = pd.to_numeric(dt1["Seats"], errors='coerce')

#torque part
def parse_torque(value):
    if pd.isna(value):
        return np.nan
    s = str(value).lower().replace(",", "").replace("nm", "").strip()
    # Check for a range like "100 - 140"
    if "-" in s:
        parts = s.split("-")
        try:
            return (float(parts[0].strip()) + float(parts[1].strip())) / 2
        except:
            return np.nan
    else:
        try:
            return float(s)
        except:
            return np.nan
dt1["Torque"] = dt1["Torque"].apply(parse_torque)


#hhourse power part
def parse_horsepower(val):
    if pd.isna(val):
        return np.nan
    s = str(val).lower().replace(",", "").strip()
    # Normalize different dash types to a hyphen
    s = s.replace("–", "-").replace("—", "-")
    # Grab numbers (works for single values and ranges)
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
    if not nums:
        return np.nan
    # If it's a range like "70-85", average the first two numbers
    return nums[0] if len(nums) == 1 else (nums[0] + nums[1]) / 2

# Apply to the column
dt1["HorsePower"] = dt1["HorsePower"].apply(parse_horsepower)

# If you keep a separate variable for convenience
dt1_horsep = dt1["HorsePower"]


#creating multiple data bases for furthur data visualization aspect by aspect
dt1_company_n=dt1["Company Names"]
dt1_car_n=dt1["Cars Names"]
dt1_eng=dt1["Engines"]
dt1_cc=dt1["CC/Battery Capacity"]
dt1_horsep=dt1["HorsePower"]
dt1_speed=dt1["Total Speed"]
dt1_perform=dt1["Performance(0 - 100 )KM/H"]
dt1_price=dt1["Cars Prices"]
dt1_fueltype=dt1["Fuel Types"]
dt1_seat=dt1["Seats"]
dt1_Torque=dt1["Torque"]

##showing their first 10 datas
# print("\n",dt1_company_n.head(10))
# print("\n",dt1_car_n.head(10))
# print("\n",dt1_company_n.head(10))
# print("\n",dt1_cc.head(10))
# print("\n",dt1_horsep.head(10))
# print("\n",dt1_speed.head(10))
# print("\n",dt1_perform.head(10))
# print("\n",dt1_price.head(10))
# print("\n",dt1_fueltype.head(10))
# print("\n",dt1_seat.head(10))
# print("\n",dt1_Torque.head(10))

#finding each data important information(max,min,mean,below or above average,...)
# print("\nCC/Battery Capacity minimum: ",dt1_cc.min())
# print("\nCC/Battery Capacity maximum: ",dt1_cc.max())
print("\nCC/Battery Capacity mean: ",dt1_cc.mean())
# print("\nHorsePower minimum: ",dt1_horsep.min())
# print("\nHorsePower Capacity maximum: ",dt1_horsep.max())
print("\nHorsePower Capacity mean: ",dt1_horsep.mean())
# print("\nTotal Speed minimum: ",dt1_speed.min())
# print("\nTotal Speed maximum: ",dt1_speed.max())
print("\nTotal Speed Capacity mean: ",dt1_speed.mean())
# print("\nPerformance(0 - 100 )KM/H minimum: ",dt1_perform.min())
# print("\nPerformance(0 - 100 )KM/H maximum: ",dt1_perform.max())
print("\nPerformance(0 - 100 )KM/H mean: ",dt1_perform.mean())
# print("\nCars Prices minimum: ",dt1_price.min())
# print("\nCars Prices maximum: ",dt1_price.max())
print("\nCars Prices mean: ",dt1_price.mean())
# print("\nSeats minimum: ",dt1_seat.min())
# print("\nSeats maximum: ",dt1_seat.max())
print("\nSeats mean: ",dt1_seat.mean())
# print("\nTorque minimum: ",dt1_Torque.min())
# print("\nTorque maximum: ",dt1_Torque.max())
print("\nTorque mean: ",dt1_Torque.mean())


# #locate the important parts in the original dataset
idx_max_hp = dt1["HorsePower"].idxmax()
idx_min_hp = dt1["HorsePower"].idxmin()
car_with_max_hp = dt1.loc[idx_max_hp]
car_with_min_hp = dt1.loc[idx_min_hp]
print("\nCar with Maximum HorsePower:\n", car_with_max_hp)
print("\nCar with Minimum HorsePower:\n", car_with_min_hp)

idx_max_cc = dt1["CC/Battery Capacity"].idxmax()
idx_min_cc = dt1["CC/Battery Capacity"].idxmin()
car_with_max_cc = dt1.loc[idx_max_cc]
car_with_min_cc = dt1.loc[idx_min_cc]
print("\nCar with Maximum CC/Battery Capacity:\n", car_with_max_cc)
print("\nCar with Minimum CC/Battery Capacity:\n", car_with_min_cc)

idx_max_speed = dt1["Total Speed"].idxmax()
idx_min_speed = dt1["Total Speed"].idxmin()
car_with_max_speed = dt1.loc[idx_max_speed]
car_with_min_speed = dt1.loc[idx_min_speed]
print("\nCar with Maximum Total Speed:\n", car_with_max_speed)
print("\nCar with Minimum Total Speed:\n", car_with_min_speed)

idx_max_perform = dt1["Performance(0 - 100 )KM/H"].idxmax()
idx_min_perform = dt1["Performance(0 - 100 )KM/H"].idxmin()
car_with_max_perform = dt1.loc[idx_max_perform]
car_with_min_perform = dt1.loc[idx_min_perform]
print("\nCar with minimum Performance(0 - 100 )KM/H:\n", car_with_max_perform)
print("\nCar with maximum Performance(0 - 100 )KM/H:\n", car_with_min_perform)

idx_max_price = dt1["Cars Prices"].idxmax()
idx_min_price = dt1["Cars Prices"].idxmin()
car_with_max_price = dt1.loc[idx_max_price]
car_with_min_price = dt1.loc[idx_min_price]
print("\nCar with Maximum Cars Prices:\n", car_with_max_price)
print("\nCar with Minimum Cars Prices:\n", car_with_min_price)


# Visualization of the 15 fastest cars
fastest_cars = dt1.nlargest(15, 'Total Speed')
slowest_cars = dt1.nsmallest(15, 'Total Speed')
# Plotting the 15 fastest cars
plt.figure(figsize=(12, 6))
plt.barh(fastest_cars['Cars Names'], fastest_cars['Total Speed'], color='skyblue')
plt.title('15 Fastest Cars')
plt.xlabel('Top Speed (km/h)')
plt.ylabel('Car Names')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()
# Plotting the 15 slowest cars
plt.figure(figsize=(12, 6))
plt.barh(slowest_cars['Cars Names'], slowest_cars['Total Speed'], color='salmon')
plt.title('15 Slowest Cars')
plt.xlabel('Top Speed (km/h)')
plt.ylabel('Car Names')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# Visualization of the 15 highest CC/Battery capacities
highest_cc = dt1.nlargest(15, 'CC/Battery Capacity')
lowest_cc = dt1.nsmallest(15, 'CC/Battery Capacity')
# Plotting the 15 highest CC/Battery capacities
plt.figure(figsize=(12, 6))
plt.plot(highest_cc['Cars Names'], highest_cc['CC/Battery Capacity'], marker='o', color='blue', label='Highest CC/Battery Capacity')
plt.title('15 Highest CC/Battery Capacities')
plt.xlabel('Car Names')
plt.ylabel('CC/Battery Capacity')
plt.xticks(rotation=45)
# Plotting the 15 lowest CC/Battery capacities
plt.figure(figsize=(12, 6))
plt.plot(lowest_cc['Cars Names'], lowest_cc['CC/Battery Capacity'], marker='o', color='red', label='Lowest CC/Battery Capacity')
plt.title('15 Lowest CC/Battery Capacities')
plt.xlabel('Car Names')
plt.ylabel('CC/Battery Capacity')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# Visualization of the 15 highest car prices
highest_prices = dt1.nlargest(15, 'Cars Prices')
lowest_prices = dt1.nsmallest(15, 'Cars Prices')
# Plotting the 15 highest car prices
plt.figure(figsize=(12, 6))
plt.barh(highest_prices['Cars Names'], highest_prices['Cars Prices'], color='green')
plt.title('15 Highest Car Prices')
plt.xlabel('Price (USD)')
plt.ylabel('Car Names')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()
# Plotting the 15 lowest car prices
plt.figure(figsize=(12, 6))
plt.barh(lowest_prices['Cars Names'], lowest_prices['Cars Prices'], color='orange')
plt.title('15 Lowest Car Prices')
plt.xlabel('Price (USD)')
plt.ylabel('Car Names')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

dt1.info()