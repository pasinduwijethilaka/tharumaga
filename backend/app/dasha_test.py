import swisseph as swe

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# THARUMAGA - VIMSHOTTARI DASHA ENGINE v1
# ============================================================
#
# CALCULATION STANDARD
# ------------------------------------------------------------
# Zodiac       : Sidereal
# Ayanamsa     : Lahiri
# Nakshatra    : 27 Nakshatras
# Dasha        : Vimshottari
# Cycle        : 120 years
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

TIMEZONE = "Asia/Colombo"

BIRTH_PLACE = "Colombo, Sri Lanka"

LATITUDE = 6.9271
LONGITUDE = 79.8612


# ============================================================
# 2. ASTROLOGY SETTINGS
# ============================================================

AYANAMSA_NAME = "Lahiri"
ZODIAC_SYSTEM = "Sidereal"
DASHA_SYSTEM = "Vimshottari"

NAKSHATRA_SIZE = 360.0 / 27.0


# ============================================================
# 3. NAKSHATRAS
# ============================================================
#
# Each Nakshatra has a fixed Vimshottari Lord.
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
# 4. VIMSHOTTARI DASHA YEARS
# ============================================================

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


# Vimshottari sequence
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


# ============================================================
# 5. LOCAL TIME → UTC
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


birth_utc = birth_local.astimezone(
    ZoneInfo("UTC")
)


# ============================================================
# 6. JULIAN DAY
# ============================================================

utc_hour = (
    birth_utc.hour
    + birth_utc.minute / 60.0
    + birth_utc.second / 3600.0
)


jd_ut = swe.julday(
    birth_utc.year,
    birth_utc.month,
    birth_utc.day,
    utc_hour,
)


# ============================================================
# 7. LAHIRI AYANAMSA
# ============================================================

swe.set_sid_mode(
    swe.SIDM_LAHIRI
)


# ============================================================
# 8. NORMALIZE LONGITUDE
# ============================================================

def normalize_degree(value):
    return value % 360.0


# ============================================================
# 9. GET NAKSHATRA
# ============================================================

def get_nakshatra(longitude):

    longitude = normalize_degree(
        longitude
    )

    nakshatra_index = int(
        longitude / NAKSHATRA_SIZE
    )

    if nakshatra_index >= 27:
        nakshatra_index = 26

    nakshatra_start = (
        nakshatra_index
        * NAKSHATRA_SIZE
    )

    position_in_nakshatra = (
        longitude
        - nakshatra_start
    )

    nakshatra_name, lord = (
        NAKSHATRAS[
            nakshatra_index
        ]
    )

    return {
        "index": nakshatra_index + 1,
        "name": nakshatra_name,
        "lord": lord,
        "start": nakshatra_start,
        "position": position_in_nakshatra,
    }


# ============================================================
# 10. CALCULATE MOON
# ============================================================

moon_position, moon_flags = (
    swe.calc_ut(
        jd_ut,
        swe.MOON,
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
    )
)


moon_longitude = normalize_degree(
    moon_position[0]
)


moon_nakshatra = get_nakshatra(
    moon_longitude
)


# ============================================================
# 11. NAKSHATRA PROGRESS
# ============================================================

position_in_nakshatra = (
    moon_nakshatra["position"]
)


nakshatra_completed_fraction = (
    position_in_nakshatra
    / NAKSHATRA_SIZE
)


nakshatra_remaining_fraction = (
    1.0
    - nakshatra_completed_fraction
)


# ============================================================
# 12. STARTING MAHADASHA
# ============================================================

starting_lord = (
    moon_nakshatra["lord"]
)


starting_dasha_years = (
    DASHA_YEARS[
        starting_lord
    ]
)


# Remaining balance
remaining_years = (
    starting_dasha_years
    * nakshatra_remaining_fraction
)


elapsed_years = (
    starting_dasha_years
    - remaining_years
)


# ============================================================
# 13. CONVERT YEARS TO DAYS
# ============================================================
#
# We use 365.2425 days per year for date calculations.
#
# This is an explicit TharuMaga implementation choice.
#
# ============================================================

DAYS_PER_YEAR = 365.2425


remaining_days = (
    remaining_years
    * DAYS_PER_YEAR
)


elapsed_days = (
    elapsed_years
    * DAYS_PER_YEAR
)


# ============================================================
# 14. DASHA END DATE
# ============================================================

birth_date_utc = birth_utc


first_dasha_end = (
    birth_date_utc
    + timedelta(
        days=remaining_days
    )
)


# ============================================================
# 15. HELPER - ADD DASHA
# ============================================================

