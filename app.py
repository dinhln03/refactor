from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from backend.search import VectorSearch
# main.py or app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/images", StaticFiles(directory="/home/dinhln/Desktop/MLOPS/AIC/keyFrameLarge"), name="images")
# Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the VectorSearch instance
bin_file_v2 = '/home/dinhln/Desktop/MLOPS/AIC/refactor/data/faiss_clipv2_cosine.bin'
json_path = '/home/dinhln/Desktop/MLOPS/AIC/refactor/data/image_paths_new.json'
media_dir= "/home/dinhln/Desktop/MLOPS/AIC/refactor/data/media-info"
vector_search = VectorSearch(bin_clipv2_file=bin_file_v2, json_path=json_path, media_dir=media_dir)

# Define the request model
class SearchRequest(BaseModel):
    text: str
    k: int
    model_type: str
    index: Optional[List[int]] = None

# Define the response model
class SearchResponse(BaseModel):
    scores: List[float]
    idx_image: List[int]
    infos_query: List[dict]
    image_paths: List[str]
    ranked_image_paths: List[str]
    meta_data: dict

@app.post("/text_search", response_model=SearchResponse)
def search(request: SearchRequest):
    scores, idx_image, infos_query, image_paths, ranked_image_paths, meta_data = vector_search.text_search(
        text=request.text,
        index=request.index,
        k=request.k,
        model_type=request.model_type
    )
    return SearchResponse(
        scores=scores.tolist(),
        idx_image=idx_image.tolist(),
        infos_query=infos_query,
        image_paths=image_paths,
        ranked_image_paths=ranked_image_paths,
        meta_data=meta_data

    )
# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)