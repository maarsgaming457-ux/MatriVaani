import re

def update_translator():
    with open('app/services/experimental_ho_translation/hi_ho_translator.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update AI Client Rate Limit & Timeout
    ai_old = '''            client = openai.OpenAI(api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1")'''
    ai_new = '''            client = openai.OpenAI(api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1", max_retries=0, timeout=5.0)'''
    content = content.replace(ai_old, ai_new)

    # 2. Update Template Filling logic
    template_old = '''        # 1b. Generalized Template Filling
        if norm_text.startswith("मैं ") and "से आया था" in norm_text:
            loc = norm_text.replace("मैं ", "").replace("से आया था", "").strip()
            return self._result(f"आइंग {loc}एतेइंग हुजु लेना", "template", "HIGH", "Matched Template T_V3_001")'''

    template_new = '''        # 1b. Generalized Template Filling
        for t in self.templates:
            semantic_pattern = t.get("semantic_pattern", "")
            ho_pattern = t.get("ho_pattern", "")
            if not semantic_pattern or not ho_pattern:
                continue
                
            # Build regex from {SUBJECT} {LOCATION} etc
            regex_pattern = semantic_pattern
            variables = re.findall(r'\\{([A-Z_]+)\\}', semantic_pattern)
            for v in variables:
                regex_pattern = regex_pattern.replace(f'{{{v}}}', f'(?P<{v}>.+?)')
            
            # Make trailing punctuation optional
            regex_pattern = "^" + regex_pattern.replace('।', '\\.?') + "$"
            
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
'''
    content = content.replace(template_old, template_new)

    with open('app/services/experimental_ho_translation/hi_ho_translator.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
update_translator()
