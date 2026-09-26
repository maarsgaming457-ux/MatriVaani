# FEASIBILITY MATRIX
- **ARCHITECTURE A (Direct NMT -> Warang Citi)**: Technically feasible ONLY with a byte-level model (ByT5) or a newly trained tokenizer.
- **ARCHITECTURE B (NMT -> Devanagari Ho -> Script Converter)**: Technically feasible, mitigates tokenizer issues, but requires a custom converter.
- **ARCHITECTURE C (Byte-level)**: Highly feasible.
- **ARCHITECTURE D (English Pivot)**: Rejected.
