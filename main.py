    import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CodeSubmission(BaseModel):
    student_name: str
    code_content: str

# Hàm tự tìm model xịn nhất đang khả dụng
def get_best_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/submit")
async def submit_code(data: CodeSubmission):
    model = get_best_model()
    if not model:
        return {"ai_feedback": "Lỗi: Không tìm thấy model AI nào khả dụng cho API Key này."}
    
    try:
        prompt = f"Sinh viên: {data.student_name}. Chấm điểm code Python: {data.code_content}"
        response = model.generate_content(prompt)
        return {"ai_feedback": response.text}
    except Exception as e:
        return {"ai_feedback": f"Lỗi hệ thống: {str(e)}"}
