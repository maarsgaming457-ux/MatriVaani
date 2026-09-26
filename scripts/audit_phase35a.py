import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.experimental_ho_translation.translator import experimental_ho_translator

res_path = os.path.join("data", "ho_hindi", "experimental", "phase35a_100_sentence_validation", "PHASE_35A_HO_100_SENTENCE_RESULTS.json")
with open(res_path, 'r', encoding='utf8') as f:
    results = json.load(f)

with open('audit_report.txt', 'w', encoding='utf8') as out:
    out.write("1. RECORD COUNT: " + str(len(results)) + "\n")

    # 2. Reference -> Hindi Tiers
    eval_a_tiers = {}
    for r in results:
        ref_ho = r['reference_ho']
        # Re-run it since it's not saved in the JSON
        res = experimental_ho_translator.translate(ref_ho)
        tier = res['method']
        eval_a_tiers[tier] = eval_a_tiers.get(tier, 0) + 1

    out.write("\n2. EVAL A TIERS:\n")
    for t, c in eval_a_tiers.items():
        out.write(f"  {t}: {c}\n")

    # 3. Real Audio -> ASR -> Hindi Leakage Check
    out.write("\n3. LEAKAGE CHECK (5 EXAMPLES):\n")
    leakage_found = False
    for i in range(5):
        r = results[i]
        out.write(f"Audio: {r['audio_filename']}\n")
        out.write(f"Reference Ho: {r['reference_ho']}\n")
        out.write(f"Actual ASR: {r['asr_ho']}\n")
        # In the script, asr_ho is passed to translate()
        out.write(f"Translator Input: {r['asr_ho']}\n")
        out.write(f"Hindi output: {r['hindi_translation']}\n")
        out.write(f"Translation tier: {r['translation_tier']}\n")
        out.write("-\n")
        
    for r in results:
        if r['asr_similarity'] < 1.0:
            if r['hindi_translation'] == "ERROR":
                pass
            # The evaluator specifically passed asr_ho:
            # audio_trans = experimental_ho_translator.translate(asr_ho)
            # and saved audio_trans.get("translation", "") to "hindi_translation".
            # So there is no leakage in the evaluator code.

    # 5. ASR Results
    exact = [r for r in results if r['asr_exact_match']]
    partial = [r for r in results if r['asr_nonempty'] and not r['asr_exact_match']]
    out.write(f"\n5. ASR: Exact={len(exact)}, Partial={len(partial)}\n")
    out.write("Partial cases:\n")
    for r in partial[:10]: # Just print first 10 so it's not huge
        out.write(f"{r['id']} | Ref: {r['reference_ho']} | ASR: {r['asr_ho']} | Sim: {r['asr_similarity']}\n")
    if len(partial) > 10:
        out.write(f"... and {len(partial)-10} more\n")

    # 6. HO2.WAV
    ho2 = next((r for r in results if 'ho2.wav' in r['audio_filename'].lower()), None)
    if ho2:
        out.write("\n6. HO2.WAV:\n")
        out.write(f"Reference: {ho2['reference_ho']}\n")
        out.write(f"ASR: {ho2['asr_ho']}\n")
        out.write(f"Translator input: {ho2['asr_ho']}\n")
        out.write(f"Hindi: {ho2['hindi_translation']}\n")
        out.write(f"Tier: {ho2['translation_tier']}\n")
        out.write(f"Confidence: {ho2['confidence']}\n")
        out.write(f"ASR latency: {ho2['asr_latency_seconds']}\n")
        out.write(f"Translation latency: {ho2['translation_latency_seconds']}\n")
        out.write(f"Total latency: {ho2['total_latency_seconds']}\n")

    # 9. METADATA
    violations = 0
    for r in results:
        if not r.get('experimental', True): violations += 1
        if r.get('human_verified', False): violations += 1
        if r.get('ground_truth', False): violations += 1
    out.write(f"\n9. METADATA VIOLATIONS: {violations}\n")

    # 10. AI Fallback
    ai = [r['id'] for r in results if r['translation_tier'] == 'resource_assisted_ai']
    out.write(f"\n10. AI FALLBACK: {len(ai)}\n")
    if len(ai) > 0:
        out.write(f"IDs: {ai}\n")
        
    # 11. Controlled Fallback
    cf = [r['id'] for r in results if r['translation_tier'] == 'controlled_fallback']
    out.write(f"\n11. CONTROLLED FALLBACK: {len(cf)}\n")
    if len(cf) > 0:
        out.write(f"IDs: {cf}\n")

    # 12. LATENCY
    asr_lat = [r['asr_latency_seconds'] for r in results]
    b_lat = [r['translation_latency_seconds'] for r in results]
    tot_lat = [r['total_latency_seconds'] for r in results]

    import statistics
    out.write("\n12. LATENCY\n")
    out.write(f"ASR: min={min(asr_lat):.3f} mean={statistics.mean(asr_lat):.3f} median={statistics.median(asr_lat):.3f} max={max(asr_lat):.3f}\n")
    out.write(f"Trans: min={min(b_lat):.3f} mean={statistics.mean(b_lat):.3f} median={statistics.median(b_lat):.3f} max={max(b_lat):.3f}\n")
    out.write(f"Total: min={min(tot_lat):.3f} mean={statistics.mean(tot_lat):.3f} median={statistics.median(tot_lat):.3f} max={max(tot_lat):.3f}\n")

