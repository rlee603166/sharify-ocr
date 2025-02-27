import os
from typing import Dict, Any
from pydantic import BaseModel
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(DATABASE_URL, SUPABASE_KEY)

class ReceiptUpdate(BaseModel):
    user_id: int | None = None
    filepath: str | None = None
    status: str | None = None
    processed_data: Dict[str, Any] | None = None


def update_receipt(id: int, receipt: ReceiptUpdate):
    return supabase.table("receipts")\
            .update(receipt.model_dump(exclude_unset=True))\
            .eq("receipt_id", id)\
            .execute()
