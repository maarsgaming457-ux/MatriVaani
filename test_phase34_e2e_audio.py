import os
import sys
import time
import json
import logging

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from dotenv import load_dotenv
load_dotenv()

from app.services.asr_service import ASRService
from app.services.tts_service import TTSService
from app.services.experimental_ho_translation.translator import experimental_ho_translator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("phase34_e2e")

def run_e2e_pipeline():
    logger.info("Initializing ASR and TTS services for Phase 34 E2E Audio Evaluation...")
    asr = ASRService()
    tts = TTSService()

    audio_files = [
        os.path.join("ho_test_audio", "ho1.wav"),
        os.path.join("ho_test_audio", "ho2.wav")
    ]

    results = []

    for audio_path in audio_files:
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            continue

        file_size_kb = os.path.getsize(audio_path) / 1024.0
        logger.info(f"\n=======================================================\nPROCESSING: {audio_path} ({file_size_kb:.1f} KB)\n=======================================================")

        # 1. Ho ASR
        t0 = time.time()
        asr_res = asr.transcribe(audio_path, language="ho")
        t_asr = time.time() - t0
        ho_transcript = asr_res.get("transcript", "") if isinstance(asr_res, dict) else str(asr_res)
        logger.info(f"[STEP 1: ASR] ({t_asr:.3f}s) Transcript: '{ho_transcript}'")

        # 2. Experimental Ho -> Hindi Translation
        t1 = time.time()
        trans_res = experimental_ho_translator.translate(ho_transcript)
        t_trans = time.time() - t1
        hindi_out = trans_res.get("translation", "")
        method = trans_res.get("method", "")
        conf = trans_res.get("confidence", "")
        logger.info(f"[STEP 2: TRANSLATE] ({t_trans:.3f}s) Method: {method} | Conf: {conf} | Hindi: '{hindi_out}'")

        # 3. Hindi TTS Synthesis
        t2 = time.time()
        tts_success = False
        tts_bytes_len = 0
        tts_error = None
        try:
            audio_bytes = tts.synthesize(hindi_out, language="hindi", provider_override="sarvam")
            t_tts = time.time() - t2
            if audio_bytes and len(audio_bytes) > 0:
                tts_success = True
                tts_bytes_len = len(audio_bytes)
                out_tts_path = f"ho_e2e_out_{os.path.basename(audio_path)}"
                with open(out_tts_path, "wb") as f_out:
                    f_out.write(audio_bytes)
                logger.info(f"[STEP 3: TTS] ({t_tts:.3f}s) Synthesized {tts_bytes_len} bytes -> {out_tts_path}")
            else:
                logger.warning(f"[STEP 3: TTS] ({t_tts:.3f}s) Received empty audio bytes.")
        except Exception as e:
            t_tts = time.time() - t2
            tts_error = str(e)
            logger.error(f"[STEP 3: TTS] ({t_tts:.3f}s) TTS synthesis failed: {e}")

        total_latency = t_asr + t_trans + t_tts

        rec = {
            "audio_file": audio_path,
            "file_size_kb": round(file_size_kb, 2),
            "asr_transcript": ho_transcript,
            "asr_latency_sec": round(t_asr, 3),
            "translation": hindi_out,
            "translation_method": method,
            "confidence": conf,
            "translation_latency_sec": round(t_trans, 3),
            "tts_success": tts_success,
            "tts_bytes": tts_bytes_len,
            "tts_latency_sec": round(t_tts, 3),
            "tts_error": tts_error,
            "total_latency_sec": round(total_latency, 3),
            "details": trans_res
        }
        results.append(rec)

    with open("PHASE_34_E2E_RESULTS.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info(f"\nE2E Evaluation complete. Saved results to PHASE_34_E2E_RESULTS.json")
    return results

if __name__ == "__main__":
    run_e2e_pipeline()
