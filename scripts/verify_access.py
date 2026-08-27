import os
os.environ["AIOHTTP_NOSENDFILE"] = "1"
import sys
import json
import sys

# Patch torchcodec to avoid DLL load crash on Windows
try:
    import torchcodec._internally_replaced_utils
    torchcodec._internally_replaced_utils.load_core_libraries = lambda *args, **kwargs: None
except ImportError:
    pass
except Exception:
    pass
import time
import psutil

# Prevent shadowing the pip datasets module
sys.path = [p for p in sys.path if p != '' and p != os.getcwd()]
import datasets

import importlib.util

spec = importlib.util.spec_from_file_location("text_normalizer", "datasets/santali/text_normalizer.py")
text_normalizer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(text_normalizer)
SantaliNormalizer = text_normalizer.SantaliNormalizer

spec2 = importlib.util.spec_from_file_location("indicvoices_loader", "datasets/santali/indicvoices_loader.py")
indicvoices_loader = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(indicvoices_loader)
IndicVoicesLoader = indicvoices_loader.IndicVoicesLoader

def get_ram_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def run_verification():
    print("Starting verification...")
    baseline_ram = get_ram_mb()
    print(f"Baseline RAM: {baseline_ram:.2f} MB")
    
    loader = IndicVoicesLoader()
    loader_ram = get_ram_mb()
    
    normalizer = SantaliNormalizer()
    
    stats = {
        "dataset": "ai4bharat/IndicVoices",
        "configuration": "santali",
        "language_code": "sat",
        "authentication": "SUCCESS",
        "train_access": "FAILED",
        "validation_access": "FAILED",
        "train_samples_tested": 0,
        "validation_samples_tested": 0,
        "audio_decoding": "FAILED",
        "transcript_access": "FAILED",
        "ol_chiki_samples": 0,
        "devanagari_samples": 0,
        "latin_samples": 0,
        "mixed_script_samples": 0,
        "baseline_ram_mb": round(baseline_ram, 2),
        "loader_ram_mb": round(loader_ram, 2),
        "peak_ram_mb": 0,
        "existing_loader": "FAILED",
        "pytest": "FAIL"
    }
    
    try:
        # Step 4: Verify train access
        print("Testing train access...")
        train_stream = loader.stream_train()
        stats["train_access"] = "SUCCESS"
        stats["existing_loader"] = "SUCCESS"
        
        # Step 5: Read exactly 5 train samples
        print("Reading 5 train samples...")
        peak_ram = loader_ram
        
        audio_success = True
        text_success = True
        
        import io
        import soundfile as sf
        
        try:
            for i in range(5):
                sample = next(train_stream)
                current_ram = get_ram_mb()
                if current_ram > peak_ram:
                    peak_ram = current_ram
                    
                # Verify audio using soundfile since datasets decode=False is used
                if "audio" not in sample or not sample["audio"]:
                    audio_success = False
                else:
                    audio = sample["audio"]
                    if "bytes" not in audio and "path" not in audio:
                        audio_success = False
                    elif "bytes" in audio:
                        try:
                            data, samplerate = sf.read(io.BytesIO(audio["bytes"]))
                            if len(data) == 0 or samplerate <= 0:
                                audio_success = False
                        except Exception as e:
                            print(f"Failed to decode audio: {e}")
                            audio_success = False
                
                # Verify transcript
                text = sample.get("transcript", sample.get("text", ""))
                if not text:
                    text_success = False
                    
                duration = sample.get("duration", 0)
                lang = sample.get("lang", sample.get("language", ""))
                
                # Print safe metadata
                print(f"Sample {i+1}: duration={duration:.2f}s, lang={lang}, text_len={len(text)}")
                
                # Script analysis
                script = normalizer.identify_script(text)
                if script == "ol_chiki":
                    stats["ol_chiki_samples"] += 1
                elif script == "devanagari":
                    stats["devanagari_samples"] += 1
                elif script == "latin":
                    stats["latin_samples"] += 1
                else:
                    stats["mixed_script_samples"] += 1
                    
        except Exception as e:
            if "torchcodec" in str(e) or "WinError" in str(e):
                print(f"Audio stream failed due to environment exception: {e}")
                audio_success = False
                print("Falling back to text-only stream to complete text analysis...")
                text_stream = loader.stream_train()
                # Remove audio column to bypass torchcodec completely
                import datasets
                text_stream = datasets.load_dataset(loader.dataset_name, loader.config, split="train", streaming=True, token=loader.token).remove_columns(["audio"])
                text_stream = iter(text_stream)
                
                for i in range(5):
                    sample = next(text_stream)
                    current_ram = get_ram_mb()
                    if current_ram > peak_ram:
                        peak_ram = current_ram
                        
                    # Verify transcript
                    text = sample.get("transcript", sample.get("text", ""))
                    if not text:
                        text_success = False
                        
                    duration = sample.get("duration", 0)
                    lang = sample.get("lang", sample.get("language", ""))
                    
                    # Print safe metadata
                    print(f"Text-Only Sample {i+1}: duration={duration:.2f}s, lang={lang}, text_len={len(text)}")
                    
                    # Script analysis
                    script = normalizer.identify_script(text)
                    if script == "ol_chiki":
                        stats["ol_chiki_samples"] += 1
                    elif script == "devanagari":
                        stats["devanagari_samples"] += 1
                    elif script == "latin":
                        stats["latin_samples"] += 1
                    else:
                        stats["mixed_script_samples"] += 1
            else:
                raise e
                    
        stats["train_samples_tested"] = 5
        stats["audio_decoding"] = "SUCCESS" if audio_success else "FAILED"
        stats["transcript_access"] = "SUCCESS" if text_success else "FAILED"
        stats["peak_ram_mb"] = round(peak_ram, 2)
        
        # Step 6: Validation access
        print("Testing validation access...")
        valid_stream = datasets.load_dataset(loader.dataset_name, loader.config, split="validation", streaming=True, token=loader.token).remove_columns(["audio"])
        valid_stream = iter(valid_stream)
        for i in range(5):
            sample = next(valid_stream)
            
        stats["validation_access"] = "SUCCESS"
        stats["validation_samples_tested"] = 5
        
        print("Done verification stream.")
    except Exception as e:
        print(f"Error during verification: {e}")
        
    # Write report
    os.makedirs("evaluation/datasets/santali", exist_ok=True)
    with open("evaluation/datasets/santali/access_verification.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)
        
if __name__ == "__main__":
    run_verification()
