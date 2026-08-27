import json
import os
from collections import defaultdict
from pathlib import Path
import sys

# Add the datasets directory to sys.path so we can import schemas without using the 'datasets' namespace
sys.path.insert(0, str(Path(__file__).parent.parent))
from pydantic import ValidationError
from schemas.schemas import ASRRecord, NMTRecord, TTSRecord

class DatasetValidator:
    def __init__(self, dataset_type: str):
        self.dataset_type = dataset_type
        if dataset_type == "asr":
            self.model = ASRRecord
        elif dataset_type == "nmt":
            self.model = NMTRecord
        elif dataset_type == "tts":
            self.model = TTSRecord
        else:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
            
    def validate_records(self, records: list[dict], root_dir: str = "."):
        report = {
            "dataset_type": self.dataset_type,
            "total_records": len(records),
            "valid_records": 0,
            "invalid_records": 0,
            "errors": [],
            "duplicate_ids": [],
            "duplicate_content": []
        }
        
        seen_ids = set()
        seen_content = set()
        
        for i, record_dict in enumerate(records):
            # 1. Check for duplicates
            sample_id = record_dict.get("sample_id")
            if sample_id:
                if sample_id in seen_ids:
                    report["duplicate_ids"].append(sample_id)
                seen_ids.add(sample_id)
            
            # Content duplication check based on type
            content_key = None
            if self.dataset_type in ["asr", "tts"]:
                content_key = record_dict.get("transcript")
            elif self.dataset_type == "nmt":
                content_key = f"{record_dict.get('source_text')}||{record_dict.get('target_text')}"
            
            if content_key:
                if content_key in seen_content:
                    report["duplicate_content"].append(content_key)
                seen_content.add(content_key)
                
            # 2. Schema validation
            try:
                record = self.model(**record_dict)
                # 3. Audio file validation for ASR/TTS
                if self.dataset_type in ["asr", "tts"]:
                    audio_path = Path(root_dir) / record.audio_path
                    if not audio_path.exists():
                        report["errors"].append({
                            "index": i,
                            "sample_id": sample_id,
                            "error": f"Audio file not found: {record.audio_path}"
                        })
                        report["invalid_records"] += 1
                        continue
                        
                # Additional logic like audio corruption check could go here
                report["valid_records"] += 1
                
            except ValidationError as e:
                report["invalid_records"] += 1
                report["errors"].append({
                    "index": i,
                    "sample_id": sample_id,
                    "error": str(e)
                })
                
        return report

def generate_validation_report(report: dict, output_path: str):
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=4)
