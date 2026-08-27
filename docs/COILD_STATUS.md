# COILD-MT-Corpus Status

## Final Status
**Closed — external dependency unavailable; alternative dataset strategy adopted.**

## Details
- **Dependency**: Hugging Face dataset `ainlpml-iitp/COILD-MT-Corpus`
- **Reported Size**: 20,603 pairs.
- **Reason for Closure**: The dataset is gated behind academic use approvals and manual authentication. Despite multiple automated extraction attempts across Phase 5, the raw `.csv` cannot be obtained without an authorized token.
- **Impact**: Without this baseline dataset, NMT fine-tuning of IndicTrans2 (or alternative models) is completely blocked.
- **Mitigation**: The MatriVaani architecture must not be permanently blocked by an external academic gate. We are transitioning to an alternative NMT data strategy focused on building a fully open, manually curated classroom dataset (see `docs/NMT_DATA_ACQUISITION_FINAL.md`).
