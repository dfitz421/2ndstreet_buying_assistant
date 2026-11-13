# 2nd Street Buying Assistant

A small proof-of-concept project based on my experience working in secondhand clothing retail.

The goal is to simplify the process of identifying and entering higher-value clothing items into a store's buying system. Currently, buyers need to research products for pricing and manually enter details such as brand, item name, category, material, and color into the buying form.

This project explores using AI to identify products from model numbers or photos of clothing tags and automatically fill in that information. Buyers would then verify the details, manually enter sizing and pricing, and add the item to a mock buying estimate.

The application will also provide shortcuts to relevant searches on eBay, Grailed, Poshmark, and Google to help with resale research.

The purpose of this is to speed up the buying process and reduce tedious data entry into buying estimate forms without relying on AI for pricing purposes.

## Current buying Process:
  1. Buyer Receives item and identifies it visually to confirm if item is in acceptable condition.
  2. Buyer completes internal store manual checks for authenticity of specific item.
  3. Buyer researches specific item, either from tag codes or visual identification to find sold listings of item or similar from websites like eBay, Grailed, Poshmark, etc.
  4. Buyer decides on price and percentage payout based on condition and resale value.
  5. Buyer manually inputs single item form into estimate form software:
       Data Fields: Brand, general category (clothing, footwear, accessory, etc.), Specific Category (men's jacket, women's bottoms, Men's footwear, etc.), Type of item (leather jacket, jeans, etc.), material, color, pattern, size, price, payout
  6. Single item is added to estimate sheet

## Proposed updated buying process:
  1. Buyer Receives item and identifies it visually to confirm if item is in acceptable condition.
  2. Buyer completes internal store manual checks for authenticity of specific item.
  3. Buyer scans item with camera or inputs designer and product code on tag into system.
  4. System autofill all relevant single item form fields from list of available options and provides search links to relevant websites for pricing research.
  5. Buyer inputs size, price, and percentage payout based on condition and resale value.
  6. Single item is added to estimate sheet

## Tech Stack

- Python
- Streamlit
- Google Gemini API

## Project Scope

This is a personal proof of concept, not a replacement for or integration with 2nd STREET's current internal buying software. The focus is on AI-assisted product identification and reducing repetitive data entry, while leaving authentication and final buying decisions to the employee.
