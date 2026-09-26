from datasets import load_dataset
try:
    ds = load_dataset('ltrciiith/bhashik-parallel-corpora-generic', split='train', streaming=True)
    count = 0
    total_checked = 0
    
    # Just to quickly see what language pairs exist in the first few records
    pairs = set()
    for row in ds:
        total_checked += 1
        src = row.get('source_language', '')
        tgt = row.get('target_language', '')
        pairs.add((src, tgt))
        
        if ('hin' in src and 'hoc' in tgt) or ('hoc' in src and 'hin' in tgt):
            count += 1
            if count <= 5:
                print(f"Match: {src}->{tgt}")
                
        if total_checked % 500000 == 0:
            print(f"Checked {total_checked} rows. Found pairs so far: {len(pairs)} unique language directions.")
        if total_checked >= 2000000:
            break
            
    print(f"Finished checking. Total pairs found: {count}")
    print(f"Sample of language pairs present in stream: {list(pairs)[:20]}")
except Exception as e:
    print('Error:', e)
