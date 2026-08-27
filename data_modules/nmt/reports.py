import json
from typing import List, Dict, Any
from .schemas import NMTRecord, VerificationStatus, DomainCategory

def generate_quality_report(records: List[NMTRecord]) -> Dict[str, Any]:
    """
    Generates a quality and statistics report for the dataset.
    """
    total = len(records)
    
    if total == 0:
        return {"total_records": 0, "status": "empty"}
        
    stats = {
        "total_records": total,
        "synthetic_count": sum(1 for r in records if r.synthetic),
        "verified_human_count": sum(1 for r in records if r.verification_status == VerificationStatus.VERIFIED_HUMAN),
        "unverified_count": sum(1 for r in records if r.verification_status == VerificationStatus.UNVERIFIED),
        "domain_distribution": {},
        "split_distribution": {"train": 0, "validation": 0, "test": 0, "unassigned": 0}
    }
    
    # Calculate domain distribution
    for domain in DomainCategory:
        count = sum(1 for r in records if r.domain == domain)
        stats["domain_distribution"][domain.value] = count
        
    # Calculate split distribution
    for r in records:
        if r.split:
            stats["split_distribution"][r.split] += 1
        else:
            stats["split_distribution"]["unassigned"] += 1
            
    # Calculate average quality score where available
    scores = [r.quality_score for r in records if r.quality_score is not None]
    stats["average_quality_score"] = sum(scores) / len(scores) if scores else None
    
    return stats

def save_report(report: Dict[str, Any], filepath: str = "datasets/nmt/reports/quality_report.json"):
    """Saves the report to a JSON file."""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
