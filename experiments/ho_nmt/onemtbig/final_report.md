# FINAL REPORT

------------------------------------------------------------
MODEL
------------------------------------------------------------
ONEMT-BIG
Checkpoint: https://vandanresearch.sgp1.digitaloceanspaces.com/bhashaverse-models/machine-translation/onemtbig/iiith-onemtbig.zip
Parameter count: ~1B-2B
Tokenizer: SentencePiece
License: CC BY-NC 4.0
Hindi code: hin_Deva
Ho code: hoc_Wara

------------------------------------------------------------
HINDI ? HO
------------------------------------------------------------
Test samples: 0
Successful non-empty outputs: 0
Empty outputs: 0
Ho-script outputs: 0
Hindi leakage: 0
English leakage: 0
Santali leakage: 0
Qualitative assessment: FAILED (Test Blocked)

------------------------------------------------------------
HO ? HINDI
------------------------------------------------------------
Test samples: 0
Successful non-empty outputs: 0
Empty outputs: 0
Hindi-script outputs: 0
Ho leakage: 0
English leakage: 0
Santali leakage: 0
Qualitative assessment: FAILED (Test Blocked)

------------------------------------------------------------
LATENCY
------------------------------------------------------------
Hindi ? Ho:
cold: UNKNOWN
mean: UNKNOWN
median: UNKNOWN
p95: UNKNOWN
max: UNKNOWN

Ho ? Hindi:
cold: UNKNOWN
mean: UNKNOWN
median: UNKNOWN
p95: UNKNOWN
max: UNKNOWN

Hardware: TEST_BLOCKED

------------------------------------------------------------
MEMORY
------------------------------------------------------------
Model RAM: UNKNOWN
GPU VRAM: UNKNOWN
CPU: UNKNOWN
GPU: UNKNOWN

------------------------------------------------------------
FINAL DECISION
------------------------------------------------------------
**OPTION E: TEST_BLOCKED**
Meaning: The official checkpoint cannot be obtained or executed. The DigitalOcean Spaces server hosting the 2.14GB model throttles downloads to roughly ~50 KB/s, which would take more than 12 hours to complete. Therefore, the model cannot be practically evaluated for zero-shot Hindi-Ho capability at this time.
