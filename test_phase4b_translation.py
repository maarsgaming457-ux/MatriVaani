import time
import requests
import sys
import json
import statistics

sys.stdout.reconfigure(encoding='utf-8')

FASTAPI_URL = "http://127.0.0.1:8000"

test_sentences = [
    "नमस्ते बच्चों।",
    "सुप्रभात, क्या हाल है?",
    "एक, दो, तीन, चार और पाँच।",
    "मेरे पास दो किताबें हैं।",
    "दो और दो चार होते हैं।",
    "यह एक लाल गेंद है।",
    "आसमान नीला है।",
    "यह एक गोल मेज है।",
    "मेरे पिता एक किसान हैं।",
    "मेरी माँ खाना बना रही है।",
    "कुत्ता भौंक रहा है।",
    "गाय घास खाती है।",
    "यह मेरी आँखें हैं।",
    "सूरज पूर्व दिशा से निकलता है।",
    "राम खेल रहा है।",
    "आज सोमवार है।",
    "कल छुट्टी है।",
    "पेड़ हमें ऑक्सीजन देते हैं।",
    "कृपया अपनी किताब खोलो।",
    "ध्यान से सुनो।"
]

def translate(text, src, tgt):
    payload = {
        "text": text,
        "source_lang": src,
        "target_lang": tgt
    }
    t0 = time.time()
    try:
        res = requests.post(f"{FASTAPI_URL}/translate", json=payload, timeout=60)
        t1 = time.time()
        latency = t1 - t0
        if res.status_code == 200:
            return res.status_code, res.json().get('translation', ''), latency
        else:
            return res.status_code, res.text, latency
    except Exception as e:
        return 500, str(e), time.time() - t0

def main():
    results = []
    latencies = []
    
    print("Starting Phase 4B Translation Tests...", flush=True)
    
    for i, text in enumerate(test_sentences):
        status, result, latency = translate(text, "Hindi", "Santali")
        print(f"Test {i+1}: {text} -> {result} ({latency:.2f}s)")
        results.append({
            "test_id": f"Test {i+1}",
            "hindi": text,
            "santali": result,
            "status": status,
            "latency": latency,
            "provider": "indictrans2_local"
        })
        latencies.append(latency)
        
    print("\nStarting Santali -> Hindi...")
    santali_text = "ᱦᱚᱞᱮ ᱜᱤᱫᱽᱨᱟᱹᱠᱚ ᱾"
    s_status, s_result, s_latency = translate(santali_text, "Santali", "Hindi")
    print(f"Santali to Hindi: {santali_text} -> {s_result} ({s_latency:.2f}s)")
    
    with open("phase4b_translation_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "hindi_to_santali": results,
            "santali_to_hindi": {
                "santali": santali_text,
                "hindi": s_result,
                "status": s_status,
                "latency": s_latency
            },
            "stats": {
                "first_latency": latencies[0],
                "min": min(latencies[1:]),
                "max": max(latencies[1:]),
                "avg": statistics.mean(latencies[1:]),
                "median": statistics.median(latencies[1:])
            }
        }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
