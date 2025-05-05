from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_processor import YouTubeRAGProcessor
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_id: str

class QuestionRequest(BaseModel):
    video_id: str
    question: str

processor = YouTubeRAGProcessor()
video_stores = {}  

@app.post("/process_video")
async def process_video(request: VideoRequest):
    try:
        retriever = processor.process_video(request.video_id)
        video_stores[request.video_id] = retriever
        return {"status": "success", "video_id": request.video_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ask_question")
async def ask_question(request: QuestionRequest):
    if request.video_id not in video_stores:
        raise HTTPException(status_code=404, detail="Video not processed")
    
    try:
        answer = processor.ask_question(
            video_stores[request.video_id],
            request.question
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)