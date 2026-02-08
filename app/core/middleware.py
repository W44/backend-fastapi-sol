"""
Middleware for the Seashell API.
Handles request/response logging and timing.
"""
import time
from fastapi import Request
from app.core.logging_config import get_logger

logger = get_logger(__name__)


async def log_requests(request: Request, call_next):
    """
    Log all incoming requests and responses with timing.
    This runs for every API call.
    """
    start_time = time.time()
    
    # Log the incoming request
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate how long it took
    process_time = time.time() - start_time
    
    # Log the response
    logger.info(
        f"Request completed: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Time: {process_time:.3f}s"
    )
    
    return response
