from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from datetime import date

app = FastAPI()

# In-memory database to store posted records
data_store = []

# Step 1: Define the schema using Pydantic
class DealerData(BaseModel):
    beat_no: int
    beat_plane_no: int
    beat_name: str
    dealer_id: int
    dealer_name: str
    date: str
    days: str
    material: str
    purchase_quantity: float
    total_order_count_per_day: int

# Step 2: POST API to collect data
@app.post("/submit-data")
async def submit_data(item: DealerData):
    data_store.append(item)
    return {"message": "Data submitted successfully", "data": item}

# Step 3: GET API to fetch all submitted data
@app.get("/get-data", response_model=List[DealerData])
async def get_data():
    return data_store

# DELETE endpoint to delete data by dealer_id
@app.delete("/delete-data/{dealer_id}")
def delete_data(dealer_id: int):
    for i, record in enumerate(db):
        if record["dealer_id"] == dealer_id:
            deleted = db.pop(i)
            return {"message": f"Record with dealer_id {dealer_id} deleted.", "deleted": deleted}
    raise HTTPException(status_code=404, detail=f"No record found with dealer_id {dealer_id}")