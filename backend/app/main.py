from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .astrology_engine import TharuMagaEngine
from .interpretation_engine import TharuMagaInterpretationEngine
from .dasha_interpretation_engine import TharuMagaDashaInterpretationEngine
from .yoga_detection_engine import TharuMagaYogaEngine
from .yoga_interpretation_engine import TharuMagaYogaInterpretationEngine


app = FastAPI(
    title="TharuMaga Astrology API",
    description="Astrology API powered by Swiss Ephemeris",
    version="1.0.0"
)


class BirthDetails(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    second: int = Field(0, ge=0, le=59)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str
    place: str = ""


@app.get("/")
def root():
    return {
        "app": "TharuMaga",
        "status": "online",
        "message": "TharuMaga Astrology API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "tharumaga-api"
    }


@app.post("/api/v1/chart")
def calculate_chart(data: BirthDetails):
    try:
        engine = TharuMagaEngine(
            day=data.day,
            month=data.month,
            year=data.year,
            hour=data.hour,
            minute=data.minute,
            second=data.second,
            latitude=data.latitude,
            longitude=data.longitude,
            timezone=data.timezone,
            place=data.place
        )

        result = engine.calculate()

        interpretation_engine = TharuMagaInterpretationEngine(result)
        interpretation = interpretation_engine.generate()
        result["interpretation"] = interpretation

        dasha_interpretation_engine = (
            TharuMagaDashaInterpretationEngine(result)
        )
        dasha_interpretation = (
            dasha_interpretation_engine.generate()
        )
        result["dasha_interpretation"] = dasha_interpretation

        # Yoga detection is kept separate from yoga interpretation.
        yoga_detection_engine = TharuMagaYogaEngine(result)
        yoga_detection = yoga_detection_engine.generate()
        result["yogas"] = yoga_detection

        yoga_interpretation_engine = (
            TharuMagaYogaInterpretationEngine(yoga_detection)
        )
        yoga_interpretation = yoga_interpretation_engine.generate()
        result["yoga_interpretation"] = yoga_interpretation

        return {
            "success": True,
            "data": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
