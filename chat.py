import orjson
import time
import base64
import json
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ExifTags
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

load_dotenv()

client = OpenAI()

def encode_image(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return base64_str


def gpt_process(image_path):
    base64_img = encode_image(image_path)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {
                "role": "system",
                "content": "You are an assistant that extracts and formats receipt data into structured JSON for a food-sharing app. Ensure that all extracted items are logically consistent, correlate with the receipt's cuisine or category, and make sense together."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": '''
                        Extract the items and prices from the following receipt image and return them as JSON with this exact structure:
                        {
                            "items": [
                                {
                                    "id": "<unique_id>",
                                    "name": "<item_name>",
                                    "price": <price>,
                                    "people": []
                                }
                            ],
                            "additional": {
                                "tax": <tax>,
                                "tip": <tip>,
                                "credit_charge": <credit_charge>
                            }
                        }
                        Use an incrementing numeric ID for each item, starting from 1. Ensure the names and prices are accurate.
                        Return only valid JSON, without any additional text or formatting.
                    '''},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_img}", "detail": "auto"},
                    },
                ]
            }
        ],
        max_tokens=1000,
    )            

    stuff = completion.choices[0].message.content

    if stuff.startswith("```json"):
        stuff = stuff.strip("```json").strip("```")

    receipt_data = json.loads(stuff)

    return receipt_data 


