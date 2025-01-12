from __future__ import annotations

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from smart_shopper.llm import llm
from smart_shopper.models import GroupedProduct


PRODUCT_PROMPT = (
            """
            You are a smart shopper who is looking for the best deals on products. You have a product that you want to generate a sentence for. 

            For example if the product is "Charmin Ultra Soft Bath Tissue, 2-Ply, 213 Sheets, 30 Rolls" and the discount is "Save $5.00"
            you will also be give other information about the store, maybe price, end date, and link.

            Do not infer any information that is not given.

            The following product is the one you will need to generate a sentence for:
            {input}

            {format_instructions}

            """
        )



parser = PydanticOutputParser(pydantic_object=GroupedProduct)

category_prompt = PromptTemplate(
    template=PRODUCT_PROMPT,
    input_variables=["input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},

)

category_chain = category_prompt | llm | parser
