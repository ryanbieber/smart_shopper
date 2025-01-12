"""COstco pipeline module."""
import structlog
from bs4 import BeautifulSoup
import re
import json
from smart_shopper.client import client
from smart_shopper.models import Product, CostcoCategories, Store
from smart_shopper.tools import jitter
from dataclasses import dataclass

logger = structlog.get_logger()

@dataclass
class CostcoPipeline:

    category: CostcoCategories
    page_size: int = 24
    pages: int = 20
    store: Store = "costco"

    def get_all_products(self) -> list[str]:
        page_data = []
        for page in range(1, self.pages+1):
            try:
                url = f"https://www.costco.com/{self.category.value}.html?currentPage={page}&dept=All&pageSize={self.page_size}&sortBy=item_page_views+desc&keyword=OFF&dept=All"
                page = client.request("get", url)
                jitter()
                page_data.append(
                    BeautifulSoup(page.content, 'html.parser')
                )
                if page == 20:
                    break
            except Exception as e:
                logger.error(f"Failed to get page {page} with error {e}")
                break
        return page_data

    def get_all_product_info(self, category_data: list[str]) -> list[str]:
        product_info = []
        for product in category_data:
            try:
                url = product.find_all("a", {"class": "product-image-url"})
                for uri in url:
                    href = uri.get("href")
                    page = client.request("get", href)
                    product_info.append(
                        BeautifulSoup(page.content, 'html.parser')
                    )
                    jitter()
            except Exception as e:
                logger.error(f"Failed to get product info with error {e}")
        return product_info

    def get_all_names_and_discounts(self, product_info: list[str]) -> list[Product]:
        products = []
        for product in product_info:
            scripts = product.find_all("script")
            canonical_link = product.find("link", {"rel": "canonical"})["href"]
            pattern = r"window\.digitalData\s*=\s*\{[\s\S]*?\};?"
            products = []
            for script in scripts:
                if script.string:
                    match = re.search(pattern, script.string)
                    if match:
                        name = re.search(r"name\s*:\s*'(.*)'", script.string).group(1)
                        price_min = re.search(r"priceMin\s*:\s*'(.*)'", script.string).group(1)
                        price_max = re.search(r"priceMax\s*:\s*'(.*)'", script.string).group(1)
                        inventory_status = re.search(r"inventoryStatus\s*:\s*'(.*)'", script.string).group(1)
                        page_crumbs = re.search(r"pageCrumbs\s*:\s*\[(.*)\]", script.string).group(1)
                        sku = re.search(r"sku\s*:\s*'(.*)'", script.string).group(1)
                        if sku == "":
                            continue
                        logger.info(f"Name: {name}, Price Min: {price_min}, Price Max: {price_max}, Inventory Status: {inventory_status}, Page Crumbs: {page_crumbs}, SKU: {sku}")
                        discount = float(price_max) - float(price_min)
                        products.append(
                            Product(
                                store=self.store,
                                name=name,
                                discount=discount,
                                price_min=price_min,
                                price_max=price_max,
                                inventory_status=inventory_status,
                                page_crumbs=page_crumbs,
                                sku=sku,
                                link=canonical_link
                            )
                        )
        return products

    def run(self) -> list[Product]:
        products = self.get_all_products()
        product_info = self.get_all_product_info(products)
        return self.get_all_names_and_discounts(product_info)
