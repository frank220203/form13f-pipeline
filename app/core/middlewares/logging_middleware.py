import time
import json

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from api.deps.di_manager import get_logger_manager

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        self.logger = get_logger_manager().get_logger()
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next:RequestResponseEndpoint):
        start_time = time.time()
        request_body_str = None

        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                request_body = request.body()

                if request_body:
                    request_body_str = request_body.decode('utf-8')
                    request._body = request_body

                    if 'application/json' in request.headers.get('content-type', ''):
                        try:
                            request_body_json = json.loads(request_body_str)
                            self.logger.info(f"[Request - {request.method}][{request.url}][{request.client.host}:{request.client.port}] --- Request Body : {request_body_json}")
                        except json.JSONDecodeError:
                            self.logger.warning(f"Request Body is not JSON : {request_body_str}")
                    else:
                        self.logger.info(f"[Request - {request.method}][{request.url}][{request.client.host}:{request.client.port}] --- Request Body : {request_body_str}")
            except Exception as e:
                self.logger.error(f"Error reading request body : {e}")
        else:
            self.logger.info(f"[Request - {request.method}][{request.url}][{request.client.host}:{request.client.port}]")

        response = Response("Internal Server Error", status_code=500)
        response_body = None
        response_body_bytes = b""
        ori_response = None

        try:
            ori_response = await call_next(request)
            content_type = ori_response.headers.get('content-type', '')

            if "application/json" in content_type:
                async for chunk in ori_response.body_iterator:
                    response_body_bytes += chunk
                response_body = response_body_bytes.decode('utf-8')
                response = JSONResponse(
                    content=json.loads(response_body),
                    status_code=ori_response.status_code,
                    headers=dict(ori_response.headers)
                )
            elif "text/" in content_type:
                async for chunk in ori_response.body_iterator:
                    response_body_bytes += chunk
                response_body = response_body_bytes.decode('utf-8')
                response = Response(
                    content=response_body,
                    media_type=content_type,
                    status_code=ori_response.status_code,
                    headers=dict(ori_response.headers)
                )
            else:
                response = ori_response
        except Exception as e:
            self.logger.error(f"[Request - {request.method}][{request.url}][{request.client.host}:{request.client.port}] --- Error : {e}", exc_info=True)
            response = JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
        finally:
            process_time = time.time() - start_time
            log_msg = f"[Response - {response.status_code}][{request.client.host}:{request.client.port}] --- Response Body : {response_body} --- {process_time:.4f}s"
            # 포트폴리오 반환값이 긴 경우 임시로 빈 값 줌
            # log_msg = ""

            if response.status_code >= 500:
                self.logger.error(log_msg)
            elif response.status_code >= 400:
                self.logger.warning(log_msg)
            else:
                self.logger.info(log_msg)
        return response