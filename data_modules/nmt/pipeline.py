import json
import uuid
import re
from typing import List, Dict, Tuple
from .schemas import NMTRecord, VerificationStatus, ScriptVariant, DomainCategory

def normalize_text(text: str) -> str:
    """
    Deterministically normalizes text.
    - Preserves Ol Chiki and Devanagari.
    - Strips leading/trailing whitespace.
    - Normalizes internal whitespace to single spaces.
    """
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def detect_duplicates(records: List[NMTRecord]) -> Tuple[List[NMTRecord], List[Dict]]:
    """
    Finds exact source-target duplicates, or same source with different targets.
    Returns: (Unique Records, List of flagged potential duplicates for review)
    """
    seen_sources = {}
    seen_pairs = set()
    
    unique_records = []
    flagged_for_review = []
    
    for record in records:
        pair_key = (record.source_text.lower(), record.target_text.lower())
        source_key = record.source_text.lower()
        
        if pair_key in seen_pairs:
            # Exact duplicate, we can safely discard or just log it
            flagged_for_review.append({"type": "exact_duplicate", "record_id": record.id})
            continue
            
        if source_key in seen_sources:
            # Same Hindi, different Santhali! Flag for human review
            flagged_for_review.append({
                "type": "conflicting_target",
                "record_id": record.id,
                "source": record.source_text,
                "existing_target": seen_sources[source_key],
                "new_target": record.target_text
            })
            # We still keep it in unique_records so humans can see it and resolve it later
            # (or we could drop it, but user requested not to automatically delete conflicting translations)
            unique_records.append(record)
        else:
            unique_records.append(record)
            
        seen_pairs.add(pair_key)
        seen_sources[source_key] = record.target_text
        
    return unique_records, flagged_for_review

def validate_and_ingest(raw_data: List[Dict]) -> Tuple[List[NMTRecord], List[Dict]]:
    """
    Takes raw dictionaries, normalizes text, validates against the Pydantic schema.
    Returns: (Valid NMTRecords, List of validation errors)
    """
    valid_records = []
    errors = []
    
    for i, item in enumerate(raw_data):
        try:
            if 'source_text' in item:
                item['source_text'] = normalize_text(item['source_text'])
            if 'target_text' in item:
                item['target_text'] = normalize_text(item['target_text'])
                
            if 'id' not in item:
                item['id'] = str(uuid.uuid4())
                
            record = NMTRecord(**item)
            valid_records.append(record)
        except Exception as e:
            errors.append({"index": i, "data": item, "error": str(e)})
            
    return valid_records, errors

def generate_splits(records: List[NMTRecord], val_ratio=0.1, test_ratio=0.1) -> Dict[str, List[NMTRecord]]:
    """
    Splits the dataset into train, validation, and test.
    Ensures that test ONLY gets VERIFIED_HUMAN and non-synthetic data.
    """
    import random
    
    # Separate eligible test data
    eligible_for_test = [r for r in records if not r.synthetic and r.verification_status in [VerificationStatus.VERIFIED_HUMAN, VerificationStatus.REVIEWED_HUMAN]]
    ineligible = [r for r in records if r not in eligible_for_test]
    
    # Calculate target sizes
    total = len(records)
    test_size = int(total * test_ratio)
    
    random.shuffle(eligible_for_test)
    random.shuffle(ineligible)
    
    test_set = eligible_for_test[:test_size]
    
    remaining = eligible_for_test[test_size:] + ineligible
    random.shuffle(remaining)
    
    val_size = int(total * val_ratio)
    val_set = remaining[:val_size]
    train_set = remaining[val_size:]
    
    # Update split flags
    for r in test_set: r.split = "test"
    for r in val_set: r.split = "validation"
    for r in train_set: r.split = "train"
    
    return {
        "train": train_set,
        "validation": val_set,
        "test": test_set
    }
