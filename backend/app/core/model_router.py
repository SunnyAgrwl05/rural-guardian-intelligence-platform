from __future__ import annotations

import asyncio
from typing import Any

from app.agents.prompts import PROMPTS
from app.core.config import settings


class DemoModel:
    async def complete(self, route, text: str) -> str:
        if route.domain == "agriculture":
            return "🌾 AGRICULTURE PLAN\n\n1. Check field drainage before heavy rain.\n2. Prioritize mature crop where practical.\n3. Keep harvested grain protected from moisture.\n4. Inspect for fungal/pest damage after prolonged wet conditions.\n\n⚠️ Verify local weather and agronomy information before acting.\n\nDEMO MODE: connect Microsoft Foundry, OpenRouter, or another authorized provider for live model responses."
        if route.domain == "disaster":
            return "🚨 DISASTER SAFETY\n\nMove toward safer ground if local authorities advise evacuation. Avoid floodwater and downed electrical lines. Keep medicines, documents, water and a charged phone accessible.\n\n⚠️ Demo mode cannot verify a live government alert. Follow official local authorities."
        if route.domain == "health":
            return "🚨 HIGH-RISK HEALTH REQUEST\n\nI cannot diagnose this condition or recommend a medicine/dose. Serious symptoms can require urgent professional assessment. Seek qualified medical/emergency assistance and follow local emergency guidance."
        return f"I routed your request to {route.agent}. Connect an authorized model provider in .env for model-generated responses."


class OpenRouterModel:
    def __init__(self):
        from openai import AsyncOpenAI

        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is missing")
        self.client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url.rstrip("/"),
            default_headers=self._headers(),
            timeout=45.0,
            max_retries=2,
        )

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if settings.openrouter_http_referer:
            headers["HTTP-Referer"] = settings.openrouter_http_referer
        if settings.openrouter_app_name:
            headers["X-Title"] = settings.openrouter_app_name
        return headers

    async def complete(self, route, text: str) -> str:
        kwargs: dict[str, Any] = {
            "model": settings.openrouter_model,
            "messages": [
                {"role": "system", "content": PROMPTS.get(route.domain, PROMPTS["general"])},
                {"role": "user", "content": text},
            ],
            "temperature": 0.2,
        }
        fallback = [m.strip() for m in settings.openrouter_fallback_models.split(",") if m.strip()]
        if fallback:
            kwargs["extra_body"] = {"models": fallback[:3]}
        response = await self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenRouter returned an empty response")
        return content


class FoundryModel:
    def __init__(self):
        from azure.identity import DefaultAzureCredential
        from azure.ai.projects import AIProjectClient

        if not settings.foundry_project_endpoint or not settings.foundry_agent_name:
            raise RuntimeError("Foundry settings missing")
        project = AIProjectClient(
            endpoint=settings.foundry_project_endpoint,
            credential=DefaultAzureCredential(),
        )
        self.client = project.get_openai_client(agent_name=settings.foundry_agent_name)

    async def complete(self, route, text: str) -> str:
        def call():
            return self.client.responses.create(
                input=[
                    {
                        "role": "system",
                        "content": [{"type": "input_text", "text": PROMPTS.get(route.domain, PROMPTS["general"])}],
                    },
                    {"role": "user", "content": [{"type": "input_text", "text": text}]},
                ]
            )

        response = await asyncio.to_thread(call)
        return response.output_text


class AzureOpenAIModel:
    def __init__(self):
        from openai import AsyncOpenAI

        if not settings.azure_openai_endpoint or not settings.azure_openai_api_key or not settings.azure_openai_deployment:
            raise RuntimeError("Azure OpenAI settings missing")
        self.client = AsyncOpenAI(
            api_key=settings.azure_openai_api_key,
            base_url=settings.azure_openai_endpoint.rstrip("/") + "/openai/v1/",
            timeout=45.0,
            max_retries=2,
        )

    async def complete(self, route, text: str) -> str:
        response = await self.client.responses.create(
            model=settings.azure_openai_deployment,
            instructions=PROMPTS.get(route.domain, PROMPTS["general"]),
            input=text,
        )
        return response.output_text


def build_model():
    if settings.model_provider == "openrouter":
        return OpenRouterModel()
    if settings.model_provider == "foundry":
        return FoundryModel()
    if settings.model_provider == "azure_openai":
        return AzureOpenAIModel()
    return DemoModel()
