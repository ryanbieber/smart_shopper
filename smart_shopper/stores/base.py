"""Base class for store pipelines."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from smart_shopper.models import Product, Store


@dataclass
class StorePipeline(ABC):
    store: Store

    @abstractmethod
    def run(self) -> list[Product]:
        """Run the pipeline."""
        pass