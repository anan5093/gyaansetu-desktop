import re
from typing import Optional
from config import settings


class RAGService:
    """
    Core RAG pipeline for GyaanSetu NCERT Tutor.
    Modified to support real-time streaming while preserving all original logic.
    """

    # ==============================
    # 🏗️ INIT — reads all limits from settings
    # ==============================
    def __init__(self, vector_store, llm_client, prompt_builder):
        self.store          = vector_store      # FAISSLoader instance
        self.llm            = llm_client        # GemmaClient instance
        self.prompt_builder = prompt_builder    # PromptBuilder instance

        # Pull tuning values from central config — no hardcoding
        self.top_k           = settings.TOP_K
        self.score_threshold = settings.SCORE_THRESHOLD
        self.max_ctx_chars   = settings.MAX_CONTEXT_CHARS

    # ==============================
    # 🔍 RETRIEVAL
    # ==============================
    def retrieve(self, question: str) -> list[dict]:
        """Queries FAISS and filters by score threshold."""
        results = self.store.search(question, k=self.top_k) or []
        filtered = [
            c for c in results
            if isinstance(c, dict) and c.get("score", 0) >= self.score_threshold
        ]
        if settings.ENABLE_LOGS:
            print(f"[RAG] Retrieved {len(filtered)}/{len(results)} chunks above threshold {self.score_threshold}")
        return filtered

    # ==============================
    # 🧹 TEXT CLEANER
    # ==============================
    def _clean_text(self, text: str) -> str:
        """Strips FAISS metadata noise from stored chunk text."""
        noise_tags = [
            "=== CONCEPT ===",
            "=== EXAM QUESTION ===",
            "Topic:",
            "Explanation:",
            "Question:",
            "Answer:",
            "Difficulty:",
            "Type:",
        ]
        for tag in noise_tags:
            text = text.replace(tag, "")

        # Regex to destroy floating difficulty/complexity tags
        text = re.sub(r'\b(Easy|Medium|Hard)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(General|Conceptual|Numerical)\b', '', text, flags=re.IGNORECASE)

        # Collapse multiple blank spaces and newlines
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"\n{2,}", "\n", text)
        return text.strip()

    # ==============================
    # ⚡ SIMPLE QUESTION DETECTOR
    # ==============================
    def _is_simple_question(self, question: str) -> bool:
        q = question.lower().strip()
        simple_prefixes = ("what is", "what are", "define", "formula for", "full form of")
        return any(q.startswith(p) for p in simple_prefixes)

    # ==============================
    # 🧠 CONTEXT BUILDER
    # ==============================
    def _build_context_chunks(self, chunks: list[dict]) -> list[str]:
        seen    = set()
        result  = []
        total   = 0

        for c in chunks:
            raw = c.get("text", "").strip()
            if not raw:
                continue

            text = self._clean_text(raw)
            if text in seen:
                continue
            seen.add(text)

            lines = [l.strip() for l in text.split("\n") if l.strip()]
            text  = " ".join(lines)

            if total + len(text) > self.max_ctx_chars:
                remaining = self.max_ctx_chars - total
                if remaining > 80:
                    result.append(text[:remaining] + "...")
                break

            result.append(text)
            total += len(text)

        return result

    # ==============================
    # ⚡ FAST PATH ANSWER
    # ==============================
    def _fast_answer(self, chunks: list[dict]) -> str:
        raw       = chunks[0].get("text", "")
        clean     = self._clean_text(raw)
        sentences = [s.strip() + "." for s in clean.split(".") if s.strip()]
        answer = " ".join(sentences[:2])
        return answer if sentences else clean

    # ==============================
    # 🤖 CORE PIPELINE (STREAMING ENABLED)
    # ==============================
    def process_query(
        self,
        question: str,
        session_id: Optional[str] = None,
        stream: bool = False  # 🔥 Added parameter to control streaming
    ) -> dict:
        """
        Modified to return a generator if stream=True and in LLM mode.
        """
        # ── Step 1: Retrieve ──────────────────────────────────────────────
        chunks = self.retrieve(question)

        if not chunks:
            return {
                "answer": "I don't have enough information in the current NCERT chapter to answer that.",
                "chunks": [],
                "context": [],
                "mode": "fallback"
            }

        # ── Step 2: Fast path ─────────────────────────────────────────────
        if self._is_simple_question(question):
            answer = self._fast_answer(chunks)
            return {"answer": answer, "chunks": chunks, "context": [], "mode": "fast"}

        # ── Step 3: Build context ─────────────────────────────────────────
        context_list = self._build_context_chunks(chunks)

        if not context_list:
            return {
                "answer": "I don't have enough information in the current NCERT chapter to answer that.",
                "chunks": chunks,
                "context": [],
                "mode": "fallback"
            }

        # ── Step 4: Build prompt ──────────────────────────────────────────
        if session_id:
            prompt = self.prompt_builder.build_chat(context_list, question, session_id)
        else:
            prompt = self.prompt_builder.build(context_list, question)

        # ── Step 5: Generate (Streaming or Synchronous) ──────────────────
        if stream:
            # 🔥 Return the generator directly from GemmaClient
            return {
                "answer_stream": self.llm.generate(prompt, session_id=session_id),
                "chunks": chunks,
                "context": context_list,
                "mode": "llm"
            }
        
        # Original Synchronous Flow
        answer = self.llm.generate(prompt, session_id=session_id)
        if answer:
            answer = self._clean_text(answer)
        
        # Failsafe for empty LLM response
        if not answer or len(answer) < 5:
            sentences = [s.strip() + "." for s in " ".join(context_list).split(".") if s.strip()]
            answer = " ".join(sentences[:2])

        return {
            "answer": answer.strip(),
            "chunks": chunks,
            "context": context_list,
            "mode": "llm",
        }

    # ==============================
    # 🔁 STREAMING WRAPPERS
    # ==============================
    def ask(self, question: str, session_id: Optional[str] = None):
        """
        Now a generator function. 
        Compatible with st.write_stream in ui/app.py.
        """
        # Call process_query in streaming mode
        result = self.process_query(question, session_id=session_id, stream=True)

        if result["mode"] in ["fast", "fallback"]:
            # Yield the static string immediately
            yield result["answer"]
        else:
            # Yield chunks as they arrive from the LLM generator
            yield from result["answer_stream"]

    def ask_with_debug(self, question: str, session_id: Optional[str] = None):
        """Dev/eval helper — uses synchronous mode for clean terminal printing."""
        result = self.process_query(question, session_id=session_id, stream=False)

        print(f"\n{'='*50}")
        print(f"❓ Question : {question}")
        print(f"⚙️  Mode     : {result['mode']}")
        print(f"\n🔎 Retrieved Chunks ({len(result['chunks'])}):")
        for i, c in enumerate(result["chunks"]):
            print(f"  {i+1}. Score: {c.get('score', 0):.4f} | Topic: {c.get('topic')}")

        print(f"\n💬 Answer:\n{result['answer']}")
        print(f"{'='*50}\n")

        return result["answer"], result["chunks"]
