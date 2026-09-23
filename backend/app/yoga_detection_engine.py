"""
TharuMaga Yoga Detection Engine v1.2
------------------------------------
Structural Jyotisha yoga detection for the TharuMaga D1/Rasi chart.

Astronomy is calculated by TharuMagaEngine. This module only evaluates
structural rules using Whole Sign houses.

v1.2 audit changes:
- Keeps same-lord, conjunction, mutual graha aspect and sign exchange.
- Uses Parashari graha drishti for mutual-aspect relationships.
- Expands Dharma-Karmadhipati, Raja and Dhana relationships.
- Avoids treating the 1st lord's dual Kendra/Trikona ownership by itself
  as a standalone Raja Yoga.
- Keeps formation separate from strength/cancellation/manifestation.
"""

from __future__ import annotations

from typing import Any


class TharuMagaYogaEngine:
    SIGN_ORDER = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
    ]

    SIGN_LORDS = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter",
    }

    KENDRA_HOUSES = {1, 4, 7, 10}
    TRIKONA_HOUSES = {1, 5, 9}

    # Parashari graha drishti:
    # all planets have the 7th aspect; Mars/Jupiter/Saturn have additional
    # special aspects. Rahu/Ketu are kept at 7th only for helper completeness.
    ASPECT_OFFSETS = {
        "Sun": {7},
        "Moon": {7},
        "Mars": {4, 7, 8},
        "Mercury": {7},
        "Jupiter": {5, 7, 9},
        "Venus": {7},
        "Saturn": {3, 7, 10},
        "Rahu": {7},
        "Ketu": {7},
    }

    def __init__(self, chart: dict[str, Any]):
        self.chart = chart or {}
        self.lagna = self.chart.get("lagna", {}) or {}
        self.planets = self.chart.get("planets", {}) or {}

    # ------------------------------------------------------------------
    # Basic helpers
    # ------------------------------------------------------------------

    def planet_house(self, planet: str) -> int | None:
        data = self.planets.get(planet, {})
        if not isinstance(data, dict):
            return None
        try:
            return int(data.get("house"))
        except (TypeError, ValueError):
            return None

    def planet_sign(self, planet: str) -> str | None:
        data = self.planets.get(planet, {})
        if not isinstance(data, dict):
            return None
        sign = data.get("sign")
        return sign if isinstance(sign, str) else None

    def planets_in_same_house(self, *planets: str) -> bool:
        houses = [self.planet_house(p) for p in planets]
        return None not in houses and len(set(houses)) == 1

    def lagna_sign(self) -> str | None:
        sign = self.lagna.get("sign")
        return sign if isinstance(sign, str) else None

    def house_sign(self, house: int) -> str | None:
        lagna = self.lagna_sign()
        if lagna not in self.SIGN_ORDER or not 1 <= house <= 12:
            return None
        index = self.SIGN_ORDER.index(lagna)
        return self.SIGN_ORDER[(index + house - 1) % 12]

    def house_lord(self, house: int) -> str | None:
        return self.SIGN_LORDS.get(self.house_sign(house))

    def lord_house(self, house: int) -> int | None:
        lord = self.house_lord(house)
        return self.planet_house(lord) if lord else None

    # ------------------------------------------------------------------
    # Relationship helpers
    # ------------------------------------------------------------------

    def planets_aspect(self, planet_a: str, planet_b: str) -> bool:
        """Return True when planet_a has a Parashari graha aspect to planet_b."""
        a_house = self.planet_house(planet_a)
        b_house = self.planet_house(planet_b)

        if a_house is None or b_house is None:
            return False

        distance = ((b_house - a_house) % 12) + 1
        return distance in self.ASPECT_OFFSETS.get(planet_a, {7})

    def mutual_aspect(self, planet_a: str, planet_b: str) -> bool:
        return (
            self.planets_aspect(planet_a, planet_b)
            and self.planets_aspect(planet_b, planet_a)
        )

    def sign_exchange(self, planet_a: str, planet_b: str) -> bool:
        """Return True when two planets occupy each other's ruled signs."""
        sign_a = self.planet_sign(planet_a)
        sign_b = self.planet_sign(planet_b)

        if not sign_a or not sign_b:
            return False

        return (
            self.SIGN_LORDS.get(sign_a) == planet_b
            and self.SIGN_LORDS.get(sign_b) == planet_a
        )

    def lord_relationship(self, planet_a: str | None, planet_b: str | None) -> list[str]:
        """
        Return all structural relationships found between two lords.

        Possible values:
        - same_lord
        - conjunction
        - mutual_aspect
        - sign_exchange
        """
        if not planet_a or not planet_b:
            return []

        if planet_a == planet_b:
            return ["same_lord"]

        relationships: list[str] = []

        house_a = self.planet_house(planet_a)
        house_b = self.planet_house(planet_b)

        if (
            house_a is not None
            and house_b is not None
            and house_a == house_b
        ):
            relationships.append("conjunction")

        if self.mutual_aspect(planet_a, planet_b):
            relationships.append("mutual_aspect")

        if self.sign_exchange(planet_a, planet_b):
            relationships.append("sign_exchange")

        return relationships

    def lord_connection(self, house_a: int, house_b: int) -> bool:
        return bool(
            self.lord_relationship(
                self.house_lord(house_a),
                self.house_lord(house_b),
            )
        )

    # ------------------------------------------------------------------
    # Output helper
    # ------------------------------------------------------------------

    def yoga(
        self,
        key: str,
        name: str,
        category: str,
        planets: list[str],
        houses: list[int],
        rule: str,
        relationships: list[str] | None = None,
    ) -> dict[str, Any]:
        result = {
            "id": key,
            "name": name,
            "category": category,
            "status": "detected",
            "planets": planets,
            "houses": houses,
            "rule": rule,
        }

        if relationships:
            result["relationships"] = relationships

        return result

    # ------------------------------------------------------------------
    # 1. Gaja Kesari Yoga
    # ------------------------------------------------------------------

    def detect_gaja_kesari(self) -> dict[str, Any] | None:
        moon_house = self.planet_house("Moon")
        jupiter_house = self.planet_house("Jupiter")

        if moon_house is None or jupiter_house is None:
            return None

        distance = ((jupiter_house - moon_house) % 12) + 1

        if distance in {1, 4, 7, 10}:
            return self.yoga(
                "gaja_kesari",
                "Gaja Kesari Yoga",
                "Mahapurusha / Raja-style",
                ["Moon", "Jupiter"],
                [moon_house, jupiter_house],
                "Jupiter is in a Kendra from the Moon.",
            )

        return None

    # ------------------------------------------------------------------
    # 2. Budha Aditya Yoga
    # ------------------------------------------------------------------

    def detect_budha_aditya(self) -> dict[str, Any] | None:
        if not self.planets_in_same_house("Sun", "Mercury"):
            return None

        house = self.planet_house("Sun")

        if house is None:
            return None

        return self.yoga(
            "budha_aditya",
            "Budha Aditya Yoga",
            "Intellect / Communication",
            ["Sun", "Mercury"],
            [house],
            "Sun and Mercury occupy the same house.",
            relationships=["conjunction"],
        )

    # ------------------------------------------------------------------
    # 3. Dharma Karmadhipati Yoga
    # ------------------------------------------------------------------

    def detect_dharma_karmadhipati(self) -> dict[str, Any] | None:
        ninth_lord = self.house_lord(9)
        tenth_lord = self.house_lord(10)
        relationships = self.lord_relationship(ninth_lord, tenth_lord)

        if not relationships:
            return None

        planets = sorted({p for p in (ninth_lord, tenth_lord) if p})
        return self.yoga(
            "dharma_karmadhipati",
            "Dharma Karmadhipati Yoga",
            "Raja Yoga",
            planets,
            [9, 10],
            "The 9th and 10th lords have a qualifying relationship: "
            "same lord, conjunction, mutual aspect, or sign exchange.",
            relationships=relationships,
        )

    # ------------------------------------------------------------------
    # 4. Raja Yoga
    # ------------------------------------------------------------------

    def detect_raja_yoga(self) -> dict[str, Any] | None:
        """
        Detect a Kendra-Trikona lord relationship.

        We use 5th/9th lords against 1st/4th/7th/10th lords.
        The 1st house is included as a Kendra, but a planet being both
        1st and another Kendra/Trikona lord is not treated as a standalone
        yoga unless there is an actual relationship between two lords.
        """
        found: list[tuple[int, int, str, str, list[str]]] = []

        for trikona in (5, 9):
            for kendra in (1, 4, 7, 10):
                trikona_lord = self.house_lord(trikona)
                kendra_lord = self.house_lord(kendra)

                relationships = self.lord_relationship(
                    trikona_lord,
                    kendra_lord,
                )

                if relationships:
                    found.append(
                        (
                            trikona,
                            kendra,
                            trikona_lord,
                            kendra_lord,
                            relationships,
                        )
                    )

        if not found:
            return None

        planets = sorted({
            p
            for _, _, lord_a, lord_b, _ in found
            for p in (lord_a, lord_b)
            if p
        })

        houses = sorted({
            h
            for house_a, house_b, _, _, _ in found
            for h in (house_a, house_b)
        })

        relationships = sorted({
            relationship
            for *_, rels in found
            for relationship in rels
        })

        return self.yoga(
            "raja_yoga",
            "Raja Yoga",
            "Raja Yoga",
            planets,
            houses,
            "A Trikona lord and Kendra lord have a qualifying "
            "relationship: same lord, conjunction, mutual aspect, "
            "or sign exchange.",
            relationships=relationships,
        )

    # ------------------------------------------------------------------
    # 5. Dhana Yoga
    # ------------------------------------------------------------------

    def detect_dhana_yoga(self) -> dict[str, Any] | None:
        """
        Detect structural relationships among the primary wealth houses:
        2nd, 5th, 9th and 11th.
        """
        wealth_houses = (2, 5, 9, 11)
        pairs: list[tuple[int, int, str, str, list[str]]] = []

        for index, house_a in enumerate(wealth_houses):
            for house_b in wealth_houses[index + 1:]:
                lord_a = self.house_lord(house_a)
                lord_b = self.house_lord(house_b)

                relationships = self.lord_relationship(lord_a, lord_b)

                if relationships:
                    pairs.append(
                        (
                            house_a,
                            house_b,
                            lord_a,
                            lord_b,
                            relationships,
                        )
                    )

        if not pairs:
            return None

        planets = sorted({
            p
            for _, _, lord_a, lord_b, _ in pairs
            for p in (lord_a, lord_b)
            if p
        })

        houses = sorted({
            h
            for house_a, house_b, _, _, _ in pairs
            for h in (house_a, house_b)
        })

        relationships = sorted({
            relationship
            for *_, rels in pairs
            for relationship in rels
        })

        return self.yoga(
            "dhana_yoga",
            "Dhana Yoga",
            "Wealth / Resources",
            planets,
            houses,
            "Lords of the 2nd, 5th, 9th and 11th houses have a "
            "qualifying relationship: same lord, conjunction, mutual "
            "aspect, or sign exchange.",
            relationships=relationships,
        )

    # ------------------------------------------------------------------
    # 6. Pancha Mahapurusha Yoga
    # ------------------------------------------------------------------

    def detect_pancha_mahapurusha(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        rules = {
            "Mars": {"Aries", "Scorpio", "Capricorn"},
            "Mercury": {"Gemini", "Virgo"},
            "Jupiter": {"Sagittarius", "Pisces", "Cancer"},
            "Venus": {"Taurus", "Libra", "Pisces"},
            "Saturn": {"Capricorn", "Aquarius", "Libra"},
        }

        names = {
            "Mars": "Ruchaka Yoga",
            "Mercury": "Bhadra Yoga",
            "Jupiter": "Hamsa Yoga",
            "Venus": "Malavya Yoga",
            "Saturn": "Sasa Yoga",
        }

        for planet, eligible_signs in rules.items():
            house = self.planet_house(planet)
            sign = self.planet_sign(planet)

            if house in self.KENDRA_HOUSES and sign in eligible_signs:
                results.append(
                    self.yoga(
                        f"mahapurusha_{planet.lower()}",
                        names[planet],
                        "Pancha Mahapurusha",
                        [planet],
                        [house],
                        f"{planet} is in a Kendra in its own or exaltation sign.",
                    )
                )

        return results

    # ------------------------------------------------------------------
    # Main detection
    # ------------------------------------------------------------------

    def detect(self) -> dict[str, Any]:
        yogas: list[dict[str, Any]] = []

        for detector in (
            self.detect_gaja_kesari,
            self.detect_budha_aditya,
            self.detect_dharma_karmadhipati,
            self.detect_raja_yoga,
            self.detect_dhana_yoga,
        ):
            result = detector()
            if result:
                yogas.append(result)

        yogas.extend(self.detect_pancha_mahapurusha())

        return {
            "engine": "TharuMaga Yoga Detection Engine",
            "version": "1.2",
            "system": "Traditional Vedic/Jyotisha rule detection",
            "house_system": "Whole Sign",
            "relationship_model": {
                "same_lord": True,
                "conjunction": True,
                "mutual_aspect": True,
                "sign_exchange": True,
            },
            "count": len(yogas),
            "yogas": yogas,
        }

    def generate(self) -> dict[str, Any]:
        return self.detect()


if __name__ == "__main__":
    from .astrology_engine import TharuMagaEngine

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

    result = TharuMagaYogaEngine(chart).generate()

    print("=" * 68)
    print("THARUMAGA YOGA DETECTION ENGINE v1.2 TEST")
    print("=" * 68)
    print("Detected yogas:", result["count"])

    for yoga in result["yogas"]:
        print(
            f"- {yoga['name']} | {yoga['planets']} | "
            f"houses {yoga['houses']} | "
            f"relationships {yoga.get('relationships', [])}"
        )
