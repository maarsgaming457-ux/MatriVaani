import os
import json
from app.core.config import settings
from app.core.logging_config import logger
from app.core.exceptions import ScriptGenerationError, CopyEditingError

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        
    def _call_groq_json(self, prompt_template_path: str, format_kwargs: dict) -> dict:
        import openai
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY is missing. Returning NOT_CONFIGURED.")
            return {"error": "GROQ_API_KEY is missing."}
            
        with open(prompt_template_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
            
        prompt = prompt_template.format(**format_kwargs)
        client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return json.loads(response.choices[0].message.content)

    def generate_script(self, translated_text: str) -> dict:
        if not translated_text:
            return {"title": "Empty Script", "script": ""}
        logger.info(f"Generating script via provider '{self.provider}'")
        try:
            if self.provider == "groq":
                return self._call_groq_json("app/prompts/scriptwriter.txt", {"source_text": translated_text})
            elif self.provider == "mock":
                return self._mock_generate_script(translated_text)
            else:
                return self._mock_generate_script(translated_text)
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            raise ScriptGenerationError(f"Script generation failed: {str(e)}")

    def copy_edit(self, generated_script: str) -> str:
        if not generated_script:
            return ""
        logger.info(f"Copy editing via provider '{self.provider}'")
        try:
            if self.provider == "groq":
                import openai
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key: return "[NOT_CONFIGURED] Copy Editor requires GROQ_API_KEY."
                with open("app/prompts/copy_editor.txt", "r", encoding="utf-8") as f:
                    prompt = f.read().format(script_text=generated_script)
                client = openai.OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                response = client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            return self._mock_copy_edit(generated_script)
        except Exception as e:
            raise CopyEditingError(f"Copy editing failed: {str(e)}")

    def generate_lesson(self, class_level, subject, topic, learning_objective, language) -> dict:
        logger.info(f"Generating lesson via '{self.provider}'")
        if self.provider == "groq":
            return self._call_groq_json("app/prompts/lesson_generator.txt", {
                "class_level": class_level, "subject": subject, "topic": topic,
                "learning_objective": learning_objective, "language": language
            })
        return {"title": "[MOCK] Lesson", "learning_objective": learning_objective}

    def generate_worksheet(self, class_level, subject, topic, language, difficulty, num_questions) -> dict:
        logger.info(f"Generating worksheet via '{self.provider}'")
        if self.provider == "groq":
            return self._call_groq_json("app/prompts/worksheet_generator.txt", {
                "class_level": class_level, "subject": subject, "topic": topic,
                "language": language, "difficulty": difficulty, "num_questions": num_questions
            })
        return {"title": "[MOCK] Worksheet", "questions": []}

    def generate_flashcards(self, class_level, topic, language) -> dict:
        logger.info(f"Generating flashcards via '{self.provider}'")
        if self.provider == "groq":
            return self._call_groq_json("app/prompts/flashcard_generator.txt", {
                "class_level": class_level, "topic": topic, "language": language
            })
        return {"flashcards": []}

    def _mock_generate_script(self, text: str) -> dict:
        return {"title": "Mock Script", "main_content": text}
        
    def _mock_copy_edit(self, text: str) -> str:
        return f"[EDITED] {text}"
