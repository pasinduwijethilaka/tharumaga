from datetime import date, datetime
from typing import Any, Dict, Optional


class TharuMagaDashaInterpretationEngine:
    """
    Reads the already-calculated Vimshottari Dasha output from
    TharuMagaEngine and adds chart-context interpretation.

    This class does NOT calculate astronomy or Dasha dates.
    """

    PLANET_NAMES_SI = {
        "Sun": "රවි", "Moon": "සඳු", "Mars": "කුජ",
        "Mercury": "බුධ", "Jupiter": "ගුරු", "Venus": "සිකුරු",
        "Saturn": "ශනි", "Rahu": "රාහු", "Ketu": "කේතු",
    }

    SIGN_NAMES_SI = {
        "Aries": "මේෂ", "Taurus": "වෘෂභ", "Gemini": "මිථුන",
        "Cancer": "කටක", "Leo": "සිංහ", "Virgo": "කන්‍යා",
        "Libra": "තුලා", "Scorpio": "වෘශ්චික",
        "Sagittarius": "ධනු", "Capricorn": "මකර",
        "Aquarius": "කුම්භ", "Pisces": "මීන",
    }

    SIGN_LORDS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
    }

    HOUSE_MEANINGS = {
        1: "ස්වභාවය, පෞරුෂය, ශරීරය සහ ජීවිතයේ මූලික දිශාව",
        2: "ධනය, පවුල, කථනය සහ සමුච්චිත සම්පත්",
        3: "ධෛර්යය, සන්නිවේදනය, උත්සාහය සහ සහෝදර සම්බන්ධතා",
        4: "නිවස, මව, අභ්‍යන්තර සැනසීම, දේපළ සහ මනසේ ස්ථාවරත්වය",
        5: "බුද්ධිය, අධ්‍යාපනය, නිර්මාණශීලීත්වය, දරුවන් සහ ආදරය",
        6: "සේවය, දෛනික වැඩ, තරඟකාරීත්වය, ණය සහ සෞඛ්‍ය රැකවරණය",
        7: "විවාහය, හවුල්කාරිත්වය, ගනුදෙනු සහ මහජන සම්බන්ධතා",
        8: "පරිවර්තනය, ගැඹුරු කරුණු, හදිසි වෙනස්කම් සහ රහස්‍ය කරුණු",
        9: "භාග්‍යය, ධර්මය, උසස් අධ්‍යාපනය, ගුරුවරු සහ දුර ගමන්",
        10: "වෘත්තිය, කීර්තිය, වගකීම් සහ සමාජ තත්ත්වය",
        11: "ලාභ, ආදායම්, ජාලගත සම්බන්ධතා සහ බලාපොරොත්තු",
        12: "වියදම්, විදේශ සම්බන්ධතා, නිදහස් වීම සහ අභ්‍යන්තර ලෝකය",
    }

    PLANET_THEMES = {
        "Sun": "නායකත්වය, ස්වයං විශ්වාසය, අධිකාරිය, පියා සහ වෘත්තීය ගෞරවය",
        "Moon": "මනස, හැඟීම්, පවුල් බැඳීම්, ජන සම්බන්ධතා සහ මානසික ආරක්ෂාව",
        "Mars": "ක්‍රියාශීලීත්වය, ධෛර්යය, තරඟකාරීත්වය, ශක්තිය සහ තීරණාත්මක ක්‍රියා",
        "Mercury": "බුද්ධිය, ඉගෙනීම, සන්නිවේදනය, ගණනය, ව්‍යාපාර සහ තාක්ෂණය",
        "Jupiter": "දැනුම, ගුරුත්වය, උපදේශනය, විශ්වාසය, වර්ධනය සහ අවස්ථා",
        "Venus": "ආදරය, සබඳතා, කලාව, සුවපහසුව, වටිනාකම් සහ භෞතික සම්පත්",
        "Saturn": "වගකීම, ඉවසීම, විනය, ප්‍රමාදය, දිගුකාලීන වැඩ සහ ස්ථාවරත්වය",
        "Rahu": "නව අත්දැකීම්, අසාමාන්‍ය මාර්ග, අභිලාෂය, තාක්ෂණය සහ ද්‍රව්‍යමය අවධානය",
        "Ketu": "වෙන්වීම, අභ්‍යන්තර සෙවීම, ආධ්‍යාත්මිකත්වය, අත්හැරීම සහ විමර්ශනය",
    }

    def __init__(self, chart_data: Dict[str, Any],
                 as_of: Optional[date] = None):
        self.chart = chart_data or {}
        self.as_of = as_of or date.today()
        self.planets = self.chart.get("planets", {}) or {}
        self.rahu = self.chart.get("rahu", {}) or {}
        self.ketu = self.chart.get("ketu", {}) or {}
        self.dasha = self.chart.get("dasha", []) or []

    def planet_si(self, planet: Optional[str]) -> str:
        return self.PLANET_NAMES_SI.get(planet, planet or "-")

    def sign_si(self, sign: Optional[str]) -> str:
        return self.SIGN_NAMES_SI.get(sign, sign or "-")

    def date_value(self, value: Any) -> Optional[date]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        try:
            return datetime.fromisoformat(str(value)[:10]).date()
        except (ValueError, TypeError):
            return None

    def is_in_period(self, target: date, start: Any, end: Any) -> bool:
        start_date = self.date_value(start)
        end_date = self.date_value(end)
        return (
            start_date is not None
            and end_date is not None
            and start_date <= target < end_date
        )

    def planet_data(self, planet: str) -> Dict[str, Any]:
        if planet in self.planets:
            return self.planets[planet]
        if planet == "Rahu":
            return self.rahu
        if planet == "Ketu":
            return self.ketu
        return {}

    def find_current_period(self) -> Dict[str, Any]:
        for maha in self.dasha:
            if not isinstance(maha, dict):
                continue

            if not self.is_in_period(
                self.as_of,
                maha.get("start"),
                maha.get("end"),
            ):
                continue

            antardashas = maha.get("antardasha", [])
            if not isinstance(antardashas, list):
                antardashas = []

            for antar in antardashas:
                if not isinstance(antar, dict):
                    continue

                if not self.is_in_period(
                    self.as_of,
                    antar.get("start"),
                    antar.get("end"),
                ):
                    continue

                pratyantardashas = antar.get("pratyantardasha", [])
                if not isinstance(pratyantardashas, list):
                    pratyantardashas = []

                for praty in pratyantardashas:
                    if not isinstance(praty, dict):
                        continue

                    if self.is_in_period(
                        self.as_of,
                        praty.get("start"),
                        praty.get("end"),
                    ):
                        return {
                            "mahadasha": maha,
                            "antardasha": antar,
                            "pratyantardasha": praty,
                        }

                return {
                    "mahadasha": maha,
                    "antardasha": antar,
                    "pratyantardasha": None,
                }

            return {
                "mahadasha": maha,
                "antardasha": None,
                "pratyantardasha": None,
            }

        return {
            "mahadasha": None,
            "antardasha": None,
            "pratyantardasha": None,
        }

    def build_planet_context(self, planet: str) -> Dict[str, Any]:
        data = self.planet_data(planet)
        if not data:
            return {
                "planet": planet,
                "planet_si": self.planet_si(planet),
                "available": False,
            }

        sign = data.get("sign")
        sign_lord = self.SIGN_LORDS.get(sign)
        nak = data.get("nakshatra", {}) or {}

        return {
            "planet": planet,
            "planet_si": self.planet_si(planet),
            "available": True,
            "sign": sign,
            "sign_si": self.sign_si(sign),
            "house": data.get("house"),
            "sign_lord": sign_lord,
            "sign_lord_si": self.planet_si(sign_lord),
            "sign_lord_house": (
                self.planet_data(sign_lord).get("house")
                if sign_lord else None
            ),
            "nakshatra": nak.get("name"),
            "nakshatra_lord": nak.get("lord"),
            "nakshatra_lord_si": self.planet_si(nak.get("lord")),
            "pada": nak.get("pada"),
            "retrograde": data.get("retrograde", False),
        }

    def interpret_planet_period(self, planet: str, level: str) -> Dict[str, Any]:
        context = self.build_planet_context(planet)
        planet_si = self.planet_si(planet)

        if not context.get("available"):
            return {
                "planet": planet,
                "planet_si": planet_si,
                "available": False,
                "level": level,
                "level_si": {
                    "Mahadasha": "මහ දශාව",
                    "Antardasha": "අන්තර් දශාව",
                    "Pratyantardasha": "ප්‍රත්‍යන්තර දශාව",
                }.get(level, level),
                "text": f"{planet_si} සඳහා ග්‍රහ පිහිටීමේ දත්ත ලබාගෙන නොමැත.",
            }

        house = context["house"]
        level_si = {
            "Mahadasha": "මහ දශාව",
            "Antardasha": "අන්තර් දශාව",
            "Pratyantardasha": "ප්‍රත්‍යන්තර දශාව",
        }.get(level, level)

        text = (
            f"{planet_si}ගේ {level_si} කාලය තුළ "
            f"{self.PLANET_THEMES.get(planet, 'අදාළ ග්‍රහ තේමාවන්')} "
            f"යන කරුණු අවධානයට ගැනේ. "
            f"{planet_si} {context['sign_si']} රාශියේ "
            f"{house} වන භාවයේ පිහිටා ඇති බැවින්, "
            f"{self.HOUSE_MEANINGS.get(house, 'අදාළ ජීවන ක්ෂේත්‍ර')} "
            f"සම්බන්ධ කරුණු මෙම කාලය විශ්ලේෂණයේදී වැදගත් වේ. "
            f"{context['sign_si']} රාශියේ අධිපති "
            f"{context['sign_lord_si']} වන අතර එම අධිපති "
            f"{context['sign_lord_house'] or '-'} වන භාවයේ පිහිටා ඇත. "
            f"{context['nakshatra'] or '-'} නක්ෂත්‍රයේ "
            f"{context['pada'] or '-'} පාදය සහ එහි අධිපති "
            f"{context['nakshatra_lord_si']} යන කරුණුද සලකා බලයි."
        )

        if context["retrograde"]:
            text += (
                f" {planet_si} වක්‍ර ගමනක පවතින බැවින්, "
                f"සාම්ප්‍රදායික විශ්ලේෂණයේදී එම ග්‍රහ තේමාවන් "
                f"වෙනස් ආකාරයකින් හෝ අභ්‍යන්තර අත්දැකීමක් ලෙස සලකා බලයි."
            )

        return {**context, "level": level, "level_si": level_si, "text": text}

    def build_combined_text(
        self,
        maha: Dict[str, Any],
        antar: Optional[Dict[str, Any]],
        praty: Optional[Dict[str, Any]],
    ) -> str:
        text = f"දැනට පවතින ප්‍රධාන කාල තේමාව {self.planet_si(maha.get('lord'))} මහ දශාවයි."
        if antar:
            text += (
                f" එයට {self.planet_si(antar.get('lord'))} අන්තර් දශාව "
                f"සම්බන්ධ වී ඇති බැවින් ග්‍රහ දෙකේ තේමාවන් එකට සලකා බලයි."
            )
        if praty:
            text += (
                f" කෙටි කාල පරාසයේ {self.planet_si(praty.get('lord'))} "
                f"ප්‍රත්‍යන්තර දශාවද ක්‍රියාත්මක වේ."
            )
        return text

    def generate(self) -> Dict[str, Any]:
        current = self.find_current_period()
        maha = current.get("mahadasha")
        antar = current.get("antardasha")
        praty = current.get("pratyantardasha")

        if maha is None:
            return {
                "as_of": self.as_of.isoformat(),
                "available": False,
                "message": "මෙම දිනය සඳහා Dasha period එකක් හඳුනාගත නොහැකි විය.",
                "current": {},
            }

        return {
            "as_of": self.as_of.isoformat(),
            "available": True,
            "current": {
                "mahadasha": self.interpret_planet_period(
                    maha["lord"], "Mahadasha"
                ),
                "antardasha": (
                    self.interpret_planet_period(
                        antar["lord"], "Antardasha"
                    ) if antar else None
                ),
                "pratyantardasha": (
                    self.interpret_planet_period(
                        praty["lord"], "Pratyantardasha"
                    ) if praty else None
                ),
            },
            "periods": {
                "mahadasha": {
                    "lord": maha.get("lord"),
                    "start": maha.get("start"),
                    "end": maha.get("end"),
                    "years": maha.get("years"),
                },
                "antardasha": (
                    {
                        "lord": antar.get("lord"),
                        "start": antar.get("start"),
                        "end": antar.get("end"),
                        "years": antar.get("years"),
                    } if antar else None
                ),
                "pratyantardasha": (
                    {
                        "lord": praty.get("lord"),
                        "start": praty.get("start"),
                        "end": praty.get("end"),
                        "years": praty.get("years"),
                    } if praty else None
                ),
            },
            "combined_text": self.build_combined_text(maha, antar, praty),
        }
