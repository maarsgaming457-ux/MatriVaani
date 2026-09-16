import os
from app.core.config import settings
from app.core.logging_config import logger
from app.core.exceptions import TranslationError

class TranslationService:
    def __init__(self):
        self.provider = settings.TRANSLATION_PROVIDER
        self._bhashini_config_cache = {}
        
    def _normalize_lang(self, lang: str) -> str:
        lang = lang.lower().strip()
        if lang in ["sat", "santali", "santhali"]:
            return "Santali"
        if lang in ["hi", "hindi"]:
            return "Hindi"
        if lang in ["ho", "hoc"]:
            return "Ho"
        raise ValueError(f"Unsupported language: {lang}")

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text:
            return ""
            
        try:
            norm_source = self._normalize_lang(source_lang)
            norm_target = self._normalize_lang(target_lang)
        except ValueError as e:
            logger.error(f"Translation failed: {e}")
            raise TranslationError(str(e))
            
        logger.info(f"Translating via provider '{self.provider}': {norm_source} -> {norm_target}")
        
        if (norm_source == "Ho" or norm_target == "Ho") and self.provider != "mock":
            raise TranslationError(f"Translation provider '{self.provider}' does not support Ho.")
            
        try:
            if self.provider == "mock":
                return self._mock_translate(text, norm_source, norm_target)
            elif self.provider == "groq":
                return self._groq_translate(text, norm_source, norm_target)
            elif self.provider == "openai":
                return self._openai_translate(text, norm_source, norm_target)
            elif self.provider == "bhashini":
                return self._bhashini_translate(text, norm_source, norm_target)
            elif self.provider == "indictrans2":
                return self._indictrans2_translate(text, norm_source, norm_target)
            elif self.provider == "indictrans2_local":
                return self._indictrans2_local_translate(text, norm_source, norm_target)
            else:
                logger.warning(f"Unknown translation provider: {self.provider}. Falling back to groq.")
                if norm_source == "Ho" or norm_target == "Ho":
                    raise TranslationError("Groq fallback does not support Ho.")
                return self._groq_translate(text, norm_source, norm_target)
        except Exception as e:
            logger.error(f"Translation execution failed: {e}")
            raise TranslationError(str(e))

    def _mock_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        return f"[MOCK {target_lang.upper()}] Translated from {source_lang}: {text}"

    def _openai_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY is missing. Returning NOT_CONFIGURED.")
            return "[NOT_CONFIGURED] Translation requires OPENAI_API_KEY."
            
        with open("app/prompts/translator.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
            
        prompt = prompt_template.format(
            source_language=source_lang,
            target_language=target_lang,
            source_text=text
        )
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()

    def _groq_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        import openai
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY is missing. Returning NOT_CONFIGURED.")
            return "[NOT_CONFIGURED] Translation requires GROQ_API_KEY."
            
        with open("app/prompts/translator.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
            
        prompt = prompt_template.format(
            source_language=source_lang,
            target_language=target_lang,
            source_text=text
        )
        
        client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()

    def _bhashini_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        import requests
        
        user_id = os.getenv("BHASHINI_USER_ID")
        api_key = os.getenv("BHASHINI_API_KEY")
        pipeline_id = os.getenv("BHASHINI_PIPELINE_ID")
        
        if not user_id or not api_key or not pipeline_id:
            logger.warning("Bhashini credentials missing. BHASHINI_USER_ID, BHASHINI_API_KEY, BHASHINI_PIPELINE_ID required.")
            return "[NOT_CONFIGURED] Bhashini translation requires credentials."
            
        bhashini_lang_map = {
            "Hindi": "hi",
            "Santali": "sat"
        }
        
        src = bhashini_lang_map.get(source_lang)
        tgt = bhashini_lang_map.get(target_lang)
        
        if not src or not tgt:
            raise TranslationError(f"Unsupported Bhashini language mapping for {source_lang} -> {target_lang}")
            
        cache_key = f"{src}_{tgt}"
        service_id = self._bhashini_config_cache.get(cache_key)
        
        headers = {
            "userID": user_id,
            "ulcaApiKey": api_key,
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        if not service_id:
            logger.info(f"Bhashini config lookup for {src} -> {tgt}")
            config_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
            config_payload = {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": src,
                                "targetLanguage": tgt
                            }
                        }
                    }
                ],
                "pipelineRequestConfig": {
                    "pipelineId": pipeline_id
                }
            }
            
            try:
                conf_res = requests.post(config_url, json=config_payload, headers=headers, timeout=10)
                conf_res.raise_for_status()
                conf_data = conf_res.json()
                
                # Find translation task
                for task in conf_data.get("pipelineResponseConfig", []):
                    if task.get("taskType") == "translation":
                        for config in task.get("config", []):
                            service_id = config.get("serviceId")
                            if service_id:
                                break
                    if service_id:
                        break
                        
                if not service_id:
                    raise TranslationError("Could not discover serviceId for the requested language pair in Bhashini pipeline.")
                    
                self._bhashini_config_cache[cache_key] = service_id
                logger.info(f"Bhashini service selected: {service_id}")
            except Exception as e:
                logger.error("Bhashini config lookup failed.")
                raise TranslationError(f"Bhashini configuration failed: {str(e)}")
                
        # Inference
        logger.info("Bhashini translation requested")
        inference_url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
        
        inference_payload = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": src,
                            "targetLanguage": tgt
                        },
                        "serviceId": service_id
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": text
                    }
                ]
            }
        }
        
        try:
            inf_res = requests.post(inference_url, json=inference_payload, headers=headers, timeout=15)
            inf_res.raise_for_status()
            inf_data = inf_res.json()
            
            # Parse output
            for resp in inf_data.get("pipelineResponse", []):
                if resp.get("taskType") == "translation":
                    for out in resp.get("output", []):
                        if "target" in out:
                            logger.info("Bhashini translation completed")
                            return out["target"].strip()
                            
            raise TranslationError("Bhashini response did not contain translated text.")
        except Exception as e:
            logger.error("Bhashini inference failed.")
            raise TranslationError(f"Bhashini inference failed: {str(e)}")

    def _indictrans2_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        import urllib.request
        import json
        
        endpoint = os.getenv("INDICTRANS2_API_URL")
        if not endpoint:
            logger.warning("INDICTRANS2_API_URL is missing. Returning NOT_CONFIGURED.")
            return "[NOT_CONFIGURED] IndicTrans2 remote endpoint is required."
            
        indic_map = {
            "Hindi": "hi",
            "Santali": "sat"
        }
        
        src = indic_map.get(source_lang)
        tgt = indic_map.get(target_lang)
        
        if not src or not tgt:
            raise TranslationError(f"Unsupported language for IndicTrans2: {source_lang} -> {target_lang}")
            
        # The URL must end with /translate
        api_url = endpoint.rstrip('/') + '/translate'
            
        payload = {
            "text": text,
            "source_lang": src,
            "target_lang": tgt
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=20) as res:
                if res.status != 200:
                    raise TranslationError(f"IndicTrans2 returned HTTP {res.status}")
                response_data = json.loads(res.read().decode('utf-8'))
                
                if "translation" in response_data:
                    return response_data["translation"].strip()
                raise TranslationError("IndicTrans2 remote response did not contain 'translation'.")
        except urllib.error.URLError as e:
            logger.error(f"IndicTrans2 remote inference failed: {e}")
            raise TranslationError(f"IndicTrans2 connection failed: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"IndicTrans2 response was not valid JSON: {e}")
            raise TranslationError(f"IndicTrans2 JSON error: {str(e)}")
        except Exception as e:
            logger.error(f"IndicTrans2 remote inference failed: {e}")
            raise TranslationError(f"IndicTrans2 inference failed: {str(e)}")

    def _indictrans2_local_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        import urllib.request
        import json
        
        indic_map = {
            "Hindi": "hin_Deva",
            "Santali": "sat_Olck"
        }
        
        src = indic_map.get(source_lang)
        tgt = indic_map.get(target_lang)
        
        if not src or not tgt:
            raise TranslationError(f"Unsupported language for Local IndicTrans2: {source_lang} -> {target_lang}")
            
        api_url = 'http://127.0.0.1:8001/translate'
            
        payload = {
            "text": text,
            "source_lang": src,
            "target_lang": tgt
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        
        try:
            # High timeout since CPU inference takes ~15 seconds per request
            with urllib.request.urlopen(req, timeout=45) as res:
                if res.status != 200:
                    raise TranslationError(f"Local IndicTrans2 returned HTTP {res.status}")
                response_data = json.loads(res.read().decode('utf-8'))
                
                if "translation" in response_data:
                    return response_data["translation"].strip()
                raise TranslationError("Local IndicTrans2 response did not contain 'translation'.")
        except urllib.error.URLError as e:
            logger.error(f"Local IndicTrans2 connection failed: {e}")
            raise TranslationError(f"Local IndicTrans2 connection failed. Ensure WSL server is running. Error: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Local IndicTrans2 response was not valid JSON: {e}")
            raise TranslationError(f"Local IndicTrans2 JSON error: {str(e)}")
        except Exception as e:
            logger.error(f"Local IndicTrans2 inference failed: {e}")
            raise TranslationError(f"Local IndicTrans2 inference failed: {str(e)}")

