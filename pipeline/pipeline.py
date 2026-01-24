import sys
import pandas as pd

print('arguments:', sys.argv)

month = int(sys.argv[1]) if len(sys.argv) > 1 else 12

df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_{month}.parquet", index=False)

print(f"Processing data for month: {month}")




