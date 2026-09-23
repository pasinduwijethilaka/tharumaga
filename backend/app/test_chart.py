import swisseph as swe
from datetime import datetime
from zoneinfo import ZoneInfo


# ============================================================
# THARUMAGA - VEDIC ASTROLOGY ENGINE v3
# ============================================================
#
# CALCULATION STANDARD
# ------------------------------------------------------------
# Zodiac       : Sidereal
# Ayanamsa     : Lahiri
# Rahu         : True Node
# Ketu         : 180° opposite Rahu
# Ephemeris    : Swiss Ephemeris
# Time         : Local birth time -> UTC
# Lagna        : Swiss Ephemeris
# D1 / Rasi    : Whole Sign Houses
# Nakshatra    : 27 Nakshatras
# Pada         : 4 Padas per Nakshatra
#
# ============================================================


# ============================================================
# 1. BIRTH DATA
# ============================================================

YEAR = 1995
MONTH = 5
DAY = 15

BIRTH_HOUR = 10
BIRTH_MINUTE = 30
BIRTH_SECOND = 0

BIRTH_PLACE = "Colombo, Sri Lanka"

LATITUDE = 6.9271
LONGITUDE = 79.8612

TIMEZONE = "Asia/Colombo"


# ============================================================
# 2. ASTROLOGY CONFIGURATION
# ============================================================

ZODIAC_SYSTEM = "Sidereal"
AYANAMSA_NAME = "Lahiri"
RAHU_SYSTEM = "True Node"
KETU_SYSTEM = "180° opposite Rahu"
EPHEMERIS_NAME = "Swiss Ephemeris"
LAGNA_SYSTEM = "Swiss Ephemeris"
D1_HOUSE_SYSTEM = "Whole Sign"


# ============================================================
# 3. ZODIAC SIGNS
# ============================================================

ZODIAC_SIGNS = [
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


# ============================================================
# 4. NAKSHATRAS
# ============================================================
#
# Each Nakshatra = 13°20'
# Each Pada      = 3°20'
#
# Nakshatra Lords follow Vimshottari sequence.
#
# ============================================================

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


# ============================================================
# 5. PLANETS
# ============================================================

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
}


# ============================================================
# 6. NAKSHATRA CONSTANTS
# ============================================================

NAKSHATRA_SIZE = 360.0 / 27.0
PADA_SIZE = NAKSHATRA_SIZE / 4.0


# ============================================================
# 7. TIME CONVERSION
# ============================================================

birth_local = datetime(
    YEAR,
    MONTH,
    DAY,
    BIRTH_HOUR,
    BIRTH_MINUTE,
    BIRTH_SECOND,
    tzinfo=ZoneInfo(TIMEZONE),
)


# Local birth time -> UTC
birth_utc = birth_local.astimezone(
    ZoneInfo("UTC")
)


# Decimal UTC hour
utc_hour = (
    birth_utc.hour
    + birth_utc.minute / 60.0
    + birth_utc.second / 3600.0
)


# ============================================================
# 8. JULIAN DAY
# ============================================================

jd_ut = swe.julday(
    birth_utc.year,
    birth_utc.month,
    birth_utc.day,
    utc_hour,
)


# ============================================================
# 9. SIDEREAL MODE
# ============================================================

# Lahiri Ayanamsa
swe.set_sid_mode(
    swe.SIDM_LAHIRI
)


# ============================================================
# 10. HELPER FUNCTIONS
# ============================================================

def normalize_degree(value):
    """
    Normalize longitude into 0° <= value < 360°.
    """

    return value % 360.0


