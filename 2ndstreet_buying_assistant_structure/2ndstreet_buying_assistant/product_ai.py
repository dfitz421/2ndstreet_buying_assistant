
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
    Identify this secondhand fashion item using the information and/or photos provided.
    Use Google Search when needed to research the exact product.

    Designer/brand: {designer_hint}
    Product code: {product_code}

    Allowed dropdown choices: {json.dumps(options or {})}

    Return the most accurate product information you can find.
    For dropdown fields, use ONLY an exact choice from the allowed list, or leave it blank.
    Do not guess the model, season, material, or other details.
    A number on a care tag may not be a product code.
    If something cannot be verified, leave it blank and explain in notes.
    Do not authenticate the item or recommend selling/buying prices.
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
