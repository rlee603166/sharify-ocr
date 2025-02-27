import os
import time
import orjson
from openai import OpenAI
from pydantic import BaseModel
from fastapi import FastAPI
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI()
# gpu = ocr_predictor(pretrained=True).cuda().half()
# cpu = ocr_predictor(pretrained=True)

def get_path(path=""):
    abs_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__)
            )
        ), 
        "divvy-backend/storage/receipts",
        path
    )

    return abs_path 

# def cpu_predict(filepath): 
#     path = get_path(filepath)
#     doc = DocumentFile.from_images(path)
#     result = cpu(doc)

#     return result.render()

# def gpu_predict(filepath): 
#     path = get_path(filepath)
#     doc = DocumentFile.from_images(path)
#     result = gpu(doc)

#     return result.render()

# def fetch_chat(extracted_text):
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "Extract receipt items and prices into structured JSON format. If the OCR extraction is unclear or incomplete, infer reasonable items based on context. Ensure that all extracted items are logically consistent, correlate with the receipt's cuisine or category, and make sense together."
#             },
#             {"role": "user", "content": f'''
#                 Extract the items and prices from the following receipt image and return them as JSON with this exact structure:
#                 {{
#                     "items": [
#                         {{
#                             "id": "<unique_id>",
#                             "name": "<item_name>",
#                             "price": <price>,
#                             "people": []
#                         }}
#                     ],
#                     "additional": {{
#                         "tax": <tax>,
#                         "tip": <tip>,
#                         "credit_charge": <credit_charge>
#                     }}
#                 }}
#                 Use an incrementing numeric ID for each item, starting from 1. Ensure the names and prices are accurate.

#                 Extracted Text:
#                 {extracted_text}
#             '''}
#         ]
#     )

#     data = completion.choices[0].message.content.strip()
#     receipt_data = orjson.loads(data.strip("```json").strip("```"))
#     return receipt_data
