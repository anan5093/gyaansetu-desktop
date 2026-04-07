from llm.gemma_client import GemmaClient
import requests


# ===============================
# 🔥 GLOBAL LLM CACHE (IMPORTANT)
# ===============================
_LLM_INSTANCE = None


class LLMFactory:

    @staticmethod
    def create():

        global _LLM_INSTANCE

        # 🔥 RETURN EXISTING INSTANCE (CRITICAL)
        if _LLM_INSTANCE is not None:
            return _LLM_INSTANCE

        try:
            print("⚙️ LLM Mode: GEMMA (LOCAL)")

            # 🔥 CHECK OLLAMA SERVER (FAST FAIL)
            if not LLMFactory._check_ollama():
                raise Exception("Ollama server not reachable")

            _LLM_INSTANCE = GemmaClient()

            print("✅ Gemma initialized (cached)")

            return _LLM_INSTANCE

        except Exception as e:
            print(f"⚠️ Gemma init failed: {e}")
            print("🔁 Falling back to basic response mode")

            _LLM_INSTANCE = FallbackLLM()
            return _LLM_INSTANCE

    # ===============================
    # 🔥 HEALTH CHECK (FAST)
    # ===============================
    @staticmethod
    def _check_ollama():

        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=2
            )

            return response.status_code == 200

        except:
            return False


# ===============================
# 🔥 FALLBACK LLM (SAFE MODE)
# ===============================
class FallbackLLM:

    def generate(self, prompt: str) -> str:
        return "⚠️ AI Tutor is temporarily unavailable. Please try again."
