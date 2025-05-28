"""
Configuration for Distill CLI
"""
import os

DEFAULT_MAX_LINES = 20
DEFAULT_FORMAT = "text"

config = {
    "max_lines": int(os.environ.get("DISTILL_MAX_LINES", DEFAULT_MAX_LINES)),
    "format": os.environ.get("DISTILL_FORMAT", DEFAULT_FORMAT),
}