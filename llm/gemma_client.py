import requests
import json
from typing import Optional
from config import settings

# ==============================
# 💬 IN-MEMORY CHAT HISTORY
# ==============================
_chat_histories: dict[str, list[dict]] = {}

def get_history(session_id: str) -> list[dict]:
    return _chat_histories.get(session_id, [])

def add_to_history(session_id: str, role: str, content: str):
    if session_id not in _chat_histories:
        _chat_histories[session_id] = []
    _chat_histories[session_id].append({"role": role, "content": content})
    
    # Keep history within reasonable bounds
    max_entries = settings.CHAT_MAX_HISTORY_TURNS * 2
    if len(_chat_histories[session_id]) > max_entries:
        _chat_histories[session_id] = _chat_histories[session_id][-max_entries:]

def clear_history(session_id: str):
    _chat_histories.pop(session_id, None)

# ==============================
# 🤖 GEMMA CLIENT (FIXED FOR NGROK)
# ==============================
class GemmaClient:
    def __init__(self):
        self.url = f"{settings.OLLAMA_HOST}/api/generate"
        self.model = settings.OLLAMA_MODEL
        self.session = requests.Session()
        
        # 🔥 CRITICAL: Skip ngrok's 403 browser warning page
        self.headers = {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning": "true",
            "User-Agent": "GyaanSetu-Tutor-Client"
        }

    def _call_ollama(self, prompt: str):
        """Generator that yields response chunks from Ollama with 403 fix."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "num_ctx": settings.LLM_NUM_CTX,
                    "num_thread": settings.LLM_NUM_THREADS,
                    "temperature": settings.LLM_TEMPERATURE,
                },
            }

            response = self.session.post(
                self.url,
                json=payload,
                headers=self.headers,  # 🔥 Injected fix for 403
                stream=True,
                timeout=settings.LLM_TIMEOUT,
            )

            if response.status_code != 200:
                yield f"⚠️ LLM Error (status {response.status_code})"
                return

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("response", "")
                        yield token
                        if chunk.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            yield f"⚠️ LLM error: {str(e)}"

    def generate(self, prompt: str, session_id: Optional[str] = None):
        """Main entry point that manages history and streaming."""
        full_prompt = self._build_chat_prompt(prompt, session_id) if session_id else prompt

        full_response = []
        for chunk in self._call_ollama(full_prompt):
            yield chunk
            full_response.append(chunk)

        # Update history only after successful stream completion
        if session_id and full_response:
            final_text = "".join(full_response).strip()
            # Only save if it's not an error message
            if "⚠️" not in final_text:
                add_to_history(session_id, "user", prompt)
                add_to_history(session_id, "assistant", final_text)

    # ==============================
    # 📜 HISTORY INJECTOR
    # ==============================
    def _build_chat_prompt(self, current_prompt: str, session_id: str) -> str:
        history = get_history(session_id)
        history_block = ""

        if history:
            lines = []
            for turn in history:
                role = "Student" if turn["role"] == "user" else "Tutor"
                lines.append(f"{role}: {turn['content']}")
            
            raw_history = "\n".join(lines)
            # Trim history to context window limits
            if len(raw_history) > settings.CHAT_MAX_HISTORY_CHARS:
                raw_history = "..." + raw_history[-settings.CHAT_MAX_HISTORY_CHARS:]
            
            history_block = f"\n[Previous conversation]\n{raw_history}\n"

        return f"{current_prompt}{history_block}\nResponse:"
