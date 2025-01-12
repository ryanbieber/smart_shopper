"""Base Models for the Smart Shopper"""

from enum import Enum
from pydantic import BaseModel, Field

class Catagories(str, Enum):
    COFFEE = "coffee"
    MEAT = "meat"
    PAPER_GOODS = "paper_goods"
    CLEANING_SUPPLIES = "cleaning_supplies"
    PERSONAL_CARE = "personal_care"
    SNACKS = "snacks"
    BEVERAGES = "beverages"
    DAIRY = "dairy"
    FROZEN = "frozen"
    CONDIMENTS = "condiments"
    SPICES = "spices"
    BABY_CARE = "baby_care"
    PET_SUPPLIES = "pet_supplies"
    OFFICE_SUPPLIES = "office_supplies"
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FURNITURE = "furniture"
    HOME_DECOR = "home_decor"


class CostcoCategories(str, Enum):
    GROCERY = 'grocery-household'
    HEALTH_BEAUTY = 'health-beauty'
    ELECTRONICS = 'electronics'
    HOME_AND_DECOR = 'home-and-decor'
    BEAUTY = 'beauty'

class Store(str, Enum):
    COSTCO = "costco"

class Product(BaseModel):
    store: Store = Field(description="The store the product is from")
    name: str  = Field(description="The name of the product")
    discount: float = Field(description="The discount on the product")
    price_min: float = Field(description="The minimum price of the product")
    price_max: float = Field(description="The maximum price of the product")
    inventory_status: str | None = Field(description="The inventory status of the product")
    page_crumbs: str | None = Field(description="The page crumbs of the product")
    sku: str | None = Field(description="The SKU of the product")
    link: str | None = Field(description="The link to the product")


class GroupedProduct(Product):
    category: Catagories = Field(description="The category of the product")

    class Config:
        use_enum_values = True