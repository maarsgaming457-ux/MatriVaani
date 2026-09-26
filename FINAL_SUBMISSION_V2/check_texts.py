import pandas as pd
df_data = pd.read_parquet("https://huggingface.co/api/datasets/PYD4320/audio-text-pair_train-test-dataset-hindi/parquet/default/test/0.parquet")
print(df_data['text'].head())
