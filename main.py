import time
from pydantic import BaseModel
from fastapi import FastAPI
from chat import gpt_process
from utils import get_path
from database import update_receipt, ReceiptUpdate

app = FastAPI()

@app.get("/")
def health():
    return { "status": "healthy" }


class Receipt(BaseModel):
    path: str
    receipt_id: int

@app.post("/gpt")
def gpt(receipt: Receipt):
    full_path = get_path(receipt.path)
    result = gpt_process(full_path)
    update = ReceiptUpdate(
        processed_data=result,
        status="completed"
    )

    return update_receipt(receipt.receipt_id, update).data[0]

@app.post("/ocr")
def ocr(receipt: Receipt):
    gpu_result = gpu_predict(receipt.path)
    result = fetch_chat(gpu_result)
    update = ReceiptUpdate(
        processed_data=result,
        status="completed"
    )

    return update_receipt(receipt.receipt_id, update).data[0]

@app.get("/{path}")
def get_time(path: str):
    start = time.time()
    gpu_result = gpu_predict(path)
    end = time.time()

    cpu_start = time.time()
    cpu_result = cpu_predict(path)
    cpu_end = time.time()

    return { "gpu": end-start, "cpu": cpu_end-cpu_start}

if __file__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
