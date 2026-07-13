import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Cấu hình API Key
# Đảm bảo bạn đã cài đặt biến môi trường GEMINI_API_KEY trên Render Dashboard
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)



# Thử dùng id model này
model = genai.GenerativeModel('gemini-3.1-flash-lite')
class CodeSubmission(BaseModel):
    student_name: str
    code_content: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # File index.html phải nằm cùng cấp với main.py trên Github
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
 
    return "<h1>Lỗi: Không tìm thấy file index.html</h1>"


from fastapi.responses import FileResponse


@app.post("/submit")
async def submit_code(data: CodeSubmission):
    try:
        prompt = f"Sinh viên: {data.student_name}. Hãy chấm điểm và nhận xét code sau đây:\n\n{data.code_content}"
        response = model.generate_content(prompt)
        return {"ai_feedback": response.text}
    except Exception as e:
        return {"ai_feedback": f"Lỗi hệ thống khi gọi AI: {str(e)}"}
