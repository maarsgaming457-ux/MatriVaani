# HO DATA VERIFICATION PROTOCOL

## Workflow
1. **COLLECTED**: Data enters system as UNVERIFIED or SYNTHETIC.
2. **TRANSCRIBED**: Audio is transcribed, or synthetic pair is proposed.
3. **NATIVE REVIEW**: Native Ho speaker reviews the sentence pair / audio transcript.
4. **DECISION**:
   - APPROVED: Upgraded to HUMAN_GROUND_TRUTH.
   - CORRECTED: New corrected record created. Old record becomes REJECTED.
   - REJECTED: Tagged as rejected.

**CRITICAL RULE**: Never overwrite original data. Corrections must preserve the original record by creating a new version.
