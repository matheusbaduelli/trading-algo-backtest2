import os
import structlog
from typing import Any, Dict

def configure_logging() -> None:
    """Configurar logging estruturado JSON"""
    
    
    environment = os.getenv("ENVIRONMENT", "development")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    
    if environment == "development":
       
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    else:
        
        processors.append(structlog.processors.JSONRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(structlog.stdlib, log_level.upper(), structlog.stdlib.INFO)
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


configure_logging()


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Obter logger estruturado para um módulo"""
    return structlog.get_logger(name)