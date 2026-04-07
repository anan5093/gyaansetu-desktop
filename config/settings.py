import os

# ==============================
# 🔧 UTILITY HELPERS
# ==============================
def get_bool(key: str, default: str = "true") -> bool:
    return os.getenv(key, default).lower() in ["true", "1", "yes"]

def get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default

def get_float(key: str, default: float) -> float:
    try:
        return float(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default


# ==============================
# ⚙️ SETTINGS
# ==============================
class Settings:

    # ==============================
    # 📂 Core Paths
    # ==============================
    # Resolves to the main GyaanSetu directory
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))

    # ==============================
    # 📘 Dataset Config
    # ==============================
    CLASS_ID: int  = get_int("CLASS_ID", 10)
    SUBJECT:  str  = os.getenv("SUBJECT", "science")

    # ==============================
    # 🔎 Retrieval Config (FAISS)
    # ==============================
    TOP_K:            int   = get_int("TOP_K", 7) 
    # Set to 0.20 to capture better context while filtering noise
    SCORE_THRESHOLD:  float = get_float("SCORE_THRESHOLD", 0.20)

    # ==============================
    # 🤖 LLM Config (Ollama / Gemma 4 via Colab)
    # ==============================
    USE_GEMMA:       bool = get_bool("USE_GEMMA", "true")
    
    # 🔥 UPDATED: Ngrok Tunnel URL for Colab Backend
    OLLAMA_HOST:     str  = os.getenv("OLLAMA_HOST", "https://gavyn-supersquamosal-meaghan.ngrok-free.dev")
    
    # Target Model for Competition
    OLLAMA_MODEL:    str  = os.getenv("OLLAMA_MODEL", "gemma4:e2b")
    
    LLM_NUM_THREADS: int  = get_int("LLM_NUM_THREADS", 6)
    LLM_NUM_CTX:     int  = get_int("LLM_NUM_CTX", 2048)   # Increased for stable multi-chunk reasoning
    LLM_NUM_PREDICT: int  = get_int("LLM_NUM_PREDICT", 1024) # High limit for long numerical steps
    LLM_TEMPERATURE: float = get_float("LLM_TEMPERATURE", 0.1) # Strict facts, no creative hallucination
    LLM_TIMEOUT:     int  = get_int("LLM_TIMEOUT", 120)       # High timeout for cloud-tunnel stability

    # ==============================
    # 💬 Chat / Session Config
    # ==============================
    CHAT_MAX_HISTORY_TURNS: int = get_int("CHAT_MAX_HISTORY_TURNS", 6)
    CHAT_MAX_HISTORY_CHARS: int = get_int("CHAT_MAX_HISTORY_CHARS", 1800)

    # ==============================
    # 🧩 Prompt / Context Config
    # ==============================
    MAX_CONTEXT_CHARS: int = get_int("MAX_CONTEXT_CHARS", 1500)

    # ==============================
    # ⚡ API Config
    # ==============================
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = get_int("API_PORT", 8000)

    # ==============================
    # 🧪 Debug / Logging
    # ==============================
    ENABLE_LOGS: bool = get_bool("ENABLE_LOGS", "true")


# ✅ Singleton instance for the application
settings = Settings()

# ==============================
# 🔥 BACKWARD COMPATIBILITY EXPORTS
# ==============================
BASE_DIR          = settings.BASE_DIR
DATA_DIR          = settings.DATA_DIR
CLASS_ID          = settings.CLASS_ID
SUBJECT           = settings.SUBJECT
TOP_K             = settings.TOP_K
SCORE_THRESHOLD   = settings.SCORE_THRESHOLD
ENABLE_LOGS       = settings.ENABLE_LOGS

OLLAMA_HOST            = settings.OLLAMA_HOST
OLLAMA_MODEL           = settings.OLLAMA_MODEL
LLM_NUM_THREADS        = settings.LLM_NUM_THREADS
LLM_NUM_CTX            = settings.LLM_NUM_CTX
LLM_NUM_PREDICT        = settings.LLM_NUM_PREDICT
LLM_TEMPERATURE        = settings.LLM_TEMPERATURE
LLM_TIMEOUT            = settings.LLM_TIMEOUT
CHAT_MAX_HISTORY_TURNS = settings.CHAT_MAX_HISTORY_TURNS
CHAT_MAX_HISTORY_CHARS = settings.CHAT_MAX_HISTORY_CHARS
MAX_CONTEXT_CHARS      = settings.MAX_CONTEXT_CHARS
