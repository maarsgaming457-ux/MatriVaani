# PARQUET METADATA REPORT
- **Row Groups**: 39 per shard
- **Total Rows**: ~10,000,000 per shard
- **Sorting**: Languages are randomly interleaved.
- **Min/Max Filtering**: Fails, because hoc_Wara falls alphabetically between the minimum (sm_Beng / eng_Latn) and maximum (urd_Arab) values present in every row group. Parquet predicate pushdown cannot skip any row groups.
