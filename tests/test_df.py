import pandas as pd
df = pd.read_parquet("datasets/cache/santali/valid.parquet")
print(df.columns)
print(df.iloc[0])
