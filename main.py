import os
import signal
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

app = FastAPI()

# --- Pipeline Automation Route ---
def perform_shutdown():
    time.sleep(1) # Wait 1 second to allow the HTTP response to send
    # SIGINT acts like a virtual Ctrl+C, allowing a graceful shutdown to save coverage
    os.kill(os.getpid(), signal.SIGINT)

@app.post("/shutdown")
def shutdown_server(background_tasks: BackgroundTasks):
    """Triggers a background task to cleanly shut down the server."""
    background_tasks.add_task(perform_shutdown)
    return {"status": "shutting down cleanly"}
# ---------------------------------

class CartItem(BaseModel):
    item_id: str
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")
    price: float

@app.post("/cart/add")
async def add_to_cart(item: CartItem):
    # Boundary Limit Rule: Cannot buy more than 50 of the same item
    if item.quantity > 50:
        raise HTTPException(status_code=400, detail="Quantity exceeds maximum allowed limit of 50.")
    
    # Calculate totals with a simulated 10% tax
    subtotal = item.quantity * item.price
    tax = subtotal * 0.10
    total_price = subtotal + tax
    
    return {
        "status": "success",
        "item": item.item_id,
        "total_price": total_price
    }