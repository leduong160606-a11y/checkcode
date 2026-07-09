from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import google.generativeai as genai

# 1. Cấu hình API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()
# Đảm bảo file index.html nằm cùng thư mục với main.py
templates = Jinja2Templates(directory=".")

class CodeSubmission(BaseModel):
    student_name: str
    code_content: str

# 2. Trang chủ
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 3. API chấm bài
@app.post("/submit")
async def submit_code(data: CodeSubmission):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Hãy đóng vai giáo viên chấm bài lập trình nghiêm túc.
        Học sinh: {data.student_name}
        Đoạn code cần chấm:
        {data.code_content}
        
        Hãy trả lời theo cấu trúc:
        1. Đánh giá: [Điểm số]/10.
        2. Nhận xét: Trực tiếp, ngắn gọn.
        3. Điểm cần cải thiện: Tối đa 2 ý.
        """
        response = model.generate_content(prompt)
        return {"ai_feedback": response.text}
    except Exception as e:
        return {"ai_feedback": f"Lỗi hệ thống: {str(e)}"}
    
    
