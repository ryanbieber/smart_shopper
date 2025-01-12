"""Main pipeline for the Smart Shopper project."""


import structlog
from smart_shopper.costco.pipeline import CostcoPipeline

logger = structlog.get_logger()

def main():
    """Main entry point of the application."""
    logger.info("Starting the Smart Shopper")
    costco_pipeline = CostcoPipeline()
    costco_products = costco_pipeline.get_all_products()
    logger.info("Finished the Smart Shopper")