from typing import Optional
from config import settings


class PromptBuilder:
    """
    Builds structured prompts for the NCERT RAG tutor.
    Updated to enforce step-by-step numerical calculations and LaTeX formatting.
    """

    # 🔥 REVISED SYSTEM PROMPT: Enforces "Chain of Thought" for math
    SYSTEM = (
        "You are GyaanSetu, an expert NCERT Science Tutor. "
        "You must follow these strict rules:\n"
        "1. STEP-BY-STEP CALCULATION: For every numerical or mathematical question, you MUST follow this structure:\n"
        "   - Given: (List the values provided in the question)\n"
        "   - Formula: (State the relevant NCERT formula)\n"
        "   - Substitution: (Show the numbers plugged into the formula and the calculation steps)\n"
        "   - Result: (The final answer clearly stated with units)\n"
        "2. DIRECT START: Do not use introductory filler. Start your response immediately with 'Given:' for numericals or the factual answer for theoretical questions.\n"
        "3. LaTeX FORMATTING: Use LaTeX for all mathematical expressions, equations, and units to ensure professional rendering.\n"
        "4. FLEXIBLE GROUNDING: Use the provided context as your primary source. If the context contains the necessary formulas but not the specific numerical, you ARE authorized to perform the calculation. Only refuse if the core concept or formula is completely missing."
    )

    # ==============================
    # 📄 STATELESS PROMPT
    # ==============================
    def build(self, context: list[str], question: str) -> str:
        context_text = self._format_context(context)
        return (
            f"{self.SYSTEM}\n\n"
            f"[NCERT Context]\n{context_text}\n\n"
            f"[Question]\n{question}\n\n"
            "Step-by-step Solution:"  # 🔥 Forces the model into 'Logic Mode'
        )

    # ==============================
    # 💬 CHAT PROMPT (multi-turn)
    # ==============================
    def build_chat(
        self,
        context: list[str],
        question: str,
        session_id: Optional[str] = None,
    ) -> str:
        context_text = self._format_context(context)
        return (
            f"{self.SYSTEM}\n\n"
            f"[NCERT Context]\n{context_text}\n\n"
            f"[Student Question]\n{question}\n\n"
            "Step-by-step Solution:"  # 🔥 Anchor for consistent tutor behavior
        )

    # ==============================
    # 🧹 CONTEXT FORMATTER
    # ==============================
    def _format_context(self, context: list[str]) -> str:
        seen = set()
        cleaned = []
        for chunk in context:
            chunk = chunk.strip()
            if chunk and chunk not in seen:
                seen.add(chunk)
                cleaned.append(chunk)

        joined = "\n".join(cleaned)

        if len(joined) > settings.MAX_CONTEXT_CHARS:
            joined = joined[:settings.MAX_CONTEXT_CHARS] + "..."

        return joined
