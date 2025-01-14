from fastapi import FastAPI, Request
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# הגדרות CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# טוען את המודל
generator = pipeline("text-generation", model="gpt2")

# זיכרון שיחה
conversation_history = []

@app.post("/generate")
async def generate_text(request: Request):
    global conversation_history
    data = await request.json()
    prompt = data.get("prompt", "")

    # הוספת ההודעה החדשה להיסטוריה
    conversation_history.append(f"You: {prompt}")

    # שמירה על הודעות קודמות בגבול 5 הודעות אחרונות
    if len(conversation_history) > 5:
        conversation_history = conversation_history[-5:]

    # יצירת ההקשר לשיחה
    context = "\n".join(conversation_history) + "\nBot:"
    
    # הפעלת המודל
    response = generator(context, max_length=100)
    bot_reply = response[0]["generated_text"]

    # הוספת תשובת הבוט להיסטוריה
    conversation_history.append(f"Bot: {bot_reply}")

    return {"generated_text": bot_reply.strip()}
