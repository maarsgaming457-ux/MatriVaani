# COILD-MT-Corpus Access Status

## Status
**ACCESS UNAVAILABLE**

## Justification
The automated Phase 5.6 pipeline searched `datasets/nmt/raw/` and `datasets/nmt/raw/COILD-MT-Corpus/` for legitimate dataset files (e.g., `.csv`, `.jsonl`, `.txt`). No files were found.

Because the COILD dataset on Hugging Face is gated behind academic license terms and manual authentication, automated scripts cannot legally or technically extract the dataset without a human-provided token. 

In strict adherence to the **NO FABRICATION** rule, the system refuses to generate artificial translations or invent a pair count. The pipeline will remain halted at the data ingestion step until a human administrator deposits the actual files into the specified directory.
