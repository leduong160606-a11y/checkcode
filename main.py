from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import google.generativeai as genai

# Cấu hình API Key từ Render (không để key cứng trong code)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()
templates = Jinja2Templates(directory=".")

class CodeSubmission(BaseModel):
    student_name: str
    code_content: str

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("name=index.html",context= {"request": request})

@app.post("/submit")
async def submit_code(data: CodeSubmission):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
Hãy đóng vai một giáo viên chấm điểm lập trình.
Dựa trên đoạn code sau của học sinh {data.student_name}: {data.code_content}
Hãy trả lời theo cấu trúc sau:
1. Đánh giá: [Điểm số] trên 10.
2. Nhận xét: Ngắn gọn.
3. Điểm cần cải thiện: Tối đa 2 ý.
"""
    response = model.generate_content(prompt)
    return {
        "message": "Đã nhận bài và AI đã chấm xong!",
        "ai_feedback": response.text
    }
    
    
