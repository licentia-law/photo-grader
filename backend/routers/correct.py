from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import Response
from utils.image_utils import bytes_to_array, array_to_bytes
from services.corrector import correct_image

router = APIRouter()


@router.post("/correct")
async def correct(
    image_a: UploadFile = File(...),
    image_b: UploadFile = File(...),
    strength: float = Form(0.75),
):
    for f in (image_a, image_b):
        if not f.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    try:
        arr_a = bytes_to_array(await image_a.read())
        arr_b = bytes_to_array(await image_b.read())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 처리 오류: {e}")

    result = correct_image(arr_b, arr_a, strength)
    output = array_to_bytes(result, format="JPEG")
    return Response(content=output, media_type="image/jpeg")
