import os
import re
import json
import unicodedata
from typing import Dict, Any, List, Optional, Tuple
from app.core.config import settings
from app.core.logging_config import logger

class ExperimentalHoTranslator:
    """
    Isolated Experimental Translation Service for Ho -> Hindi.
    Designed for Smart India Hackathon (SIH) prototype.

    CRITICAL POLICY:
    - All outputs are experimental research candidates (experimental=True, ground_truth=False, human_verified=False).
    - Combines Exact Retrieval, Grammar Rules, Similarity Matching, and Resource-Assisted AI Fallback.
    - Zero interference with production translation pipeline (IndicTrans2, Bhashini, Sarvam).
    """

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

        # Datasets & Resources
        self.authentic_base_records: List[Dict[str, Any]] = []
        self.synthetic_records: List[Dict[str, Any]] = []
        self.dictionary_records: List[Dict[str, Any]] = []
        self.ho_to_hindi_lexicon: Dict[str, str] = {}
        self.normalized_authentic_map: Dict[str, Dict[str, Any]] = {}
        self.normalized_synthetic_map: Dict[str, Dict[str, Any]] = {}

        self._load_resources()

    def _normalize_ho(self, text: str) -> str:
        """
        Carefully normalizes Ho text in Devanagari orthography without losing linguistic features.
        - Unicode NFKC normalization
        - Standardizes visarga (colon ':' <-> Devanagari visarga 'ः')
        - Standardizes punctuation, removes redundant whitespace
        """
        if not text:
            return ""

        # 1. Unicode normalization
        norm = unicodedata.normalize("NFKC", text.strip())

        # 2. Standardize common orthographic variations in Ho Devanagari
        # Visarga variation: ':' often represents glottal stop / short check in field data
        norm = norm.replace("::", "ः").replace(":", "ः")

        # 3. Clean punctuation but preserve lexical characters
        # Replace dandas and sentence enders with single space for token comparison
        norm = re.sub(r'[\r\n\t]+', ' ', norm)
        norm = re.sub(r'[।॥\.\?!,;"]+', '', norm)

        # 4. Collapse multiple spaces
        norm = re.sub(r'\s+', ' ', norm).strip()

        return norm

    def _load_resources(self):
        """Loads authentic dataset, synthetic dataset, and bilingual dictionary."""
        # 1. Authentic Base Dataset (196 resource-supported records)
        base_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/v3_dataset/resource_supported_ai.jsonl")
        if os.path.exists(base_path):
            with open(base_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        rec = json.loads(line)
                        self.authentic_base_records.append(rec)
                        norm_ho = self._normalize_ho(rec.get("ho", ""))
                        if norm_ho:
                            self.normalized_authentic_map[norm_ho] = rec
            logger.info(f"Loaded {len(self.authentic_base_records)} authentic base Ho-Hindi pairs.")
        else:
            logger.warning(f"Authentic base dataset not found at {base_path}")

        # 2. Synthetic Grammar Variants (32 records)
        syn_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/v3_dataset/synthetic_augmented.jsonl")
        if os.path.exists(syn_path):
            with open(syn_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        rec = json.loads(line)
                        self.synthetic_records.append(rec)
                        norm_ho = self._normalize_ho(rec.get("ho", ""))
                        if norm_ho:
                            self.normalized_synthetic_map[norm_ho] = rec
            logger.info(f"Loaded {len(self.synthetic_records)} synthetic augmented Ho-Hindi pairs.")
        else:
            logger.warning(f"Synthetic dataset not found at {syn_path}")

        # 3. Bilingual Dictionary & Lexicon
        # Seed with Deeney (1978) core grammatical markers and high-frequency terms
        core_munda_lexicon = {
            "आइंग": "मैं",
            "अले": "हम लोग (अपवर्जक)",
            "आबु": "हम सब (समावेशी)",
            "आम": "तुम / आप",
            "आबेन": "तुम दोनों",
            "आपे": "तुम सब",
            "आए": "वह",
            "अकिन": "वे दोनों",
            "आको": "वे लोग",
            "अको": "वे लोग",
            "इनि:": "यह",
            "हनी": "वह",
            "नेना": "यह वस्तु/बात",
            "एना": "वह वस्तु/बात",
            "मेना:": "है / विद्यमान है",
            "मेनाइए": "वह है / मौजूद है",
            "मेना:लेया": "हम हैं / मौजूद हैं",
            "मेना:कोआ": "वे हैं / मौजूद हैं",
            "मेना:या": "है",
            "बनो:": "नहीं है / अनुपस्थित है",
            "बनु:आ": "नहीं है",
            "बनुइए": "वह नहीं है",
            "बनु:कोआ": "वे नहीं हैं",
            "ओआ:": "घर",
            "ओवा:": "घर",
            "ओआ": "घर",
            "दा:": "पानी / जल",
            "दा": "पानी",
            "मंडी": "भात / भोजन",
            "हातु": "गाँव",
            "होन": "बच्चा",
            "कुई": "लड़की",
            "कोड़ा": "लड़का",
            "हो": "व्यक्ति / मनुष्य",
            "दुरुम": "सोना / नींद",
            "सेनो:": "जाना",
            "सेनो": "जाना",
            "हजु:": "आना",
            "हजु": "आना",
            "जोम": "खाना",
            "नू": "पीना",
            "पाइटी": "काम / कार्य",
            "ओल": "लिखना / पढ़ाई",
            "पढ़ाव": "पढ़ना",
            "इतु": "सिखाना / पढ़ाना",
            "गे": "ही",
            "गेया": "ही है / निश्चित रूप से है",
            "का": "नहीं",
            "आलो": "मत / न",
            "ओन्दो:": "और / फिर",
            "ओन्दो": "और",
            "एसु": "बहुत",
            "पुर:": "बहुत / अधिक"
        }
        for hw, hiw in core_munda_lexicon.items():
            norm_hw = self._normalize_ho(hw)
            self.ho_to_hindi_lexicon[norm_hw] = hiw

        dict_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/resources/ho_hindi_dictionary.jsonl")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        rec = json.loads(line)
                        self.dictionary_records.append(rec)
                        ho_w = self._normalize_ho(rec.get("ho_word", ""))
                        hi_w = rec.get("hindi_word", "").strip()
                        if ho_w and hi_w:
                            self.ho_to_hindi_lexicon[ho_w] = hi_w
            logger.info(f"Loaded {len(self.dictionary_records)} dictionary entries into lexicon map.")
        else:
            logger.warning(f"Dictionary not found at {dict_path}")

    def _char_ngram_similarity(self, s1: str, s2: str, n: int = 3) -> float:
        """Calculates character n-gram Dice similarity."""
        if not s1 or not s2:
            return 0.0
        if s1 == s2:
            return 1.0

        ngrams1 = set(s1[i:i+n] for i in range(len(s1) - n + 1)) if len(s1) >= n else {s1}
        ngrams2 = set(s2[i:i+n] for i in range(len(s2) - n + 1)) if len(s2) >= n else {s2}

        intersection = len(ngrams1 & ngrams2)
        total = len(ngrams1) + len(ngrams2)
        return (2.0 * intersection) / total if total > 0 else 0.0

    def _token_jaccard_similarity(self, s1: str, s2: str) -> float:
        """Calculates token Jaccard similarity."""
        tokens1 = set(s1.split())
        tokens2 = set(s2.split())
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union if union > 0 else 0.0

    def _find_nearest_exemplars(self, norm_query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Finds top-k most similar authentic base examples using character + token similarity."""
        scored = []
        for rec in self.authentic_base_records:
            norm_target = self._normalize_ho(rec.get("ho", ""))
            char_sim = self._char_ngram_similarity(norm_query, norm_target, n=3)
            tok_sim = self._token_jaccard_similarity(norm_query, norm_target)
            combined_sim = 0.5 * char_sim + 0.5 * tok_sim
            scored.append((rec, combined_sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def _get_relevant_lexicon(self, norm_text: str) -> List[Dict[str, str]]:
        """Finds dictionary matches for tokens, stems, and substrings in the query text."""
        tokens = norm_text.split()
        matches = []
        seen_words = set()

        def try_add(k, source_term):
            if k in self.ho_to_hindi_lexicon and k not in seen_words:
                matches.append({"ho": source_term, "hindi": self.ho_to_hindi_lexicon[k]})
                seen_words.add(k)
                return True
            return False

        # Check individual tokens, sub-stems (stripping postpositions and concord markers)
        # Common Ho postpositions/markers: -रे (in/at/locative), -ते (by/with/instrumental),
        # -एते (from/ablative), -अः (of/genitive), -लेया (1st pl concord), -कोआ (3rd pl concord)
        for tok in tokens:
            try_add(tok, tok)
            # Try stripping locative -रे (-re), -ते (-te), -एते (-ete), -अः (-ah)
            for suffix in ["रे", "ते", "एते", "अः", "आः"]:
                if tok.endswith(suffix) and len(tok) > len(suffix) + 1:
                    stem = tok[:-len(suffix)]
                    if try_add(stem, tok):
                        break

            # Try stripping concord markers from existential verbs (e.g. मेना:लेया -> मेना:)
            for concord in ["लेया", "कोआ", "इए", "या", "बु"]:
                if tok.endswith(concord) and len(tok) > len(concord) + 2:
                    stem = tok[:-len(concord)]
                    if try_add(stem, tok):
                        break

        # Check bi-grams
        for i in range(len(tokens) - 1):
            bigram = f"{tokens[i]} {tokens[i+1]}"
            try_add(bigram, bigram)

        return matches

    def _apply_grammar_rules(self, norm_ho: str) -> Optional[Dict[str, Any]]:
        """
        Applies Deeney (1978) grammatical transformations against known authentic sentences.
        If the input is a single-step grammatical variant (pronoun, dual/plural, aspect, negation)
        of a known base sentence, computes the corresponding Hindi transformation.
        """
        # 1. Direct match in precomputed synthetic dataset
        if norm_ho in self.normalized_synthetic_map:
            match = self.normalized_synthetic_map[norm_ho]
            return {
                "hindi_text": match.get("hindi", "").strip(),
                "method": "grammar_rule_transformation",
                "confidence": "MEDIUM",
                "grammar_rule": match.get("grammar_rule", "Deeney (1978) synthetic grammar variant"),
                "provenance": match.get("id", "synthetic_augmented")
            }

        # 2. Dynamic Rule Substitution: Plural '-ko' <-> Dual '-kin'
        if " किन " in norm_ho or norm_ho.endswith(" किन"):
            # Try converting to plural '-ko' and check authentic map
            plural_variant = re.sub(r'\bकिन\b', 'को', norm_ho)
            if plural_variant in self.normalized_authentic_map:
                base = self.normalized_authentic_map[plural_variant]
                base_hindi = base.get("hindi", "")
                # Transform Hindi: 'उन लोगों' -> 'उन दोनों' / 'वे लोग' -> 'वे दोनों'
                transformed_hi = base_hindi.replace("उन लोगों", "उन दोनों").replace("वे लोग", "वे दोनों").replace("लोग", "दोनों")
                return {
                    "hindi_text": transformed_hi,
                    "method": "grammar_rule_transformation",
                    "confidence": "MEDIUM",
                    "grammar_rule": "Deeney (1978) §3: Animate dual marker substitution (-kin <-> -ko)",
                    "provenance": f"Derived from {base.get('id', 'ASR_BASE')}"
                }

        # 3. Dynamic Rule Substitution: Pronouns
        # If input has 'आइंग' (I) instead of 'आए' (he/she)
        if "आइंग " in norm_ho or norm_ho.startswith("आइंग"):
            third_person = re.sub(r'\bआइंग\b', 'आए', norm_ho)
            if third_person in self.normalized_authentic_map:
                base = self.normalized_authentic_map[third_person]
                base_hindi = base.get("hindi", "")
                transformed_hi = base_hindi.replace("वह ", "मैं ").replace("रहा है।", "रहा हूँ।").replace("ता है।", "ता हूँ।")
                return {
                    "hindi_text": transformed_hi,
                    "method": "grammar_rule_transformation",
                    "confidence": "MEDIUM",
                    "grammar_rule": "Deeney (1978) §12: First person singular pronominal concord",
                    "provenance": f"Derived from {base.get('id', 'ASR_BASE')}"
                }

        return None

    def _ai_fallback_translate(self, ho_text: str, norm_ho: str) -> Optional[str]:
        """
        Resource-Assisted AI Translation Fallback.
        Injects dictionary definitions, grammar rules, and nearest authentic examples into prompt context.
        """
        groq_api_key = os.getenv("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
        openai_api_key = os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", None)

        if not groq_api_key and not openai_api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                groq_api_key = os.getenv("GROQ_API_KEY")
                openai_api_key = os.getenv("OPENAI_API_KEY")
            except Exception:
                pass

        if not groq_api_key and not openai_api_key:
            logger.warning("No LLM API keys available for AI translation fallback.")
            return None

        # Gather context
        lex_matches = self._get_relevant_lexicon(norm_ho)
        exemplars = self._find_nearest_exemplars(norm_ho, top_k=3)

        lex_context = "\n".join([f"- Ho: '{m['ho']}' -> Hindi: '{m['hindi']}'" for m in lex_matches]) if lex_matches else "No direct dictionary entry found."
        ex_context = "\n".join([f"Example Ho: {ex[0].get('ho')}\nHindi Translation: {ex[0].get('hindi')}" for ex in exemplars if ex[1] > 0.2])

        prompt = f"""You are a specialized linguistic translator from Ho (हो भाषा - an Austroasiatic/Munda language spoken in Jharkhand/Odisha, written here in Devanagari) to standard Hindi (हिंदी).

TRANSLATION INSTRUCTIONS:
1. Translate the provided authentic Ho sentence into fluent, accurate Hindi.
2. Use the provided authentic Ho dictionary entries and grammatical references as ground truth.
3. Ho follows Subject-Object-Verb (SOV) structure.
4. Key grammatical markers:
   - 'ताना' / 'तना' = Present continuous (रहा है / रही है)
   - 'केना' / 'केने' = Past continuous (रहा था)
   - 'केडा' / 'लेना' = Past completed (किया / लिया था)
   - 'याना' / 'सेनोयन' = Intransitive past (हो गया / चला गया)
   - 'का' / 'काबु' / 'काको' = Negation placed before verbs (नहीं)
   - 'गे' / 'गेया' = Emphatic marker (ही / निश्चित रूप से है)
   - 'मेना:' / 'मेनाइए' = Existential presence (विद्यमान है / मौजूद है)
5. Output ONLY the translated Hindi sentence. Do not provide explanations, transliterations, or markdown tags.

AUTHENTIC DICTIONARY MATCHES:
{lex_context}

SIMILAR AUTHENTIC EXEMPLAR SENTENCES:
{ex_context}

INPUT HO SENTENCE TO TRANSLATE:
{ho_text}

HINDI TRANSLATION:"""

        try:
            import openai

            # Prefer Groq if key is present
            if groq_api_key:
                client = openai.OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
                # Try gpt-oss-120b, gpt-oss-20b, or qwen3.8-27b
                model_name = settings.GROQ_MODEL if hasattr(settings, 'GROQ_MODEL') and settings.GROQ_MODEL else "openai/gpt-oss-120b"
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a professional Ho to Hindi translator. Output only the Hindi translation."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=1024
                )
                raw_out = response.choices[0].message.content.strip() if response.choices[0].message.content else ""
                # Clean any quotes or leading labels
                clean_out = re.sub(r'^(हिंदी अनुवाद|अनुवाद|Hindi Translation|Translation):\s*', '', raw_out, flags=re.IGNORECASE)
                clean_out = clean_out.strip('"`\' \n')
                if clean_out and "उपलब्ध नहीं" not in clean_out:
                    return clean_out
            elif openai_api_key:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a professional Ho to Hindi translator. Output only the Hindi translation."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=150
                )
                raw_out = response.choices[0].message.content.strip()
                clean_out = re.sub(r'^(हिंदी अनुवाद|अनुवाद|Hindi Translation|Translation):\s*', '', raw_out, flags=re.IGNORECASE)
                clean_out = clean_out.strip('"`\' \n')
                if clean_out:
                    return clean_out
        except Exception as e:
            logger.error(f"AI translation fallback error: {e}")

        return None

    def translate(self, ho_text: str) -> Dict[str, Any]:
        """
        Translates a Ho sentence to Hindi using multi-tier hybrid strategies:
        Tier 1: Exact authentic base retrieval
        Tier 2: Grammar rule transformation
        Tier 3: High-similarity retrieval
        Tier 4: Resource-assisted AI fallback
        Tier 5: Safe controlled fallback
        """
        if not ho_text or not ho_text.strip():
            return {
                "source_language": "hoc",
                "target_language": "hin",
                "ho_text": ho_text,
                "input": ho_text,
                "hindi_text": "",
                "translation": "",
                "method": "empty_input",
                "confidence": "LOW",
                "similarity_score": 0.0,
                "dictionary_matches": [],
                "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
                "experimental": True,
                "ground_truth": False,
                "human_verified": False
            }

        raw_input = ho_text.strip()
        norm_input = self._normalize_ho(raw_input)

        # Check if input is non-Ho (e.g. English, numbers only, random symbols)
        has_devanagari = bool(re.search(r'[ऀ-ॿ]', raw_input))
        if not has_devanagari and len(raw_input) > 0:
            return {
                "source_language": "hoc",
                "target_language": "hin",
                "ho_text": raw_input,
                "input": raw_input,
                "hindi_text": "Ho translation is currently experimental and could not produce a reliable result.",
                "translation": "Ho translation is currently experimental and could not produce a reliable result.",
                "method": "controlled_fallback",
                "confidence": "LOW",
                "similarity_score": 0.0,
                "dictionary_matches": [],
                "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
                "experimental": True,
                "ground_truth": False,
                "human_verified": False,
                "notes": "Non-Devanagari / invalid input detected."
            }

        # -------------------------------------------------------------
        # TIER 1: EXACT AUTHENTIC RETRIEVAL
        # -------------------------------------------------------------
        if norm_input in self.normalized_authentic_map:
            matched_rec = self.normalized_authentic_map[norm_input]
            return {
                "source_language": "hoc",
                "target_language": "hin",
                "ho_text": raw_input,
                "input": raw_input,
                "hindi_text": matched_rec.get("hindi", "").strip(),
                "translation": matched_rec.get("hindi", "").strip(),
                "method": "resource_supported_exact_retrieval",
                "confidence": "HIGH",
                "similarity_score": 1.0,
                "dictionary_matches": self._get_relevant_lexicon(norm_input),
                "provenance": matched_rec.get("id", "ASR_BASE"),
                "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
                "experimental": True,
                "ground_truth": False,
                "human_verified": False
            }

        # -------------------------------------------------------------
        # TIER 2: GRAMMAR-RULE TRANSFORMATION & SYNTHETIC MATCH
        # -------------------------------------------------------------
        grammar_res = self._apply_grammar_rules(norm_input)
        if grammar_res:
            return {
                "source_language": "hoc",
                "target_language": "hin",
                "ho_text": raw_input,
                "input": raw_input,
                "hindi_text": grammar_res["hindi_text"],
                "translation": grammar_res["hindi_text"],
                "method": grammar_res["method"],
                "confidence": grammar_res["confidence"],
                "similarity_score": 0.95,
                "dictionary_matches": self._get_relevant_lexicon(norm_input),
                "grammar_rule": grammar_res.get("grammar_rule", ""),
                "provenance": grammar_res.get("provenance", "Deeney1978"),
                "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
                "experimental": True,
                "ground_truth": False,
                "human_verified": False
            }

        # -------------------------------------------------------------
        # TIER 3: SIMILARITY RETRIEVAL
        # -------------------------------------------------------------
        nearest = self._find_nearest_exemplars(norm_input, top_k=1)
        best_rec, best_sim = nearest[0] if nearest else (None, 0.0)

        # If very high similarity (>= 0.88), e.g. minor typo or single particle difference
        if best_rec and best_sim >= 0.88:
            return {
                "source_language": "hoc",
                "target_language": "hin",
                "ho_text": raw_input,
                "input": raw_input,
                "hindi_text": best_rec.get("hindi", "").strip(),
                "translation": best_rec.get("hindi", "").strip(),
                "method": "similarity_retrieval",
                "confidence": "MEDIUM",
                "similarity_score": round(best_sim, 3),
                "dictionary_matches": self._get_relevant_lexicon(norm_input),
                "provenance": best_rec.get("id", "ASR_BASE"),
                "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
                "experimental": True,
                "ground_truth": False,
                "human_verified": False
            }

        # -------------------------------------------------------------
        # TIER 4: RESOURCE-ASSISTED AI TRANSLATION FALLBACK
        # -------------------------------------------------------------
        ai_trans = self._ai_fallback_translate(raw_input, norm_input)
        if ai_trans:
            # Determine confidence based on lexical overlap
            lex_matches = self._get_relevant_lexicon(norm_input)
            tok_count = len(norm_input.split())
            lex_coverage = len(lex_matches) / max(1, tok_count)
            conf = "MEDIUM" if lex_coverage >= 0.5 or best_sim >= 0.6 else "LOW"

            return {
                "source_language": "hoc",
                "target_language": "hin",
                "ho_text": raw_input,
                "input": raw_input,
                "hindi_text": ai_trans,
                "translation": ai_trans,
                "method": "resource_assisted_ai",
                "confidence": conf,
                "similarity_score": round(best_sim, 3),
                "dictionary_matches": lex_matches,
                "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
                "experimental": True,
                "ground_truth": False,
                "human_verified": False
            }

        # -------------------------------------------------------------
        # TIER 5: CONTROLLED FALLBACK SAFETY (TASK 13)
        # -------------------------------------------------------------
        return {
            "source_language": "hoc",
            "target_language": "hin",
            "ho_text": raw_input,
            "input": raw_input,
            "hindi_text": "Ho translation is currently experimental and could not produce a reliable result.",
            "translation": "Ho translation is currently experimental and could not produce a reliable result.",
            "method": "controlled_fallback",
            "confidence": "LOW",
            "similarity_score": round(best_sim, 3),
            "dictionary_matches": [],
            "disclaimer": "Experimental candidate translation; not verified by native speakers. ground_truth=False",
            "experimental": True,
            "ground_truth": False,
            "human_verified": False
        }

# Global singleton instance for isolated experimental module
experimental_ho_translator = ExperimentalHoTranslator()
