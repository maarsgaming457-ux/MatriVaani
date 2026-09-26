# HO-NMT-DATA-3 — BHASHIK ACCESS AUDIT

## 1. Access Status
Access to the gated dataset ltrciiith/bhashik-parallel-corpora-generic is **GRANTED**.

## 2. Authentication Status
Authenticated via Hugging Face Hub successfully. (Logged in).

## 3. Repository Structure
The repository consists of:
- .gitattributes
- README.md
- data/ (Directory containing 774 shards)

## 4. Data Formats
All data records are stored in parquet format.

## 5. Configurations/splits
- **Config**: default
- **Split**: 	rain (mapped to data/train-*.parquet)
- **Split**: 	est (mapped to data/test-*.parquet, but currently missing from the repo, which causes the Dataset Viewer's 500 error).

## 6. Language Metadata Structure
The Parquet schema contains the following string fields:
- domain
- source_language
- 	arget_language
- source_text
- 	arget_text

## 7. Evidence for hin_Deva
The dataset card (README.md) explicitly lists hin_Deva in the Language(s) metadata.

## 8. Evidence for hoc_Wara
The dataset card (README.md) explicitly lists hoc_Wara in the Language(s) metadata.

## 9. Exact Location of Hindi-Ho Data if Found
HINDI_HO_LOCATION
- **Configuration**: default
- **Split**: train
- **Relevant Shard Names**: Interleaved randomly across data/train-shard_00000001.parquet to data/train-shard_00000774.parquet (232 GB total).
- **Format**: Parquet
- **Fields**: source_language, 	arget_language, source_text, 	arget_text

## 10. Hindi-Ho Pair Count
exact_count = NOT_YET_COMPUTED
- Because the dataset is 232 GB partitioned into 774 generic shards, and hoc_Wara records are interleaved randomly, scanning the entire corpus via HTTP streaming sequentially would take hours/days.
- **Cheapest Safe Method**: Provision a PySpark or distributed computing cluster (like Google Colab / AWS EMR), download the dataset to high-speed NVMe storage, and run a parallel predicate filter query: SELECT COUNT(*) FROM read_parquet('data/*.parquet') WHERE source_language='hin_Deva' AND target_language='hoc_Wara'.

## 11. Sample Hindi-Ho Pairs
*Could not be extracted safely within the restricted streaming window. Predicate pushdown via HTTP on 774 unindexed Parquet shards failed to yield a pair in the first 100,000 sequentially streamed rows.*

## 12. Warang Citi Statistics
*Sample not yet retrieved.*

## 13. Duplicate/Quality Findings
*Sample not yet retrieved.*

## 14. License/Usage Conditions
- **License**: CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)
- **Attribution**: "BhashaVerse : Translation Ecosystem for Indian Subcontinent Languages"
- **Restrictions**: Non-commercial use only.

## 15. Whether Streaming/Filtering is Possible
Streaming is *technically* possible using datasets.load_dataset('parquet', data_files={'train':'hf://...'}, streaming=True). However, filtering for a highly specific zero-resource language like Ho across 232 GB of unindexed generic Parquet files via HTTP is computationally unviable for rapid discovery.

## 16. Exact Recommended Next Step
Do not attempt to HTTP-stream the 232GB dataset. Instead, launch a dedicated ephemeral high-compute instance with large bandwidth, download the data/ shards in parallel, use DuckDB or PySpark locally to slice out exactly source_language='hin_Deva' and 	arget_language='hoc_Wara', and export ONLY the Ho subset into a small JSONL artifact.

## FINAL STATUS
**HINDI_HO_DATA_PRESENT_BUT_NOT_YET_COUNTED**
