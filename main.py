from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import google.generativeai as genai

# Cấu hình API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class CodeSubmission(BaseModel):
    student_name: str
    code_content: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/submit")
async def submit_code(data: CodeSubmission):
    try:
        # Tự liệt kê và lấy model đầu tiên hỗ trợ generateContent
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = models[0] if models else 'gemini-1.5-flash'
        
        model = genai.GenerativeModel(model_name)
        # ... (phần còn lại giữ nguyên)
        prompt = f"Học sinh: {data.student_name}. Code: {data.code_content}. Hãy chấm điểm và nhận xét."
        response = model.generate_content(prompt)
        return {"ai_feedback": response.text}
    except Exception as e:
        return {"ai_feedback": f"Lỗi: {str(e)}"}
