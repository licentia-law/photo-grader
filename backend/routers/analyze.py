from fastapi import APIRouter, File, UploadFile, HTTPException
from utils.image_utils import bytes_to_array
from services.analyzer import analyze_image

router = APIRouter()


@router.post("/analyze")
async def analyze(image_a: UploadFile = File(...)):
    if not image_a.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    data = await image_a.read()
    try:
        image = bytes_to_array(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 처리 오류: {e}")

    return analyze_image(image)
