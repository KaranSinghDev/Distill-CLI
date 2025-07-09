"""
Configuration for Distill CLI
"""
import os

DEFAULT_MAX_LINES = 20
DEFAULT_FORMAT = "text"
DEFAULT_OUTPUT_TYPE = "generic"

config = {
    "max_lines": int(os.environ.get("DISTILL_MAX_LINES", DEFAULT_MAX_LINES)),
    "format": os.environ.get("DISTILL_FORMAT", DEFAULT_FORMAT),
    "output_type": os.environ.get("DISTILL_TYPE", DEFAULT_OUTPUT_TYPE),
}

__all__ = ["DEFAULT_MAX_LINES", "DEFAULT_FORMAT", "DEFAULT_OUTPUT_TYPE", "config"]