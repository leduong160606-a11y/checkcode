@app.get("/list-models")
async def list_models():
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return {"models": models}
