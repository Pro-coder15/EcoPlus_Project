import pandas as pd
import random
from datetime import date, timedelta

# Start & End date (1 full year)
start_date = date(2024, 1, 1)
end_date = date(2025, 12, 31)

data = []
current_date = start_date

while current_date <= end_date:
    energy = random.randint(65, 90)
    water = random.randint(55, 80)
    waste = random.randint(50, 75)
    green = random.randint(70, 90)
    transport = random.randint(45, 70)

    data.append([
        current_date,
        energy,
        water,
        waste,
        green,
        transport
    ])

    current_date += timedelta(days=1)

df = pd.DataFrame(
    data,
    columns=["date", "energy", "water", "waste", "green", "transport"]
)

df.to_csv("campus_daily_data.csv", index=False)

print("✅ campus_daily_data.csv generated successfully (365 days)")
