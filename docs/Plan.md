# 📸 사진 보정 앱 — 개발 기획서 v2.0
**Reference-based Photo Color Grading Tool**

> 기준 사진 A의 밝기·색감·무드를 분석하고,  
> 보정할 사진 B에 동일한 분위기를 자동으로 적용하는 웹 기반 도구

`Python` `FastAPI` `scikit-image` `React` `Vite` `JavaScript/JSX` `Tailwind CSS`

---

## 1. 프로젝트 개요

### 💡 만들고자 하는 것

사진 A (레퍼런스)를 입력하면 밝기, 색감, 무드를 자동 분석하고,  
사진 B (보정 대상)를 입력하면 사진 A의 분위기로 자동 보정해주는 웹 도구.

### 사용 시나리오

1. **사진 A 업로드** — 원하는 색감/무드의 레퍼런스 사진 (예: 따뜻한 필름 감성)
2. **분석 결과 확인** — 밝기, 색온도, 채도, 무드 키워드 자동 추출
3. **사진 B 업로드** — 같은 분위기로 바꾸고 싶은 내 사진
4. **보정 결과 확인** — 전/후 슬라이더로 비교
5. **다운로드** — 보정된 사진 저장

### 핵심 가치

| 기존 방식 | 이 앱 |
|---|---|
| Lightroom에서 수동으로 수치 조정 | 레퍼런스 사진 하나로 자동 적용 |
| 색감 맞추는 데 수십 분 소요 | 수초 내 자동 보정 |
| 전문 지식 필요 | 사진 두 장만 있으면 OK |

---

## 2. 개발 환경 확정 사항

| 항목 | 결정 | 비고 |
|---|---|---|
| **OS** | Windows / macOS 크로스 환경 | 두 환경 모두 동작 보장 |
| **프론트엔드 언어** | JavaScript (JSX) | TypeScript는 러닝커브 있어 제외 |
| **Python 환경 관리** | venv | pyenv/conda 없이 심플하게 |
| **목적** | 개인 사용 + 포트폴리오 | |
| **배포** | 로컬 우선, 추후 확장 | |

### OS별 명령어 차이 참고

| 작업 | macOS / Linux | Windows |
|---|---|---|
| venv 생성 | `python3 -m venv venv` | `python -m venv venv` |
| venv 활성화 | `source venv/bin/activate` | `venv\Scripts\activate` |
| 서버 실행 | `uvicorn main:app --reload` | 동일 |
| 프론트 실행 | `npm run dev` | 동일 |

---

## 3. 핵심 기능

### 📊 사진 A 분석 (레퍼런스)

- **밝기 분석** — 평균 휘도, 밝은 영역/어두운 영역 비율
- **색온도 분석** — 따뜻함(Warm) / 차가움(Cool) 수치
- **채도 분석** — 선명한(Vivid) / 차분한(Muted) 수치
- **색조 분포** — RGB 히스토그램 시각화
- **무드 키워드** — 예: "따뜻한 필름", "차가운 모노톤", "생동감 있는 여름" 등

### 🎨 사진 B 보정

- **Histogram Matching** — 사진 A의 색상 분포를 B에 적용 (Phase 1 핵심)
- **강도 조절** — 보정 강도 슬라이더 (0~100%)
- **채널별 적용** — R/G/B 각 채널 독립 조정 가능
- **미리보기** — 실시간 보정 전/후 비교

### 🖼️ 결과 화면

- **슬라이더 비교** — 좌우로 드래그하여 보정 전/후 비교
- **수치 비교** — A 분석값 vs B 보정 후 수치 나란히 표시
- **다운로드** — JPG / PNG 선택 다운로드

---

## 4. 화면 구성 (UI)

### 주요 화면 목록

| 화면 | 설명 |
|---|---|
| 🏠 메인 | 사진 A/B 업로드 영역, 앱 설명 |
| 📊 분석 결과 | 사진 A의 밝기/색감/무드 분석 카드 |
| 🎨 보정 화면 | 보정 강도 조절, 실시간 미리보기 |
| 🖼️ 결과 비교 | 슬라이더 비교, 수치 비교, 다운로드 |

### 메인 레이아웃

```
┌─────────────────────────────────────────────────────┐
│  📸 Photo Color Grading Tool                        │
├─────────────────────┬───────────────────────────────┤
│                     │                               │
│  📷 사진 A 업로드   │   📷 사진 B 업로드            │
│  (레퍼런스)         │   (보정 대상)                 │
│                     │                               │
│  [이미지 드롭 영역] │   [이미지 드롭 영역]          │
│                     │                               │
├─────────────────────┴───────────────────────────────┤
│  📊 사진 A 분석 결과                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ 밝기     │ │ 색온도   │ │ 채도     │            │
│  │ 72/100   │ │ Warm 65% │ │ Vivid 80%│            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  무드: "따뜻한 골든아워 필름 감성"                  │
├─────────────────────────────────────────────────────┤
│  🎨 보정 강도: ────────●──── 75%   [보정 시작]     │
└─────────────────────────────────────────────────────┘
```

### 결과 비교 화면

