# property-service/src/api/__init__.py
"""
Property Service API Package
"""

try:
    from .routes import *
except ImportError:
    pass