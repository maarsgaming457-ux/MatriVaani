import duckdb
import time
import os
from huggingface_hub import get_token

token = get_token()
os.environ['HF_TOKEN'] = token

con = duckdb.connect()
con.execute('INSTALL httpfs; LOAD httpfs;')

start = time.time()
try:
    print('Querying parquet metadata for shard 1...')
    res = con.execute("SELECT source_language, target_language, COUNT(*) FROM 'hf://datasets/ltrciiith/bhashik-parallel-corpora-generic/data/train-shard_00000001.parquet' GROUP BY source_language, target_language;").fetchall()
    print('Query successful. Rows in shard 1:', sum(r[2] for r in res))
    print('Distinct language pairs:', len(res))
    
    # Check if there is any Ho at all
    ho_pairs = [r for r in res if r[0] == 'hoc_Wara' or r[1] == 'hoc_Wara']
    print('Ho pairs found:', ho_pairs)
except Exception as e:
    print('Error:', e)
print(f'Time taken: {time.time() - start:.2f}s')