```
┌─────────────────────────────────────────────────────┐
│  보정 전 ◄────────────────►  보정 후               │
│  ┌──────────────────────────────────────────────┐  │
│  │                    │                         │  │
│  │    원본 사진 B      │     보정된 사진 B       │  │
│  │                    │                         │  │
│  └──────────────────────────────────────────────┘  │
│  (슬라이더로 좌우 드래그)                           │
├─────────────────────────────────────────────────────┤
│  [⬇ JPG 다운로드]  [⬇ PNG 다운로드]  [↺ 다시하기] │
└─────────────────────────────────────────────────────┘
```

---

## 5. 기술 스택

### 전체 아키텍처

```
[브라우저 - React]
       ↕ HTTP (multipart/form-data)
[백엔드 - FastAPI (Python)]
       ↕
[이미지 처리 - scikit-image / Pillow / NumPy]
```

### 기술 스택 상세

| 분류 | 기술 | 역할 |
|---|---|---|
| **백엔드** | Python 3.11+ | 서버 언어 |
| **웹 프레임워크** | FastAPI | REST API 서버, 이미지 수신/반환 |
| **핵심 알고리즘** | scikit-image | `match_histograms` — 히스토그램 매칭 |
| **이미지 처리** | Pillow (PIL) | 이미지 열기/저장/변환 |
| **수치 계산** | NumPy | 색상 통계 계산 |
| **프론트엔드** | React + Vite **(JavaScript/JSX)** | UI 프레임워크 |
| **스타일링** | Tailwind CSS | UI 스타일 |
| **HTTP 통신** | Axios | API 호출 |
| **비교 슬라이더** | react-compare-image | 전/후 비교 UI |
| **차트** | Recharts | 히스토그램 시각화 |

> ⚠️ **`react-compare-image` 호환성 주의**  
> React 18/19 환경에서 간혹 호환성 이슈 발생. 문제 시 `react-img-comparison-slider`로 대체.

### 핵심 알고리즘 (scikit-image)

```python
from skimage.exposure import match_histograms
import numpy as np

# 사진 A (레퍼런스), 사진 B (보정 대상)
matched = match_histograms(image_b, image_a, channel_axis=-1)

# 강도 조절 (0~1)
strength = 0.75
result = (matched * strength + image_b * (1 - strength)).astype(np.uint8)
```

단 **세 줄**로 핵심 기능 구현 가능.

---

## 6. API 설계

> 💡 **CORS 필수 설정** — React 개발 서버(5173 포트) ↔ FastAPI(8000 포트) 간 통신이므로 백엔드에 CORS 미들웨어 설정이 반드시 필요.

### POST `/api/analyze`
사진 A를 분석하여 색감 정보 반환

**Request:**
```
multipart/form-data
- image_a: File (JPG/PNG)
```

**Response:**
```json
{
  "brightness": 72,
  "color_temp": { "warm": 65, "cool": 35 },
  "saturation": 80,
  "mood": "따뜻한 골든아워 필름 감성",
  "histogram": {
    "r": [...],
    "g": [...],
    "b": [...]
  }
}
```

### POST `/api/correct`
사진 B를 사진 A 스타일로 보정

**Request:**
```
multipart/form-data
- image_a: File (레퍼런스)
- image_b: File (보정 대상)
- strength: float (0.0 ~ 1.0, default: 0.75)
```

**Response:**
```
image/jpeg (보정된 이미지 바이너리)
```

---

## 7. 색감 분석 로직

### 밝기 (Brightness)
```python
# LAB 색공간의 L 채널 평균
lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
brightness = lab[:, :, 0].mean() / 255 * 100  # 0~100
```

### 색온도 (Color Temperature)
```python
# R 채널 평균 vs B 채널 평균 비율
r_mean = image[:, :, 0].mean()
b_mean = image[:, :, 2].mean()
warm_ratio = r_mean / (r_mean + b_mean) * 100  # 50 이상이면 Warm
```

### 채도 (Saturation)
```python
# HSV 색공간의 S 채널 평균
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
saturation = hsv[:, :, 1].mean() / 255 * 100  # 0~100
```

### 무드 키워드 분류

| 조건 | 무드 키워드 |
|---|---|
| 밝기 높음 + Warm + 채도 높음 | ☀️ 따뜻한 골든아워 |
| 밝기 낮음 + Cool + 채도 낮음 | 🌙 다크 무드 |
| 밝기 중간 + Cool + 채도 낮음 | 🌫️ 차가운 필름 |
| 밝기 높음 + Cool + 채도 높음 | 💎 선명한 블루톤 |
| 밝기 중간 + Warm + 채도 낮음 | 🍂 빈티지 필름 |
| 밝기 낮음 + Warm + 채도 중간 | 🕯️ 따뜻한 저조도 |

---

## 8. 프로젝트 폴더 구조