def add_dasha(
    lord,
    start_date,
    duration_years,
):

    duration_days = (
        duration_years
        * DAYS_PER_YEAR
    )

    end_date = (
        start_date
        + timedelta(
            days=duration_days
        )
    )

    return {
        "lord": lord,
        "years": duration_years,
        "start": start_date,
        "end": end_date,
    }


# ============================================================
# 16. BUILD MAHADASHA TIMELINE
# ============================================================

start_index = DASHA_SEQUENCE.index(
    starting_lord
)


mahadashas = []


# ------------------------------------------------------------
# First Mahadasha
# ------------------------------------------------------------

current_start = birth_date_utc

first_dasha = {
    "lord": starting_lord,
    "years": remaining_years,
    "start": current_start,
    "end": first_dasha_end,
}


mahadashas.append(
    first_dasha
)


current_start = first_dasha_end


# ------------------------------------------------------------
# Remaining Mahadashas
# ------------------------------------------------------------

for offset in range(
    1,
    len(DASHA_SEQUENCE)
):

    lord_index = (
        start_index + offset
    ) % len(DASHA_SEQUENCE)

    lord = DASHA_SEQUENCE[
        lord_index
    ]

    years = DASHA_YEARS[
        lord
    ]

    dasha = add_dasha(
        lord,
        current_start,
        years,
    )

    mahadashas.append(
        dasha
    )

    current_start = dasha[
        "end"
    ]


# ============================================================
# 17. OUTPUT
# ============================================================

print()
print("=" * 80)
print("THARUMAGA - VIMSHOTTARI DASHA ENGINE")
print("=" * 80)


# ============================================================
# SETTINGS
# ============================================================

print()
print("DASHA SETTINGS")
print("--------------")

print(
    f"Zodiac       : "
    f"{ZODIAC_SYSTEM}"
)

print(
    f"Ayanamsa     : "
    f"{AYANAMSA_NAME}"
)

print(
    f"Dasha System  : "
    f"{DASHA_SYSTEM}"
)

print(
    f"Cycle         : "
    f"120 years"
)


# ============================================================
# BIRTH DATA
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


# ============================================================
# MOON
# ============================================================

print()
print("=" * 80)
print("MOON NAKSHATRA")
print("=" * 80)

print(
    f"Moon Longitude       : "
    f"{moon_longitude:.8f}°"
)

print(
    f"Nakshatra            : "
    f"{moon_nakshatra['name']}"
)

print(
    f"Nakshatra Lord       : "
    f"{starting_lord}"
)

print(
    f"Position in Nakshatra: "
    f"{position_in_nakshatra:.8f}°"
)

print(
    f"Completed             : "
    f"{nakshatra_completed_fraction * 100:.6f}%"
)

print(
    f"Remaining             : "
    f"{nakshatra_remaining_fraction * 100:.6f}%"
)


# ============================================================
# STARTING DASHA
# ============================================================

print()
print("=" * 80)
print("BIRTH MAHADASHA")
print("=" * 80)

print(
    f"Mahadasha Lord       : "
    f"{starting_lord}"
)

print(
    f"Full Mahadasha       : "
    f"{starting_dasha_years} years"
)

print(
    f"Elapsed              : "
    f"{elapsed_years:.8f} years"
)

print(
    f"Remaining            : "
    f"{remaining_years:.8f} years"
)

print(
    f"Remaining Days       : "
    f"{remaining_days:.4f}"
)

print(
    f"Mahadasha End        : "
    f"{first_dasha_end.strftime('%d/%m/%Y')}"
)


# ============================================================
# MAHADASHA TIMELINE
# ============================================================

print()
print("=" * 80)
print("VIMSHOTTARI MAHADASHA TIMELINE")
print("=" * 80)

for index, dasha in enumerate(
    mahadashas,
    start=1
):

    print()

    print(
        f"{index:2d}. "
        f"{dasha['lord']:8}"
    )

    print(
        f"    Start : "
        f"{dasha['start'].strftime('%d/%m/%Y')}"
    )

    print(
        f"    End   : "
        f"{dasha['end'].strftime('%d/%m/%Y')}"
    )

    print(
        f"    Years : "
        f"{dasha['years']:.8f}"
    )


# ============================================================
# FINAL
# ============================================================

print()
print("=" * 80)
print("THARUMAGA DASHA CALCULATION COMPLETE")
print("=" * 80)

print()
print("✓ Moon longitude calculated")
print("✓ Moon Nakshatra identified")
print("✓ Nakshatra Lord identified")
print("✓ Birth Mahadasha identified")
print("✓ Remaining Mahadasha balance calculated")
print("✓ Mahadasha timeline generated")

print()
print("Next module: Antardasha / Bhukti")
print("=" * 80)