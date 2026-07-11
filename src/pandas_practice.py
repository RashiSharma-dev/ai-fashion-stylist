import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame (Pandas' table structure)
df = pd.read_csv("data/outfits.csv")

#show the first few rows
print("First 5 rows:")
print(df.head())

#show basic info about the data
print("\nColumn names:", df.columns.tolist())
print("Total outfits:", len(df))

#count how many outfits of each color 
color_counts = df['color'].value_counts()
print("\nColor counts:")
print(color_counts)

#plot a bar chart of colors
color_counts.plot(kind='bar')
plt.title("Outfit Colors Count")
plt.xlabel("Color")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("data/color_chart.png")
print("\ncolor_chart.png has been saved!")