```
photo-correction/
├── backend/
│   ├── main.py                   # FastAPI 앱 진입점 + CORS 설정
│   ├── routers/
│   │   ├── analyze.py            # 사진 분석 API
│   │   └── correct.py            # 사진 보정 API
│   ├── services/
│   │   ├── analyzer.py           # 밝기/색온도/채도 분석 로직
│   │   └── corrector.py          # histogram matching 로직
│   ├── utils/
│   │   └── image_utils.py        # 이미지 변환 유틸
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx
│   │   │   ├── AnalysisCard.jsx
│   │   │   ├── HistogramChart.jsx
│   │   │   ├── StrengthSlider.jsx
│   │   │   └── CompareSlider.jsx
│   │   ├── pages/
│   │   │   ├── MainPage.jsx
│   │   │   └── ResultPage.jsx
│   │   ├── api/
│   │   │   └── photoApi.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 9. 환경 설정

### 백엔드 설치

**macOS**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn scikit-image pillow numpy python-multipart opencv-python
uvicorn main:app --reload --port 8000
```

**Windows**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn scikit-image pillow numpy python-multipart opencv-python
uvicorn main:app --reload --port 8000
```

### 프론트엔드 설치 (공통)
```bash
cd frontend
npm create vite@latest . -- --template react
npm install
npm install tailwindcss axios react-compare-image recharts lucide-react
npm run dev
```

### requirements.txt
```
fastapi==0.115.0
uvicorn==0.30.0
scikit-image==0.24.0
pillow==10.4.0
numpy==1.26.0
python-multipart==0.0.12
opencv-python==4.10.0.84
```

---

## 10. 개발 계획 (Phase별)

| 단계 | 목표 | 주요 작업 |
|---|---|---|
| **Phase 1** | 백엔드 핵심 기능 | FastAPI 셋업 + CORS 설정, analyzer.py, corrector.py, API 엔드포인트 2개, curl 테스트 |
| **Phase 2** | 프론트엔드 기본 UI | React+Vite 셋업, 업로드 UI, API 연동, 결과 이미지 표시 |
| **Phase 3** | 분석 시각화 | 히스토그램 차트, 분석 수치 카드, 무드 키워드 |
| **Phase 4** | 비교 슬라이더 | 전/후 비교 슬라이더, 보정 강도 실시간 조절 |
| **Phase 5** | 마무리 | 다운로드 기능, 에러 처리, UI 다듬기, 테스트 |

> 💡 **개발 팁**: Phase 1 완료 후 반드시 curl로 두 API를 직접 테스트한 뒤 Phase 2로 넘어갈 것.  
> 백엔드가 안정적으로 동작하는 걸 확인하고 UI 작업에 들어가야 디버깅이 훨씬 편합니다.

---

## 11. Claude Code 시작 프롬프트

새 대화창에서 아래 내용을 그대로 붙여넣기:

```
Python FastAPI + React Vite로 사진 보정 웹앱을 만들어줘.

기능:
- 사진 A(레퍼런스)를 업로드하면 밝기/색온도/채도/무드를 분석
- 사진 B(보정 대상)를 업로드하면 사진 A의 색감으로 자동 보정
- 보정 강도 슬라이더 (0~100%)
- 전/후 비교 슬라이더
- 보정 결과 JPG/PNG 다운로드

기술 스택:
- 백엔드: Python FastAPI, scikit-image (match_histograms), Pillow, NumPy, OpenCV
- 프론트엔드: React + Vite (JavaScript/JSX), Tailwind CSS, Axios, react-compare-image, Recharts

환경 조건:
- Windows / macOS 모두에서 동작해야 함 (크로스 플랫폼)
- Python은 venv로 관리 (pyenv/conda 없음)
- 경로 구분자, 스크립트 실행 명령어 등 OS 차이를 주석 또는 README에 명시해줘

API:
- POST /api/analyze — 사진 A 분석 (밝기/색온도/채도/히스토그램/무드 반환)
- POST /api/correct — 사진 A + B 입력, strength(0~1) 파라미터, 보정 이미지 반환
- CORS 설정 포함 (React 개발 서버 5173 포트 허용)

이미지 처리 주의사항:
- 고해상도 사진 업로드 시 처리 속도 저하 방지를 위해 백엔드에서 최대 해상도 제한 처리 추가

Phase 1부터 시작:
백엔드 FastAPI 셋업, 이미지 분석 서비스(analyzer.py), 히스토그램 매칭 서비스(corrector.py), 두 API 엔드포인트 구현부터 해줘.
README.md에 Windows / macOS 각각의 실행 방법도 함께 작성해줘.
```

---

## 12. 향후 확장 계획

| 기능 | 설명 | 난이도 |
|---|---|---|
| **AI 무드 분석** | Claude API로 무드 설명 고도화 | 쉬움 |
| **LUT 생성** | 보정값을 LUT 파일로 내보내기 (Lightroom 호환) | 중간 |
| **배치 처리** | 여러 장의 사진 B를 한 번에 보정 | 중간 |
| **히스토리** | 최근 사용한 레퍼런스 저장 | 쉬움 |
| **AI Color Transfer** | 딥러닝 기반 색감 전달 알고리즘 적용 | 어려움 |
| **영상 지원** | 동영상에도 색감 적용 | 어려움 |

---

*개발 기획서 v2.0 | 2026-04-09*
