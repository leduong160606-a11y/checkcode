import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

# 1. Khởi tạo ứng dụng
app = FastAPI()

# 2. Cấu hình API Key từ Render (Environment Variable)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CodeSubmission(BaseModel):
    student_name: str
    code_content: str

# 3. Route chính để hiển thị trang web
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 4. Route xử lý nộp bài
@app.post("/submit")
async def submit_code(data: CodeSubmission):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Sinh viên: {data.student_name}. Hãy đóng vai giảng viên, chấm điểm và nhận xét đoạn code sau một cách nghiêm túc: {data.code_content}"
        response = model.generate_content(prompt)
        return {"ai_feedback": response.text}
    except Exception as e:
        return {"ai_feedback": f"Lỗi hệ thống: {str(e)}"}
