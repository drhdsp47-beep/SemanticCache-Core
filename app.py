from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="SemanticCache-Core: Smart AI Cache")

# ذاكرة تخزين مؤقتة وهمية داخل النظام لتخزين الإجابات السابقة مجاناً
cache_database = [
    {
        "keys": ["how to reset password", "reset my password", "forgot password", "تغيير كلمة المرور", "نسيت الباسورد"],
        "response": "To reset your password, click on 'Forgot Password' at the login page and follow the email instructions."
    },
    {
        "keys": ["shipping time", "delivery duration", "when will my order arrive", "وقت الشحن", "متى يصل الطلب"],
        "response": "Standard shipping takes 3-5 business days. International shipping takes 7-14 business days."
    }
]

class CacheRequest(BaseModel):
    user_query: str

def find_cached_response(query: str):
    query_words = set(query.lower().split())
    
    for item in cache_database:
        for key in item["keys"]:
            key_words = set(key.lower().split())
            # حساب نسبة الكلمات المشتركة بين السؤالين (خوارزمية تشابه دلالي مبسطة وسريعة)
            intersection = query_words.intersection(key_words)
            if len(intersection) >= 2 or (len(query_words) == 1 and query in key):
                return item["response"]
    return None

@app.post("/v1/cache")
async def check_cache(request: CacheRequest):
    cached_res = find_cached_response(request.user_query)
    
    if cached_res:
        # إذا كانت الإجابة موجودة، يتم إرجاعها فوراً وتوفير 100% من التكلفة
        return {
            "status": "HIT",
            "source": "Local Semantic Cache",
            "saved_cost": "100% Saved",
            "ai_response": cached_res
        }
    
    # إذا كان السؤال جديداً كلياً، يخبر النظام المطور بضرورة تمريره للذكاء الاصطناعي
    return {
        "status": "MISS",
        "source": "Forward to AI Model",
        "saved_cost": "$0.00 (New Query)",
        "message": "Query not found in cache. Forwarding to local or cloud LLM."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
