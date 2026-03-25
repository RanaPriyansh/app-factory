"""AI generation service with a local-first fallback mode."""
from __future__ import annotations

from textwrap import shorten
from typing import Optional

from config import settings
from utils.prompts import get_prompt


class ClaudeService:
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.AI_PROVIDER
        self.model = settings.CLAUDE_MODEL

    async def generate(self, prompt: str, user_input: str, system_prompt: Optional[str] = None) -> str:
        if self.provider == "anthropic":
            return await self._generate_with_anthropic(prompt=prompt, user_input=user_input, system_prompt=system_prompt)
        return self._generate_local(prompt=prompt, user_input=user_input, system_prompt=system_prompt)

    async def generate_for_app(self, app_type: str, user_input: str) -> str:
        system_prompt, prompt_template = get_prompt(app_type)
        return await self.generate(prompt=prompt_template, user_input=user_input, system_prompt=system_prompt)

    async def _generate_with_anthropic(self, prompt: str, user_input: str, system_prompt: Optional[str] = None) -> str:
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("AI_PROVIDER=anthropic requires ANTHROPIC_API_KEY")

        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise RuntimeError("anthropic package is not installed") from exc

        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model=self.model,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            system=system_prompt or "You are a helpful AI assistant.",
            messages=[
                {"role": "user", "content": prompt.format(input=user_input)}
            ],
        )
        return "".join(block.text for block in message.content if hasattr(block, "text")).strip()

    def _generate_local(self, prompt: str, user_input: str, system_prompt: Optional[str] = None) -> str:
        rendered_prompt = prompt.format(input=user_input).strip()
        summary = shorten(" ".join(user_input.split()), width=240, placeholder="...")
        sections = [
            "Teacher Assistant local demo output",
            "",
            f"System intent: {(system_prompt or 'Helpful classroom assistant').strip()}",
            f"Teacher request: {summary}",
            "",
            "Suggested lesson-plan draft:",
            "1. Learning objective: Define what students should know or do by the end of the lesson.",
            "2. Materials: List handouts, manipulatives, slides, and classroom setup needs.",
            "3. Mini-lesson: Introduce the topic with direct instruction and a quick model.",
            "4. Guided practice: Have students practice with teacher support and check-for-understanding prompts.",
            "5. Differentiation: Add scaffolds for struggling learners and an extension for advanced students.",
            "6. Assessment: Use an exit ticket or short formative check tied to the objective.",
            "7. Homework/extension: Reinforce the concept with one manageable follow-up task.",
            "",
            "Prompt used:",
            rendered_prompt,
        ]
        return "\n".join(sections).strip()
