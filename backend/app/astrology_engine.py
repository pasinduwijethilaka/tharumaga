import swisseph as swe
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class TharuMagaEngine:
    """
    TharuMaga Vedic Astrology Calculation Engine

    Standards:
    - Zodiac: Sidereal
    - Ayanamsa: Lahiri
    - Rahu: True Node
    - Ketu: 180 degrees opposite Rahu
    - Ephemeris: Swiss Ephemeris
    - D1 / Rasi: Whole Sign Houses
    - Nakshatra: 27
    - Pada: 4 per Nakshatra
    - Dasha: Vimshottari
    """

    # =========================================================================
    # CONSTANTS
    # =========================================================================

    SIGNS = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]

    PLANETS = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
    }

    DASHA_YEARS = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
    }

    DASHA_SEQUENCE = [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    ]

    NAKSHATRAS = [
        ("Ashwini", "Ketu"),
        ("Bharani", "Venus"),
        ("Krittika", "Sun"),
        ("Rohini", "Moon"),
        ("Mrigashira", "Mars"),
        ("Ardra", "Rahu"),
        ("Punarvasu", "Jupiter"),
        ("Pushya", "Saturn"),
        ("Ashlesha", "Mercury"),
        ("Magha", "Ketu"),
        ("Purva Phalguni", "Venus"),
        ("Uttara Phalguni", "Sun"),
        ("Hasta", "Moon"),
        ("Chitra", "Mars"),
        ("Swati", "Rahu"),
        ("Vishakha", "Jupiter"),
        ("Anuradha", "Saturn"),
        ("Jyeshtha", "Mercury"),
        ("Mula", "Ketu"),
        ("Purva Ashadha", "Venus"),
        ("Uttara Ashadha", "Sun"),
        ("Shravana", "Moon"),
        ("Dhanishta", "Mars"),
        ("Shatabhisha", "Rahu"),
        ("Purva Bhadrapada", "Jupiter"),
        ("Uttara Bhadrapada", "Saturn"),
        ("Revati", "Mercury"),
    ]

    NAKSHATRA_SIZE = 360.0 / 27.0
    PADA_SIZE = 360.0 / 108.0

    DASHA_CYCLE = 120.0

    # Current date conversion convention
    DAYS_PER_YEAR = 365.2425

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def __init__(
        self,
        day,
        month,
        year,
        hour,
        minute,
        second,
        latitude,
        longitude,
        timezone,
        place="",
    ):
        self.day = day
        self.month = month
        self.year = year

        self.hour = hour
        self.minute = minute
        self.second = second

        self.latitude = latitude
        self.longitude = longitude

        self.timezone = timezone
        self.place = place

        self.local_birth = None
        self.utc_birth = None
        self.jd_ut = None

        self.planets = {}
        self.rahu = None
        self.ketu = None
        self.lagna = None

        self.moon_nakshatra = None
        self.birth_mahadasha = None

        # Lahiri Ayanamsa
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Swiss Ephemeris + Sidereal + Speed
        self.flags = (
            swe.FLG_SWIEPH
            | swe.FLG_SIDEREAL
            | swe.FLG_SPEED
        )

    # =========================================================================
    # BASIC HELPERS
    # =========================================================================

    @staticmethod
    def normalize_degree(value):
        return value % 360.0

    @classmethod
    def get_sign_index(cls, longitude):
        longitude = cls.normalize_degree(longitude)

        index = int(longitude / 30.0)

        if index >= 12:
            index = 11

        return index

    @classmethod
    def get_sign(cls, longitude):
        return cls.SIGNS[
            cls.get_sign_index(longitude)
        ]

    @classmethod
    def get_nakshatra(cls, longitude):
        longitude = cls.normalize_degree(longitude)

        index = int(
            longitude / cls.NAKSHATRA_SIZE
        )

        if index >= 27:
            index = 26

        name, lord = cls.NAKSHATRAS[index]

        start_degree = (
            index * cls.NAKSHATRA_SIZE
        )

        position = (
            longitude - start_degree
        )

        completed_fraction = (
            position / cls.NAKSHATRA_SIZE
        )

        remaining_fraction = (
            1.0 - completed_fraction
        )

        pada = int(
            position / cls.PADA_SIZE
        ) + 1

        if pada > 4:
            pada = 4

        return {
            "name": name,
            "lord": lord,
            "pada": pada,
            "position_degrees": position,
            "completed_percent": (
                completed_fraction * 100.0
            ),
            "remaining_percent": (
                remaining_fraction * 100.0
            ),
            "completed_fraction": (
                completed_fraction
            ),
            "remaining_fraction": (
                remaining_fraction
            ),
        }

    @classmethod
    def add_dasha_years(cls, start_date, years):
        return start_date + timedelta(
            days=years * cls.DAYS_PER_YEAR
        )

    @classmethod
    def dasha_index(cls, lord):
        return cls.DASHA_SEQUENCE.index(lord)

    # =========================================================================
    # TIME CALCULATION
    # =========================================================================

    def calculate_time(self):

        local_tz = ZoneInfo(
            self.timezone
        )

        self.local_birth = datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            tzinfo=local_tz,
        )

        self.utc_birth = (
            self.local_birth.astimezone(
                ZoneInfo("UTC")
            )
        )

        ut_hour = (
            self.utc_birth.hour
            + self.utc_birth.minute / 60.0
            + self.utc_birth.second / 3600.0
        )

        self.jd_ut = swe.julday(
            self.utc_birth.year,
            self.utc_birth.month,
            self.utc_birth.day,
            ut_hour,
        )

    # =========================================================================
    # PLANETS
    # =========================================================================

    def calculate_planets(self):

        self.planets = {}

        for name, planet_id in self.PLANETS.items():

            data, ret_flags = swe.calc_ut(
                self.jd_ut,
                planet_id,
                self.flags,
            )

            longitude = self.normalize_degree(
                data[0]
            )

            speed = data[3]

            self.planets[name] = {
                "longitude": longitude,
                "sign": self.get_sign(longitude),
                "sign_index": self.get_sign_index(
                    longitude
                ),
                "speed": speed,
                "retrograde": speed < 0,
                "nakshatra": self.get_nakshatra(
                    longitude
                ),
            }

    # =========================================================================
    # RAHU / KETU
    # =========================================================================

    def calculate_nodes(self):

        data, ret_flags = swe.calc_ut(
            self.jd_ut,
            swe.TRUE_NODE,
            self.flags,
        )

        rahu_longitude = self.normalize_degree(
            data[0]
        )

        ketu_longitude = self.normalize_degree(
            rahu_longitude + 180.0
        )

        self.rahu = {
            "longitude": rahu_longitude,
            "sign": self.get_sign(
                rahu_longitude
            ),
            "sign_index": self.get_sign_index(
                rahu_longitude
            ),
            "speed": data[3],
            "retrograde": data[3] < 0,
            "nakshatra": self.get_nakshatra(
                rahu_longitude
            ),
        }

        self.ketu = {
            "longitude": ketu_longitude,
            "sign": self.get_sign(
                ketu_longitude
            ),
            "sign_index": self.get_sign_index(
                ketu_longitude
            ),
            "speed": data[3],
            "retrograde": data[3] < 0,
            "nakshatra": self.get_nakshatra(
                ketu_longitude
            ),
        }

    # =========================================================================
    # LAGNA
    # =========================================================================

    def calculate_lagna(self):

        cusps, ascmc = swe.houses_ex(
            self.jd_ut,
            self.latitude,
            self.longitude,
            b"P",
            swe.FLG_SIDEREAL,
        )

        lagna_longitude = self.normalize_degree(
            ascmc[0]
        )

        self.lagna = {
            "longitude": lagna_longitude,
            "sign": self.get_sign(
                lagna_longitude
            ),
            "sign_index": self.get_sign_index(
                lagna_longitude
            ),
            "nakshatra": self.get_nakshatra(
                lagna_longitude
            ),
        }

    # =========================================================================
    # D1 WHOLE SIGN HOUSES
    # =========================================================================

    def calculate_houses(self):

        lagna_sign_index = (
            self.lagna["sign_index"]
        )

        for planet in self.planets.values():

            planet["house"] = (
                (
                    planet["sign_index"]
                    - lagna_sign_index
                ) % 12
            ) + 1

        self.rahu["house"] = (
            (
                self.rahu["sign_index"]
                - lagna_sign_index
            ) % 12
        ) + 1

        self.ketu["house"] = (
            (
                self.ketu["sign_index"]
                - lagna_sign_index
            ) % 12
        ) + 1

    # =========================================================================
    # BIRTH MAHADASHA
    # =========================================================================

    def calculate_birth_mahadasha(self):

        moon_longitude = (
            self.planets["Moon"]["longitude"]
        )

        moon_nakshatra = (
            self.get_nakshatra(
                moon_longitude
            )
        )

        self.moon_nakshatra = (
            moon_nakshatra
        )

        lord = moon_nakshatra["lord"]

        full_years = (
            self.DASHA_YEARS[lord]
        )

        remaining_years = (
            full_years
            * moon_nakshatra[
                "remaining_fraction"
            ]
        )

        birth_start = (
            self.local_birth.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        )

        end_date = (
            birth_start
            + timedelta(
                days=(
                    remaining_years
                    * self.DAYS_PER_YEAR
                )
            )
        )

        self.birth_mahadasha = {
            "lord": lord,
            "full_years": full_years,
            "remaining_years": remaining_years,
            "start": birth_start,
            "end": end_date,
        }

    # =========================================================================
    # MAHADASHA TIMELINE
    # =========================================================================

    def get_mahadasha_timeline(self):

        timeline = []

        birth_lord = (
            self.birth_mahadasha["lord"]
        )

        birth_start = (
            self.birth_mahadasha["start"]
        )

        birth_end = (
            self.birth_mahadasha["end"]
        )

        start_index = self.dasha_index(
            birth_lord
        )

        timeline.append({
            "lord": birth_lord,
            "start": birth_start,
            "end": birth_end,
            "years": (
                self.birth_mahadasha[
                    "remaining_years"
                ]
            ),
        })

        current_start = birth_end

        for step in range(1, 9):

            index = (
                start_index + step
            ) % len(
                self.DASHA_SEQUENCE
            )

            lord = (
                self.DASHA_SEQUENCE[index]
            )

            years = (
                self.DASHA_YEARS[lord]
            )

            current_end = (
                self.add_dasha_years(
                    current_start,
                    years,
                )
            )

            timeline.append({
                "lord": lord,
                "start": current_start,
                "end": current_end,
                "years": years,
            })

            current_start = current_end

        return timeline

    # =========================================================================
    # ANTARDASHA
    # =========================================================================

    def get_antardasha(
        self,
        maha_lord,
        maha_start,
        maha_end,
    ):

        result = []

        maha_years = (
            self.DASHA_YEARS[
                maha_lord
            ]
        )

        start_index = (
            self.dasha_index(
                maha_lord
            )
        )

        current_start = maha_start

        for step in range(9):

            index = (
                start_index + step
            ) % len(
                self.DASHA_SEQUENCE
            )

            antar_lord = (
                self.DASHA_SEQUENCE[index]
            )

            antar_years = (
                maha_years
                * self.DASHA_YEARS[
                    antar_lord
                ]
                / self.DASHA_CYCLE
            )

            current_end = (
                current_start
                + timedelta(
                    days=(
                        antar_years
                        * self.DAYS_PER_YEAR
                    )
                )
            )

            if current_end > maha_end:
                current_end = maha_end

            result.append({
                "mahadasha": maha_lord,
                "lord": antar_lord,
                "start": current_start,
                "end": current_end,
                "years": antar_years,
            })

            current_start = current_end

        return result

    # =========================================================================
    # PRATYANTARDASHA
    # =========================================================================

    def get_pratyantardasha(
        self,
        maha_lord,
        antar_lord,
        antar_start,
        antar_end,
    ):

        result = []

        maha_years = (
            self.DASHA_YEARS[
                maha_lord
            ]
        )

        antar_years = (
            maha_years
            * self.DASHA_YEARS[
                antar_lord
            ]
            / self.DASHA_CYCLE
        )

        start_index = (
            self.dasha_index(
                antar_lord
            )
        )

        current_start = antar_start

        for step in range(9):

            index = (
                start_index + step
            ) % len(
                self.DASHA_SEQUENCE
            )

            praty_lord = (
                self.DASHA_SEQUENCE[index]
            )

            praty_years = (
                antar_years
                * self.DASHA_YEARS[
                    praty_lord
                ]
                / self.DASHA_CYCLE
            )

            current_end = (
                current_start
                + timedelta(
                    days=(
                        praty_years
                        * self.DAYS_PER_YEAR
                    )
                )
            )

            if current_end > antar_end:
                current_end = antar_end

            result.append({
                "mahadasha": maha_lord,
                "antardasha": antar_lord,
                "lord": praty_lord,
                "start": current_start,
                "end": current_end,
                "years": praty_years,
            })

            current_start = current_end

        return result

    # =========================================================================
    # COMPLETE DASHA SYSTEM
    # =========================================================================

    def calculate_dasha_system(self):

        mahadasha = (
            self.get_mahadasha_timeline()
        )

        complete = []

        for maha in mahadasha:

            antardashas = (
                self.get_antardasha(
                    maha["lord"],
                    maha["start"],
                    maha["end"],
                )
            )

            maha_data = {
                "lord": maha["lord"],
                "start": maha["start"],
                "end": maha["end"],
                "years": maha["years"],
                "antardasha": [],
            }

            for antar in antardashas:

                pratyantardashas = (
                    self.get_pratyantardasha(
                        maha["lord"],
                        antar["lord"],
                        antar["start"],
                        antar["end"],
                    )
                )

                maha_data[
                    "antardasha"
                ].append({
                    "lord": antar["lord"],
                    "start": antar["start"],
                    "end": antar["end"],
                    "years": antar["years"],
                    "pratyantardasha": (
                        pratyantardashas
                    ),
                })

            complete.append(
                maha_data
            )

        return complete

    # =========================================================================
    # JSON SERIALIZATION
    # =========================================================================

    @classmethod
    def serialize_value(cls, value):

        if isinstance(value, datetime):
            return value.strftime(
                "%Y-%m-%d"
            )

        if isinstance(value, dict):
            return {
                key: cls.serialize_value(
                    val
                )
                for key, val in value.items()
            }

        if isinstance(value, list):
            return [
                cls.serialize_value(item)
                for item in value
            ]

        return value

    # =========================================================================
    # FINAL CALCULATION
    # =========================================================================

    def calculate(self):

        # Time
        self.calculate_time()

        # Planets
        self.calculate_planets()

        # Rahu/Ketu
        self.calculate_nodes()

        # Lagna
        self.calculate_lagna()

        # Houses
        self.calculate_houses()

        # Birth Dasha
        self.calculate_birth_mahadasha()

        # Full Dasha system
        dasha_system = (
            self.calculate_dasha_system()
        )

        result = {
            "engine": {
                "name": "TharuMaga",
                "version": "1.0",
                "zodiac": "Sidereal",
                "ayanamsa": "Lahiri",
                "rahu": "True Node",
                "ketu": "180° opposite Rahu",
                "house_system": "Whole Sign",
                "dasha_system": "Vimshottari",
            },

            "birth": {
                "date": (
                    self.local_birth.strftime(
                        "%Y-%m-%d"
                    )
                ),
                "local_time": (
                    self.local_birth.strftime(
                        "%H:%M:%S"
                    )
                ),
                "timezone": self.timezone,
                "utc": (
                    self.utc_birth.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ),
                "place": self.place,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "julian_day_ut": self.jd_ut,
            },

            "lagna": {
                "longitude": (
                    self.lagna[
                        "longitude"
                    ]
                ),
                "sign": (
                    self.lagna[
                        "sign"
                    ]
                ),
                "sign_index": (
                    self.lagna[
                        "sign_index"
                    ]
                ),
                "nakshatra": (
                    self.lagna[
                        "nakshatra"
                    ]
                ),
            },

            "planets": self.planets,

            "rahu": self.rahu,

            "ketu": self.ketu,

            "d1": {
                "house_system": "Whole Sign",
                "lagna_sign": (
                    self.lagna[
                        "sign"
                    ]
                ),
                "lagna_sign_index": (
                    self.lagna[
                        "sign_index"
                    ]
                ),
            },

            "moon_nakshatra": (
                self.moon_nakshatra
            ),

            "birth_mahadasha": {
                "lord": (
                    self.birth_mahadasha[
                        "lord"
                    ]
                ),
                "full_years": (
                    self.birth_mahadasha[
                        "full_years"
                    ]
                ),
                "remaining_years": (
                    self.birth_mahadasha[
                        "remaining_years"
                    ]
                ),
                "start": (
                    self.birth_mahadasha[
                        "start"
                    ]
                ),
                "end": (
                    self.birth_mahadasha[
                        "end"
                    ]
                ),
            },

            "dasha": dasha_system,
        }

        # Convert every datetime recursively.
        return self.serialize_value(
            result
        )


