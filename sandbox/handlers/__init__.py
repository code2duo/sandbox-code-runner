from .python import PythonHandler as _PythonHandler
from .c import CHandler as _CHandler
from .cpp import CPPHandler as _CPPHandler
from .java import JavaHandler as _JavaHandler

HandlerMapping = {
    "python": _PythonHandler,
    "c": _CHandler,
    "cpp": _CPPHandler,
    "java": _JavaHandler,
}
