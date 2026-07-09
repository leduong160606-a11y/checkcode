from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
genai.configure(api_key="AQ.Ab8RN6I-7PFX_7lSPZ8ZdRb5TjgjGBlNIQcW1zsnZik8kvAIaw")
#models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
#print(models)
app = FastAPI()
templates = Jinja2Templates(directory=".")
class CodeSubmission(BaseModel):
    student_name: str
    code_content: str
@app.get("/")
def read_root(request: Request):
    return  templates.TemplateResponse(request,"index.html", {"request":request})
@app.post("/submit")
async def submit_code(data: CodeSubmission):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
Hãy đóng vai một giáo viên chấm điểm lập trình nghiêm túc. 
Dựa trên đoạn code sau: {data.code_content}
Hãy trả lời theo cấu trúc sau:
1. Đánh giá: [Điểm số] (trên thang điểm 10).
2. Nhận xét: Trả lời ngắn gọn, trực tiếp vào vấn đề.
3. Điểm cần cải thiện: Nêu tối đa 2 ý chính quan trọng nhất.
"""
    response = model.generate_content(prompt)
    return {
    "message": " Đã nhận bài và AI đã chấm xong!",
    "ai_feedback": response.text
    }
    import uvicorn
    uvicorn.run("main:app",reload=True)
    
    
