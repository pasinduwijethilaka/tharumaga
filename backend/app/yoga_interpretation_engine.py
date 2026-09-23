"""
TharuMaga Yoga Interpretation Engine
------------------------------------
Interpretation layer for structurally detected yogas.

This module does NOT calculate astronomy and does NOT decide whether a
classical yoga is valid. It consumes the output of Yoga Detection Engine
v1.1 and converts detected structural combinations into user-friendly
interpretation cards.

Design:
    Yoga Detection Engine
            ↓
    Yoga Interpretation Engine
            ↓
    structured interpretation

The wording intentionally distinguishes structural detection from
strength/manifestation. A detected yoga is not automatically interpreted
as a guaranteed life outcome.
"""

from __future__ import annotations

from typing import Any


class TharuMagaYogaInterpretationEngine:
    """Generate structured interpretations for detected yogas."""

    YOGA_LIBRARY: dict[str, dict[str, Any]] = {
        "gaja_kesari": {
            "title": "Gaja Kesari Yoga",
            "category": "Wisdom & Influence",
            "summary": (
                "A traditional combination involving the Moon and Jupiter. "
                "When structurally present, it is traditionally associated "
                "with learning, judgment, confidence and social influence."
            ),
            "themes": [
                "learning and knowledge",
                "judgment and decision-making",
                "confidence",
                "social recognition",
            ],
            "life_areas": [
                "education",
                "communication",
                "relationships with mentors",
                "public or social life",
            ],
            "caution": (
                "The presence of the combination alone does not determine "
                "how strongly these themes manifest. Planetary strength, "
                "condition and the wider chart should be assessed separately."
            ),
        },
        "budha_aditya": {
            "title": "Budha Aditya Yoga",
            "category": "Intellect & Communication",
            "summary": (
                "A Sun-Mercury combination traditionally associated with "
                "intellect, communication, analytical thinking and the "
                "ability to express ideas."
            ),
            "themes": [
                "intellectual activity",
                "communication",
                "analysis",
                "learning",
                "self-expression",
            ],
            "life_areas": [
                "education",
                "writing and speaking",
                "business or analytical work",
                "planning and problem-solving",
            ],
            "caution": (
                "Sun-Mercury conjunction by itself does not guarantee "
                "academic or professional success. Strength and condition "
                "must be evaluated separately."
            ),
        },
        "dharma_karmadhipati": {
            "title": "Dharma Karmadhipati Yoga",
            "category": "Purpose & Career",
            "summary": (
                "A relationship between the 9th and 10th house lords. "
                "Traditionally this connects themes of dharma, guidance, "
                "fortune and higher purpose with career, responsibility "
                "and action."
            ),
            "themes": [
                "purpose",
                "career direction",
                "responsibility",
                "guidance",
                "achievement through action",
            ],
            "life_areas": [
                "career",
                "professional responsibility",
                "leadership",
                "higher learning and guidance",
            ],
            "caution": (
                "The yoga describes a structural relationship in the chart; "
                "it should not be presented as a guaranteed career outcome."
            ),
        },
        "raja_yoga": {
            "title": "Raja Yoga",
            "category": "Achievement & Responsibility",
            "summary": (
                "A qualifying relationship between Kendra and Trikona lords. "
                "In traditional Jyotisha this links areas connected with "
                "action, stability, purpose and opportunity."
            ),
            "themes": [
                "achievement",
                "responsibility",
                "leadership",
                "opportunity",
                "constructive action",
            ],
            "life_areas": [
                "career",
                "leadership",
                "public responsibilities",
                "major life goals",
            ],
            "caution": (
                "A detected Raja Yoga is a structural indication, not a "
                "promise of status, wealth or success. The complete chart "
                "and timing systems are needed for deeper assessment."
            ),
        },
        "dhana_yoga": {
            "title": "Dhana Yoga",
            "category": "Resources & Prosperity",
            "summary": (
                "A qualifying relationship among the 2nd, 5th, 9th and "
                "11th house lords. These houses are traditionally connected "
                "with resources, accumulated wealth, merit, opportunity and "
                "gains."
            ),
            "themes": [
                "resources",
                "financial opportunities",
                "accumulation",
                "gains",
                "practical value",
            ],
            "life_areas": [
                "income and resources",
                "financial planning",
                "gains from skills",
                "long-term material goals",
            ],
            "caution": (
                "Dhana Yoga does not guarantee a specific amount of money. "
                "Financial outcomes depend on the complete chart, timing "
                "and real-world circumstances."
            ),
        },
        "mahapurusha_mars": {
            "title": "Ruchaka Yoga",
            "category": "Pancha Mahapurusha",
            "summary": (
                "A Mars-based Pancha Mahapurusha combination associated "
                "traditionally with courage, initiative, strength and "
                "decisive action."
            ),
            "themes": ["courage", "initiative", "drive", "decisiveness"],
            "life_areas": ["leadership", "competition", "action-oriented work"],
            "caution": (
                "The combination is a structural indication; its expression "
                "depends on Mars and the wider chart."
            ),
        },
        "mahapurusha_mercury": {
            "title": "Bhadra Yoga",
            "category": "Pancha Mahapurusha",
            "summary": (
                "A Mercury-based Pancha Mahapurusha combination traditionally "
                "associated with intellect, communication, reasoning and skill."
            ),
            "themes": ["reasoning", "communication", "analysis", "skill"],
            "life_areas": ["education", "business", "writing", "technical work"],
            "caution": (
                "The combination is a structural indication; its expression "
                "depends on Mercury and the wider chart."
            ),
        },
        "mahapurusha_jupiter": {
            "title": "Hamsa Yoga",
            "category": "Pancha Mahapurusha",
            "summary": (
                "A Jupiter-based Pancha Mahapurusha combination traditionally "
                "associated with wisdom, learning, ethics and guidance."
            ),
            "themes": ["wisdom", "learning", "ethics", "guidance"],
            "life_areas": ["education", "teaching", "mentoring", "counsel"],
            "caution": (
                "The combination is a structural indication; its expression "
                "depends on Jupiter and the wider chart."
            ),
        },
        "mahapurusha_venus": {
            "title": "Malavya Yoga",
            "category": "Pancha Mahapurusha",
            "summary": (
                "A Venus-based Pancha Mahapurusha combination traditionally "
                "associated with refinement, relationships, creativity and "
                "comfort."
            ),
            "themes": ["refinement", "creativity", "relationships", "comfort"],
            "life_areas": ["arts", "relationships", "design", "lifestyle"],
            "caution": (
                "The combination is a structural indication; its expression "
                "depends on Venus and the wider chart."
            ),
        },
        "mahapurusha_saturn": {
            "title": "Sasa Yoga",
            "category": "Pancha Mahapurusha",
            "summary": (
                "A Saturn-based Pancha Mahapurusha combination traditionally "
                "associated with discipline, endurance, organization and "
                "responsibility."
            ),
            "themes": ["discipline", "endurance", "organization", "responsibility"],
            "life_areas": ["management", "long-term work", "administration", "structure"],
            "caution": (
                "The combination is a structural indication; its expression "
                "depends on Saturn and the wider chart."
            ),
        },
    }

    def __init__(self, yoga_result: dict[str, Any] | None):
        self.yoga_result = yoga_result or {}

    def _relationships_text(self, yoga: dict[str, Any]) -> str:
        relationships = yoga.get("relationships") or []
        if not relationships:
            return "Structural relationship identified."

        labels = {
            "same_lord": "same planetary lord",
            "conjunction": "conjunction in the same house",
            "mutual_aspect": "mutual planetary aspect",
            "sign_exchange": "sign exchange",
        }

        readable = [labels.get(item, item) for item in relationships]
        return ", ".join(readable)

    def _build_card(self, yoga: dict[str, Any]) -> dict[str, Any]:
        yoga_id = yoga.get("id", "")
        library = self.YOGA_LIBRARY.get(yoga_id)

        if library is None:
            return {
                "id": yoga_id,
                "title": yoga.get("name", yoga_id),
                "category": yoga.get("category", "Yoga"),
                "status": "detected",
                "summary": (
                    "A yoga was structurally detected by the TharuMaga "
                    "Yoga Detection Engine."
                ),
                "planets": yoga.get("planets", []),
                "houses": yoga.get("houses", []),
                "rule": yoga.get("rule", ""),
                "relationships": yoga.get("relationships", []),
                "relationship_summary": self._relationships_text(yoga),
                "themes": [],
                "life_areas": [],
                "caution": (
                    "This interpretation is intentionally limited because "
                    "no dedicated interpretation profile exists yet."
                ),
            }

        return {
            "id": yoga_id,
            "title": library["title"],
            "category": library["category"],
            "status": "detected",
            "summary": library["summary"],
            "planets": yoga.get("planets", []),
            "houses": yoga.get("houses", []),
            "rule": yoga.get("rule", ""),
            "relationships": yoga.get("relationships", []),
            "relationship_summary": self._relationships_text(yoga),
            "themes": list(library["themes"]),
            "life_areas": list(library["life_areas"]),
            "caution": library["caution"],
        }

    def generate(self) -> dict[str, Any]:
        detected = self.yoga_result.get("yogas", [])
        if not isinstance(detected, list):
            detected = []

        cards = [
            self._build_card(yoga)
            for yoga in detected
            if isinstance(yoga, dict)
        ]

        return {
            "engine": "TharuMaga Yoga Interpretation Engine",
            "version": "1.0",
            "source_engine": self.yoga_result.get(
                "engine",
                "TharuMaga Yoga Detection Engine",
            ),
            "source_engine_version": self.yoga_result.get("version"),
            "count": len(cards),
            "interpretations": cards,
        }


if __name__ == "__main__":
    from .astrology_engine import TharuMagaEngine
    from .yoga_detection_engine import TharuMagaYogaEngine

    chart = TharuMagaEngine(
        day=10,
        month=1,
        year=2000,
        hour=2,
        minute=25,
        second=0,
        latitude=6.9271,
        longitude=79.8612,
        timezone="Asia/Colombo",
        place="Colombo, Sri Lanka",
    ).calculate()

    yoga_result = TharuMagaYogaEngine(chart).generate()
    interpretation = TharuMagaYogaInterpretationEngine(yoga_result).generate()

    print("=" * 68)
    print("THARUMAGA YOGA INTERPRETATION ENGINE TEST")
    print("=" * 68)
    print("Detected yogas:", interpretation["count"])

    for card in interpretation["interpretations"]:
        print(f"- {card['title']} | {card['category']}")
        print(f"  Planets: {card['planets']}")
        print(f"  Houses: {card['houses']}")
        print(f"  Relationship: {card['relationship_summary']}")
        print(f"  Summary: {card['summary']}")
