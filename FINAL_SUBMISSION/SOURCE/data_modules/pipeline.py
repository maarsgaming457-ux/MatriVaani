import json
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from validation.validator import DatasetValidator, generate_validation_report

def process_dataset(input_jsonl: str, dataset_type: str, output_dir: str):
    print(f"Processing {dataset_type} dataset from {input_jsonl}...")
    
    records = []
    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
                
    validator = DatasetValidator(dataset_type)
    
    # Normally this would be RAW -> CLEAN -> NORMALIZE
    # For now we jump to validation of the parsed records
    print("Validating records...")
    report = validator.validate_records(records, root_dir=str(Path(input_jsonl).parent))
    
    out_path = Path(output_dir) / f"{dataset_type}_validation_report.json"
    generate_validation_report(report, str(out_path))
    
    print(f"Validation complete. Report saved to {out_path}")
    if report["invalid_records"] > 0 or report["duplicate_ids"] or report["duplicate_content"]:
        print(f"WARNING: Dataset has errors. Valid: {report['valid_records']}, Invalid: {report['invalid_records']}")
        return False
        
    print("Dataset passed validation.")
    # Here we would do: SPLIT (Train/Val/Test)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSONL")
    parser.add_argument("--type", required=True, choices=["asr", "nmt", "tts"], help="Dataset type")
    parser.add_argument("--outdir", required=True, help="Output directory for report")
    args = parser.parse_args()
    process_dataset(args.input, args.type, args.outdir)
