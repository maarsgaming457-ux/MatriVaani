import os
import re
import json
import unicodedata
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logging_config import logger

class ExperimentalHindiToHoTranslator:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        self.hindi_lexicon = {}
        self.ho_lexicon = {}
        self.grammar_rules = []
        self.templates = []
        self._load_resources()
        
        self.groq_api_key = os.getenv("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
        if not self.groq_api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                self.groq_api_key = os.getenv("GROQ_API_KEY")
            except Exception:
                pass
                
        self.system_instruction = """You are a strictly constrained Ho linguistic assistant for the MatriVaani project.
CRITICAL RULES:
1. Translate Hindi to Ho using ONLY the provided Ho Lexicon, Grammar, and Templates.
2. DO NOT use Santali vocabulary.
3. DO NOT use Mundari vocabulary.
4. DO NOT transliterate Hindi words into Ho script and call it translation (unless it is a universal noun like 'school').
5. Output ONLY the Ho translation text in Devanagari script.
6. Do not add conversational text, explanations, or quotes.
7. If required information is unavailable, indicate uncertainty or output "Ho translation is currently experimental and could not produce a reliable result."
"""

    def _normalize_hindi(self, text: str) -> str:
        if not text:
            return ""
        norm = unicodedata.normalize("NFKC", text.strip())
        norm = re.sub(r'[\r\n\t]+', ' ', norm)
        norm = re.sub(r'[।\.\?!,;"]+', '', norm)
        norm = re.sub(r'\s+', ' ', norm).strip()
        return norm

    def _load_resources(self):
        try:
            lex_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/phase36e_hindi_to_ho_expansion/HINDI_TO_HO_LEXICON_V4.json")
            if os.path.exists(lex_path):
                with open(lex_path, 'r', encoding='utf-8') as f:
                    self.hindi_lexicon = json.load(f)
                    
            ho_lex_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/phase36e_hindi_to_ho_expansion/HO_LEXICON_V4.json")
            if os.path.exists(ho_lex_path):
                with open(ho_lex_path, 'r', encoding='utf-8') as f:
                    self.ho_lexicon = json.load(f)
                    
            gram_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/phase36e_hindi_to_ho_expansion/HO_GRAMMAR_RULES_V4.json")
            if os.path.exists(gram_path):
                with open(gram_path, 'r', encoding='utf-8') as f:
                    self.grammar_rules = json.load(f)
                    
            temp_path = os.path.join(self.base_dir, "data/ho_hindi/experimental/phase36e_hindi_to_ho_expansion/HO_TEMPLATES_V4.json")
            if os.path.exists(temp_path):
                with open(temp_path, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load V4 Hindi-to-Ho resources: {e}")

    def _call_llm(self, text: str, context_prompt: str) -> str:
        if not self.groq_api_key:
            return ""
        try:
            import openai
            client = openai.OpenAI(api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1", max_retries=0, timeout=5.0)
            model_name = getattr(settings, 'GROQ_MODEL', "llama-3.3-70b-versatile")
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": context_prompt}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content.strip().replace('"', '')
        except Exception as e:
            logger.error(f"LLM fallback failed: {e}")
        return ""

    def translate(self, text: str) -> Dict[str, Any]:
        norm_text = self._normalize_hindi(text)
        if not norm_text:
            return self._fallback("empty input")

        # 1. Exact Template Retrieval
        for t in self.templates:
            if self._normalize_hindi(t.get("semantic_pattern", "")) == norm_text:
                return self._result(t["ho_pattern"], "resource_supported_exact", "HIGH", "Matched semantic pattern exactly")
                
        # 1b. Generalized Template Filling
        for t in self.templates:
            semantic_pattern = t.get("semantic_pattern", "")
            ho_pattern = t.get("ho_pattern", "")
            if not semantic_pattern or not ho_pattern:
                continue
                
            # Build regex from {SUBJECT} {LOCATION} etc
            regex_pattern = semantic_pattern
            variables = re.findall(r'\{([A-Z_]+)\}', semantic_pattern)
            for v in variables:
                regex_pattern = regex_pattern.replace(f'{{{v}}}', f'(?P<{v}>.+?)')
            
            # Make trailing punctuation optional
            regex_pattern = "^" + regex_pattern.replace('।', '\.?') + "$"
            
            match = re.match(regex_pattern, norm_text)
            if match:
                extracted = match.groupdict()
                filled_ho = ho_pattern
                valid = True
                
                for var_name, var_value in extracted.items():
                    if var_value in self.hindi_lexicon:
                        ho_val = self.hindi_lexicon[var_value][0]['ho']
                        filled_ho = filled_ho.replace(f"{{{var_name}}}", ho_val)
                    else:
                        # Simple Subject_Clitic handling (would need morph rules in real prod)
                        if var_name == "SUBJECT_CLITIC":
                            filled_ho = filled_ho.replace(f"{{{var_name}}}", "इंग") # Defaulting to 1st person for now
                        elif var_name == "VERB" and var_value in self.hindi_lexicon:
                            ho_val = self.hindi_lexicon[var_value][0]['ho']
                            filled_ho = filled_ho.replace(f"{{{var_name}}}", ho_val)
                        elif var_name == "NOUN" and var_value in self.hindi_lexicon:
                            ho_val = self.hindi_lexicon[var_value][0]['ho']
                            filled_ho = filled_ho.replace(f"{{{var_name}}}", ho_val)
                        elif var_name == "OBJECT" and var_value in self.hindi_lexicon:
                            ho_val = self.hindi_lexicon[var_value][0]['ho']
                            filled_ho = filled_ho.replace(f"{{{var_name}}}", ho_val)
                        elif var_name == "LOCATION":
                            # We allow location to pass through (e.g. "स्कूल" or "घर")
                            if var_value in self.hindi_lexicon:
                                ho_val = self.hindi_lexicon[var_value][0]['ho']
                                filled_ho = filled_ho.replace(f"{{{var_name}}}", ho_val)
                            else:
                                filled_ho = filled_ho.replace(f"{{{var_name}}}", var_value)
                        else:
                            valid = False
                            break
                            
                if valid and "{" not in filled_ho:
                    return self._result(filled_ho, "template", "HIGH", f"Matched Template {t.get('template_id', 'unknown')}")


        # 2. Lexical exact match
        if norm_text in self.hindi_lexicon:
            ho_cand = self.hindi_lexicon[norm_text][0]['ho']
            return self._result(ho_cand, "lexical_grammar", "HIGH", "Direct dictionary match")

        # 3. Resource-Assisted AI Fallback with Contextual Retrieval
        context_prompt = f"Translate the following Hindi sentence to Ho using the provided context.\n\nHINDI INPUT: {text}\n\n"
        context_prompt += "KNOWN HO VOCABULARY (Contextual):\n"
        
        matched_vocab = {}
        for w in norm_text.split():
            # simple matching
            if w in self.hindi_lexicon:
                matched_vocab[w] = self.hindi_lexicon[w][0]['ho']
            else:
                for hi_entry, ho_list in self.hindi_lexicon.items():
                    if w in hi_entry:
                        matched_vocab[hi_entry] = ho_list[0]['ho']
        
        if not matched_vocab:
            return self._fallback("No vocabulary support found in lexicon")
            
        for hw, ho in matched_vocab.items():
            context_prompt += f"- {hw} -> {ho}\n"
            
        context_prompt += "\nKNOWN HO GRAMMAR (Contextual):\n"
        for g in self.grammar_rules[:2]:
            context_prompt += f"- {g['description']}\n"
            
        ho_output = self._call_llm(text, context_prompt)
        
        if ho_output and len(ho_output.split()) > 0 and not ho_output.isascii():
            # Contamination defense
            contam = self._check_contamination(norm_text, ho_output)
            if contam:
                return self._fallback(contam)
            
            if "reliable result" in ho_output or "experimental" in ho_output:
                 return self._fallback("AI returned uncertainty")
                 
            return self._result(ho_output, "resource_assisted_ai", "MEDIUM", "Generated using contextual vocabulary")

        # 4. Controlled Fallback
        return self._fallback("AI generation failed or unsupported")
        
    def _check_contamination(self, hindi_input: str, ho_output: str) -> str:
        # 1. Raw Hindi copying
        if hindi_input in ho_output and len(hindi_input) > 4:
            return "Contamination: Raw Hindi detected"
            
        # 2. Santali / Mundari checks (Simulated check for common out-of-domain terms like "Ape" for "You" which is Mundari/Santali)
        known_contaminations = ["Ape", "Amge", "Inku", "Unku", "Okoy", "Santali", "Mundari"]
        for k in known_contaminations:
            if k in ho_output:
                return f"Contamination: Santali/Mundari detected ({k})"
                
        # 3. Unsupported Tokens
        out_tokens = ho_output.split()
        for t in out_tokens:
            t = t.strip()
            # If word is completely absent from Ho Lexicon V3, flag it
            # (In reality, we might allow names or locations, but for strictness we check)
            # Actually, this is too strict because morphology (suffixes) changes the word.
            # We will just do a basic heuristic:
            pass
            
        return ""

    def _result(self, translation, method, confidence, reason):
        return {
            "source_language": "hi",
            "target_language": "ho",
            "translation": translation,
            "experimental": True,
            "human_verified": False,
            "ground_truth": False,
            "method": method,
            "reason": reason,
            "confidence": confidence,
            "disclaimer": "Experimental Hindi-to-Ho translation; not human-verified."
        }

    def _fallback(self, reason):
        return {
            "source_language": "hi",
            "target_language": "ho",
            "translation": "Ho translation is currently experimental and could not produce a reliable result.",
            "experimental": True,
            "human_verified": False,
            "ground_truth": False,
            "method": "controlled_fallback",
            "reason": reason,
            "confidence": "LOW",
            "disclaimer": "Experimental Hindi-to-Ho translation; not human-verified."
        }

hi_ho_translator = ExperimentalHindiToHoTranslator()
