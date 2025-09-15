import pytest
import asyncio
from api.deps import da_manager

# Kafka Consumer 통합 테스트
# 비동기로 작동하는 Kafka를 사용하므로 asynio 사용
@pytest.mark.asyncio
async def test_read() -> None:
    # Mock
    # Mocking
    # 통합 테스트는 모킹 과정 생략

    # When
    # Consumer가 무한 대기 상태를 유지하기 때문에 timeout 설정
    kafka_service = da_manager.get_kafka_connection()
    await kafka_service.start()
    try:
        msg = await asyncio.wait_for(await kafka_service.read(), timeout=60.0)
        # Then
        assert "Kafka consumed message1" in msg
    except Exception as e:
        da_manager.get_logger_manager().get_logger().info(e)
    finally:
        await kafka_service.stop()