from fastapi import FastAPI, Request
from agents.kairoscip.agent import KairoAgent

app = FastAPI()


@app.post("/webhook")
async def receive_webhook(request: Request):
    # Access the raw request body
    body = await request.body()
    # Or parse JSON if the webhook sends JSON
    # data = await request.json()

    # Implement your logic to process the webhook data
    print(f"Received webhook: {body.decode()}")

    

    return {"message": "Webhook received successfully!"}