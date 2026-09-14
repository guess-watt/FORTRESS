from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.feature_extractor import extract_features
from backend.app.move_analyzer import analyze_game
from backend.app.pgn_parser import parse_pgn
from backend.app.schemas import AnalyzeRequest, AnalyzeResponse
from ml.models.anomaly_model import AnomalyModel, prepare_features


MODEL_PATH = "ml/models/anomaly_model.joblib"


app = FastAPI(
    title="FORTRESS API",
    description="Chess anomaly detection API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:5174","http://127.0.0.1:5174",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "FORTRESS API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        parsed_game = parse_pgn(request.pgn)

        analysis_results = analyze_game(
            parsed_game["moves"]
        )

        features = extract_features(
            analysis_results
        )

        model = AnomalyModel.load(
            MODEL_PATH
        )

        feature_vector = prepare_features(
            features
        )

        prediction = model.predict(
            feature_vector
        )

        isolation_score = model.anomaly_score(
            feature_vector
        )

        label = (
            "ANOMALOUS"
            if prediction == -1
            else "NORMAL"
        )

        return {
            "anomaly_label": label,
            "isolation_score": isolation_score,
            "features": features,
        }

    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc