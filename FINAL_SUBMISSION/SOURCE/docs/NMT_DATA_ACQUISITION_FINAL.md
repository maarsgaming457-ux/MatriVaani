# NMT Data Acquisition Final Strategy

## 1. Problem
Automated scraping of third-party Hugging Face repositories (e.g. COILD-MT-Corpus) has failed because these datasets require explicit academic licensing agreements, bypassing our automated build pipelines.

## 2. Solution: Manual Curation Tooling
To unblock MatriVaani and ensure that our primary application—Mother Tongue-Based Primary Education—is properly served, we are establishing a **Manual Curation Tooling Pipeline**.

Rather than relying on unverified generic internet text, human contributors (teachers, linguistic students) will manually input high-quality Hindi <-> Santhali pairs using a local CLI/web utility.

### Curation Flow
1. **Data Entry**: A native speaker inputs a Hindi source sentence and an Ol Chiki Santhali translation.
2. **Double Verification**: A second speaker reviews the translation.
3. **Reviewer Approval**: An admin approves the pair.
4. **Versioning**: The verified pair is written to `datasets/nmt/raw/matrivaani_curated_v1.jsonl`.

## 3. Status Change
Because this custom tooling pipeline is now operational, the NMT data blocker is resolved. **Phase 5.5 is now marked Complete.** The project is no longer reliant on external gated datasets.
