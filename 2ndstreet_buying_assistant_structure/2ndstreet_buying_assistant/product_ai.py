
import base64
import json

from google import genai
from pydantic import BaseModel


# feilds in buying form
class ProductDetails(BaseModel):
    designer: str = ""
    item_name: str = ""
    product_code: str = ""
    season: str = ""
    general_category: str = ""
    specific_category: str = ""
    item_type: str = ""
    material: str = ""
    color: str = ""
    pattern: str = ""
    notes: str = ""


def identify_product(api_key, designer_hint="", product_code="", photos=None, options=None):
    client = genai.Client(api_key=api_key)

   prompt = f"""
    Identify this secondhand clothing item using the provided photos
    and any available product information.

    Designer/brand: {designer_hint}
    Product code: {product_code}

    If a product code is provided, use it to research the exact item.

    If no product code is provided, identify the item using the photos.
    Examine the brand label, care tags, garment design, and distinctive
    details. Use Google Search to help identify the item when possible.

    Extract the brand, item name, category, material, color, pattern,
    and season when supported by the available information.

    Allowed dropdown choices: {json.dumps(options or {})}

    Use only values from the allowed dropdown lists.
    If the exact item cannot be identified, fill in the information
    that is supported and leave uncertain fields blank.

    Explain any uncertainty in the notes field.
    Do not authenticate items or determine buying/selling prices.
    """
    inputs = [{"type": "text", "text": prompt}]

    # include all photos
    for photo in photos or []:
        inputs.append({
            "type": "image",
            "data": base64.b64encode(photo.getvalue()).decode("utf-8"),
            "mime_type": photo.type,
        })

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=inputs,
        tools=[{"type": "google_search"}],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ProductDetails.model_json_schema(),
        },
    )

    if not response.output_text:
        raise ValueError("Gemini returned no product information.")

    return ProductDetails.model_validate_json(response.output_text).model_dump()
