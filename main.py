from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, JSONData
from fastapi import HTTPException
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📥 POST JSON
@app.post("/collect-json/")
async def collect_json(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    # Save the entire JSON object
    json_entry = JSONData(raw=data)
    db.add(json_entry)
    db.commit()

    return {"status": "success", "message": "JSON stored"}

# 📤 GET JSON
@app.get("/get-json/")
def get_json(db: Session = Depends(get_db)):
    all_data = db.query(JSONData).all()
    return [{"id": item.id, "raw": item.raw} for item in all_data]

@app.delete("/delete-json/{item_id}")
def delete_json(item_id: int, db: Session = Depends(get_db)):
    item = db.query(JSONData).filter(JSONData.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"status": "success", "message": f"Item {item_id} deleted"}
