"""
Smart shopper package initialization.
"""

__version__ = "0.1.0"

from .client import client
from .email import EmailSender
from .models import Product, Store
from .stores.base import StorePipeline
from .tools import jitter
from .stores.costco.pipeline import CostcoPipeline


__all__ = [
    "client",
    "EmailSender",
    "Product",
    "Store",
    "StorePipeline",
    "jitter",
    "CostcoPipeline",
]