def get_sign_index(longitude):
    """
    Return zodiac sign index.

    Aries    = 0
    Taurus   = 1
    ...
    Pisces   = 11
    """

    longitude = normalize_degree(
        longitude
    )

    return int(longitude // 30.0)


def get_zodiac_sign(longitude):
    """
    Return:
        sign name
        degree inside sign
    """

    longitude = normalize_degree(
        longitude
    )

    sign_index = get_sign_index(
        longitude
    )

    degree = longitude % 30.0

    return (
        ZODIAC_SIGNS[sign_index],
        degree,
    )


def decimal_to_dms(decimal_degree):
    """
    Convert degree into:
        degrees
        minutes
        seconds
    """

    decimal_degree = decimal_degree % 30.0

    degrees = int(
        decimal_degree
    )

    minutes_float = (
        decimal_degree - degrees
    ) * 60.0

    minutes = int(
        minutes_float
    )

    seconds = (
        minutes_float - minutes
    ) * 60.0

    return (
        degrees,
        minutes,
        seconds,
    )


def format_dms(decimal_degree):
    """
    Format degree as:
        4° 3' 21.93"
    """

    degrees, minutes, seconds = (
        decimal_to_dms(
            decimal_degree
        )
    )

    return (
        f"{degrees}° "
        f"{minutes}' "
        f"{seconds:.2f}\""
    )


# ============================================================
# 11. NAKSHATRA CALCULATOR
# ============================================================

def get_nakshatra(longitude):
    """
    Calculate Nakshatra, Pada and Lord
    from sidereal longitude.

    360° / 27 = 13°20'
    13°20' / 4 = 3°20'
    """

    longitude = normalize_degree(
        longitude
    )

    # Determine Nakshatra number
    nakshatra_index = int(
        longitude / NAKSHATRA_SIZE
    )

    # Protect against floating-point edge case
    if nakshatra_index >= 27:
        nakshatra_index = 26

    # Position inside Nakshatra
    nakshatra_start = (
        nakshatra_index
        * NAKSHATRA_SIZE
    )

    position_in_nakshatra = (
        longitude
        - nakshatra_start
    )

    # Determine Pada: 1-4
    pada = int(
        position_in_nakshatra
        / PADA_SIZE
    ) + 1

    # Protect against edge case
    if pada > 4:
        pada = 4

    nakshatra_name, lord = (
        NAKSHATRAS[
            nakshatra_index
        ]
    )

    return {
        "index": nakshatra_index + 1,
        "name": nakshatra_name,
        "lord": lord,
        "pada": pada,
        "position": position_in_nakshatra,
    }


# ============================================================
# 12. WHOLE SIGN HOUSE
# ============================================================

def get_whole_sign_house(
    planet_longitude,
    lagna_longitude,
):
    """
    Determine D1/Rasi Whole Sign house.

    The Lagna sign = House 1.
    """

    planet_sign_index = (
        get_sign_index(
            planet_longitude
        )
    )

    lagna_sign_index = (
        get_sign_index(
            lagna_longitude
        )
    )

    house = (
        planet_sign_index
        - lagna_sign_index
    ) % 12 + 1

    return house


# ============================================================
# 13. HEADER
# ============================================================

print()
print("=" * 80)
print("THARUMAGA - VEDIC ASTROLOGY ENGINE v3")
print("=" * 80)


# ============================================================
# 14. CALCULATION STANDARD
# ============================================================

print()
print("CALCULATION STANDARD")
print("--------------------")

print(
    f"Zodiac       : {ZODIAC_SYSTEM}"
)

print(
    f"Ayanamsa     : {AYANAMSA_NAME}"
)

print(
    f"Rahu         : {RAHU_SYSTEM}"
)

print(
    f"Ketu         : {KETU_SYSTEM}"
)

print(
    f"Ephemeris    : {EPHEMERIS_NAME}"
)

print(
    f"Time         : Local birth time -> UTC"
)

print(
    f"Lagna        : {LAGNA_SYSTEM}"
)

print(
    f"D1 / Rasi    : {D1_HOUSE_SYSTEM}"
)

print(
    f"Nakshatra    : 27 Nakshatras"
)

print(
    f"Pada         : 4 Padas per Nakshatra"
)


# ============================================================
# 15. BIRTH INFORMATION
# ============================================================

print()
print("BIRTH INFORMATION")
print("------------------")

print(
    "Local Birth Time :",
    birth_local.strftime(
        "%d/%m/%Y %I:%M:%S %p %Z"
    ),
)

print(
    "UTC Birth Time   :",
    birth_utc.strftime(
        "%d/%m/%Y %H:%M:%S UTC"
    ),
)

print(
    f"Birth Place      : "
    f"{BIRTH_PLACE}"
)

print(
    f"Latitude         : "
    f"{LATITUDE}"
)

print(
    f"Longitude        : "
    f"{LONGITUDE}"
)

print()
print(
    f"Julian Day (UT)  : "
    f"{jd_ut:.8f}"
)


# ============================================================
# 16. LAGNA / ASCENDANT
# ============================================================

# Swiss Ephemeris calculates
# the astronomical Ascendant.

cusps, ascmc = swe.houses_ex(
    jd_ut,
    LATITUDE,
    LONGITUDE,
    b'P',
    swe.FLG_SIDEREAL,
)


ascendant = normalize_degree(
    ascmc[0]
)


lagna_sign, lagna_degree = (
    get_zodiac_sign(
        ascendant
    )
)


lagna_nakshatra = get_nakshatra(
    ascendant
)


# ============================================================
# 17. LAGNA OUTPUT
# ============================================================

print()
print("=" * 80)
print("LAGNA / ASCENDANT")
print("=" * 80)

print(
    f"Lagna Longitude : "
    f"{ascendant:.8f}°"
)

print(
    f"Lagna           : "
    f"{lagna_sign} "
    f"{format_dms(lagna_degree)}"
)

print(
    f"Nakshatra       : "
    f"{lagna_nakshatra['name']}"
)

print(
    f"Pada            : "
    f"{lagna_nakshatra['pada']}"
)

print(
    f"Nakshatra Lord  : "
    f"{lagna_nakshatra['lord']}"
)


# ============================================================
# 18. PLANETARY POSITIONS
# ============================================================

print()
print("=" * 80)
print("SIDEREAL PLANETARY POSITIONS")
print("=" * 80)


planet_results = {}


for planet_name, planet_id in PLANETS.items():

    flags = (
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    position, return_flags = (
        swe.calc_ut(
            jd_ut,
            planet_id,
            flags,
        )
    )

    longitude = normalize_degree(
        position[0]
    )

    latitude = position[1]

    distance = position[2]

    speed = position[3]


    sign, degree = (
        get_zodiac_sign(
            longitude
        )
    )


    retrograde = (
        speed < 0
    )


    house = get_whole_sign_house(
        longitude,
        ascendant,
    )


    nakshatra = get_nakshatra(
        longitude
    )


    planet_results[
        planet_name
    ] = {
        "longitude": longitude,
        "latitude": latitude,
        "distance": distance,
        "speed": speed,
        "sign": sign,
        "degree": degree,
        "retrograde": retrograde,
        "house": house,
        "nakshatra": nakshatra,
    }


    status = (
        "Retrograde"
        if retrograde
        else "Direct"
    )


    print()
    print(
        f"Planet      : "
        f"{planet_name}"
    )

    print(
        f"Longitude   : "
        f"{longitude:.8f}°"
    )

    print(
        f"Position    : "
        f"{sign} "
        f"{format_dms(degree)}"
    )

    print(
        f"House       : "
        f"{house}"
    )

    print(
        f"Nakshatra   : "
        f"{nakshatra['name']}"
    )

    print(
        f"Pada        : "
        f"{nakshatra['pada']}"
    )

    print(
        f"Nakshatra Lord : "
        f"{nakshatra['lord']}"
    )

    print(
        f"Latitude    : "
        f"{latitude:.8f}°"
    )

    print(
        f"Speed       : "
        f"{speed:.8f}°/day"
    )

    print(
        f"Motion      : "
        f"{status}"
    )


# ============================================================
# 19. TRUE RAHU
# ============================================================

print()
print("=" * 80)
print("RAHU / KETU")
print("=" * 80)


node_flags = (
    swe.FLG_SWIEPH
    | swe.FLG_SIDEREAL
    | swe.FLG_SPEED
)


node_position, node_return_flags = (
    swe.calc_ut(
        jd_ut,
        swe.TRUE_NODE,
        node_flags,
    )
)


# True Rahu
rahu_longitude = normalize_degree(
    node_position[0]
)

rahu_speed = node_position[3]


rahu_sign, rahu_degree = (
    get_zodiac_sign(
        rahu_longitude
    )
)


rahu_nakshatra = get_nakshatra(
    rahu_longitude
)


rahu_house = get_whole_sign_house(
    rahu_longitude,
    ascendant,
)


# ============================================================
# 20. KETU
# ============================================================

ketu_longitude = normalize_degree(
    rahu_longitude + 180.0
)


ketu_sign, ketu_degree = (
    get_zodiac_sign(
        ketu_longitude
    )
)


ketu_nakshatra = get_nakshatra(
    ketu_longitude
)


ketu_house = get_whole_sign_house(
    ketu_longitude,
    ascendant,
)


# ============================================================
# 21. RAHU OUTPUT
# ============================================================

print()
print("Rahu")
print("----")

print(
    f"Longitude      : "
    f"{rahu_longitude:.8f}°"
)

print(
    f"Position       : "
    f"{rahu_sign} "
    f"{format_dms(rahu_degree)}"
)

print(
    f"House          : "
    f"{rahu_house}"
)

print(
    f"Nakshatra      : "
    f"{rahu_nakshatra['name']}"
)

print(
    f"Pada           : "
    f"{rahu_nakshatra['pada']}"
)

print(
    f"Nakshatra Lord : "
    f"{rahu_nakshatra['lord']}"
)

print(
    f"Speed          : "
    f"{rahu_speed:.8f}°/day"
)


# ============================================================
# 22. KETU OUTPUT
# ============================================================

print()
print("Ketu")
print("----")

print(
    f"Longitude      : "
    f"{ketu_longitude:.8f}°"
)

print(
    f"Position       : "
    f"{ketu_sign} "
    f"{format_dms(ketu_degree)}"
)

print(
    f"House          : "
    f"{ketu_house}"
)

print(
    f"Nakshatra      : "
    f"{ketu_nakshatra['name']}"
)

print(
    f"Pada           : "
    f"{ketu_nakshatra['pada']}"
)

print(
    f"Nakshatra Lord : "
    f"{ketu_nakshatra['lord']}"
)


# ============================================================
# 23. D1 / RASI WHOLE SIGN HOUSES
# ============================================================

print()
print("=" * 80)
print("D1 / RASI - WHOLE SIGN HOUSES")
print("=" * 80)


lagna_sign_index = get_sign_index(
    ascendant
)


for house_number in range(1, 13):

    sign_index = (
        lagna_sign_index
        + house_number
        - 1
    ) % 12


    house_sign = (
        ZODIAC_SIGNS[
            sign_index
        ]
    )


    print(
        f"House {house_number:2d} : "
        f"{house_sign}"
    )


# ============================================================
# 24. PLANETS BY HOUSE
# ============================================================

print()
print("=" * 80)
print("PLANETS BY WHOLE SIGN HOUSE")
print("=" * 80)


house_planets = {
    house: []
    for house in range(1, 13)
}


# Normal planets
for planet_name, data in (
    planet_results.items()
):

    house_planets[
        data["house"]
    ].append(
        planet_name
    )


# Rahu
house_planets[
    rahu_house
].append("Rahu")


# Ketu
house_planets[
    ketu_house
].append("Ketu")


for house in range(1, 13):

    sign_index = (
        lagna_sign_index
        + house
        - 1
    ) % 12


    sign = (
        ZODIAC_SIGNS[
            sign_index
        ]
    )


    planets_in_house = (
        house_planets[
            house
        ]
    )


    if planets_in_house:

        planets_text = (
            ", ".join(
                planets_in_house
            )
        )

    else:

        planets_text = "Empty"


    print(
        f"House {house:2d} "
        f"({sign:12}) : "
        f"{planets_text}"
    )


# ============================================================
# 25. NAKSHATRA SUMMARY
# ============================================================

print()
print("=" * 80)
print("NAKSHATRA SUMMARY")
print("=" * 80)


for planet_name, data in (
    planet_results.items()
):

    nakshatra = data[
        "nakshatra"
    ]

    print(
        f"{planet_name:8} : "
        f"{nakshatra['name']:18} "
        f"Pada {nakshatra['pada']} "
        f"| Lord: "
        f"{nakshatra['lord']}"
    )


print(
    f"{'Rahu':8} : "
    f"{rahu_nakshatra['name']:18} "
    f"Pada {rahu_nakshatra['pada']} "
    f"| Lord: "
    f"{rahu_nakshatra['lord']}"
)


print(
    f"{'Ketu':8} : "
    f"{ketu_nakshatra['name']:18} "
    f"Pada {ketu_nakshatra['pada']} "
    f"| Lord: "
    f"{ketu_nakshatra['lord']}"
)


# ============================================================
# 26. FINAL STATUS
# ============================================================

print()
print("=" * 80)
print("THARUMAGA CALCULATION COMPLETE")
print("=" * 80)

print()
print("✓ Local time converted to UTC")
print("✓ Sidereal zodiac enabled")
print("✓ Lahiri ayanamsa enabled")
print("✓ Swiss Ephemeris enabled")
print("✓ Sun-Saturn calculated")
print("✓ True Rahu calculated")
print("✓ Ketu = Rahu + 180°")
print("✓ Lagna calculated by Swiss Ephemeris")
print("✓ D1 / Rasi uses Whole Sign Houses")
print("✓ Planets assigned to Whole Sign houses")
print("✓ 27 Nakshatras calculated")
print("✓ Nakshatra Pada calculated")
print("✓ Nakshatra Lords calculated")

print()
print("Next module: Vimshottari Dasha")
print("=" * 80)