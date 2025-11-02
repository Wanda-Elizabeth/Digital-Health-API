from .patients import router as patients_router
from .encounters import router as encounters_router

__all__ = ["patients_router", "encounters_router"]
