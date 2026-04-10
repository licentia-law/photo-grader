# Photo Color Grading Tool — CLAUDE.md

## 프로젝트 개요
레퍼런스 사진(A)의 색감·무드를 분석하고, 보정 대상 사진(B)에 동일한 분위기를 자동 적용하는 웹 앱.
상세 기획서: `docs/Plan.md`

## 기술 스택
| 영역 | 기술 |
|---|---|
| 백엔드 | Python FastAPI + scikit-image + Pillow + NumPy + OpenCV |
| 프론트엔드 | React + Vite (JSX) + Tailwind CSS v4 + Axios + Recharts + img-comparison-slider |
| 핵심 알고리즘 | `skimage.exposure.match_histograms` |

## 폴더 구조
```
photo-grader/
├── backend/
│   ├── .venv/                  # Python 가상환경 (Git 제외)
│   ├── main.py                 # FastAPI 앱 진입점 + CORS 설정
│   ├── routers/
│   │   ├── analyze.py          # POST /api/analyze
│   │   └── correct.py          # POST /api/correct
│   ├── services/
│   │   ├── analyzer.py         # 밝기/색온도/채도 분석 로직
│   │   └── corrector.py        # histogram matching 로직
│   ├── utils/
│   │   └── image_utils.py      # 이미지 변환 유틸
│   └── requirements.txt
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
│   │   ├── App.jsx
│   │   └── index.css           # @import "tailwindcss" 포함
│   ├── vite.config.js          # Tailwind v4 플러그인 설정 포함
│   └── package.json
├── docs/
│   └── Plan.md
├── CLAUDE.md                   # 이 파일
├── current_phase.txt
├── session_notes.txt
└── session_context.sh
```

## 환경 설정 & 실행 방법

### 백엔드 (Python)
```bash
# Windows
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --port 8000

# macOS/Linux
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 프론트엔드 (Node.js)
```bash
cd frontend
npm run dev
# → http://localhost:5173
```

## API 명세
| 메서드 | 경로 | 설명 |
|---|---|---|
| POST | `/api/analyze` | 사진 A 분석 (밝기/색온도/채도/히스토그램/무드) |
| POST | `/api/correct` | 사진 A+B로 보정 이미지 반환 (strength: 0.0~1.0) |

- CORS: React 개발 서버 포트 5173 허용 필수
- 고해상도 처리: 백엔드에서 최대 해상도 제한 처리 필요

## 핵심 알고리즘
```python
from skimage.exposure import match_histograms
matched = match_histograms(image_b, image_a, channel_axis=-1)
strength = 0.75
result = (matched * strength + image_b * (1 - strength)).astype(np.uint8)
```

## 개발 Phase
| Phase | 목표 | 상태 |
|---|---|---|
| Phase 1 | 백엔드 핵심 기능 (FastAPI + 분석/보정 API) | 준비 중 |
| Phase 2 | 프론트엔드 기본 UI + API 연동 | 대기 |
| Phase 3 | 분석 시각화 (히스토그램 차트, 수치 카드, 무드) | 대기 |
| Phase 4 | 비교 슬라이더 + 보정 강도 실시간 조절 | 대기 |
| Phase 5 | 다운로드, 에러 처리, UI 마무리 | 대기 |

## 주의사항
- `react-compare-image`는 React 18/19 호환 이슈 → `img-comparison-slider` 사용
- Tailwind CSS v4 사용 중 (설정 방식이 v3과 다름 — `tailwind.config.js` 불필요, `@import "tailwindcss"` 사용)
- Windows 환경 기준 개발, macOS도 동작 보장 필요
- Python 환경: venv (pyenv/conda 없음), 가상환경 위치: `backend/.venv`