# =============================================================================
# MAIN TEST
# =============================================================================

if __name__ == "__main__":

    print("=" * 80)
    print("THARUMAGA MAIN ASTROLOGY ENGINE TEST")
    print("=" * 80)

    engine = TharuMagaEngine(
        day=15,
        month=5,
        year=1995,
        hour=10,
        minute=30,
        second=0,
        latitude=6.9271,
        longitude=79.8612,
        timezone="Asia/Colombo",
        place="Colombo, Sri Lanka",
    )

    chart = engine.calculate()

    print()
    print("ENGINE STATUS")
    print("-" * 20)

    print("✓ Engine initialized")
    print("✓ Time converted")
    print("✓ Julian Day calculated")
    print("✓ Planets calculated")
    print("✓ True Rahu calculated")
    print("✓ Ketu calculated")
    print("✓ Lagna calculated")
    print("✓ Whole Sign D1 calculated")
    print("✓ Nakshatra calculated")
    print("✓ Vimshottari Mahadasha calculated")
    print("✓ Antardasha calculated")
    print("✓ Pratyantardasha calculated")

    print()
    print("CORE RESULTS")
    print("-" * 20)

    print(
        f"Lagna      : "
        f"{chart['lagna']['sign']}"
    )

    print(
        f"Moon       : "
        f"{chart['planets']['Moon']['sign']}"
    )

    print(
        f"Nakshatra  : "
        f"{chart['moon_nakshatra']['name']}"
    )

    print(
        f"Pada       : "
        f"{chart['moon_nakshatra']['pada']}"
    )

    print(
        f"Birth Dasha: "
        f"{chart['birth_mahadasha']['lord']}"
    )

    print(
        f"Rahu       : "
        f"{chart['rahu']['sign']}"
    )

    print(
        f"Ketu       : "
        f"{chart['ketu']['sign']}"
    )

    print()
    print("=" * 80)
    print("THARUMAGA MAIN ENGINE TEST COMPLETE")
    print("=" * 80)