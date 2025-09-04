import pytest
import asyncio
from api.deps import di_manager
from core.external_interfaces.gemini_prompt import GeminiPrompt

# Kafka Consumer 통합 테스트
# 비동기로 작동하는 Kafka를 사용하므로 asynio 사용
@pytest.mark.asyncio
async def test_get_response() -> None:
    # Mock
    # Mocking
    # 통합 테스트는 모킹 과정 생략

    # When
    prompt = GeminiPrompt(di_manager.get_config_manager())
    msg = await asyncio.wait_for(prompt.get_naics(["02005N100"]), timeout=5.0)

    # Then
    assert "Gemini answered" in msg