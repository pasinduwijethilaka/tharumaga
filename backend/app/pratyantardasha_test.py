import swisseph as swe
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# =============================================================================
# THARUMAGA - PRATYANTARDASHA / SOOKSHMA DASHA ENGINE v1
# =============================================================================

print("=" * 80)
print("THARUMAGA - PRATYANTARDASHA / SOOKSHMA DASHA ENGINE")
print("=" * 80)

# =============================================================================
# BIRTH DATA
# =============================================================================

DAY = 15
MONTH = 5
YEAR = 1995

HOUR = 10
MINUTE = 30
SECOND = 0

TIMEZONE = "Asia/Colombo"

PLACE = "Colombo, Sri Lanka"
LATITUDE = 6.9271
LONGITUDE = 79.8612

# =============================================================================
# DASHA SETTINGS
# =============================================================================

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

DASHA_CYCLE = 120.0
DAYS_PER_YEAR = 365.2425

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


# =============================================================================
# HELPERS
# =============================================================================

def normalize_degree(value):
    return value % 360.0


def get_nakshatra(longitude):
    longitude = normalize_degree(longitude)

    index = int(longitude / NAKSHATRA_SIZE)

    if index >= 27:
        index = 26

    name, lord = NAKSHATRAS[index]

    position = (
        longitude
        - index * NAKSHATRA_SIZE
    )

    completed_fraction = (
        position / NAKSHATRA_SIZE
    )

    remaining_fraction = (
        1.0 - completed_fraction
    )

    return (
        name,
        lord,
        position,
        completed_fraction,
        remaining_fraction,
    )


def add_years(start_date, years):
    return start_date + timedelta(
        days=years * DAYS_PER_YEAR
    )


def format_date(value):
    return value.strftime("%d/%m/%Y")


def dasha_index(lord):
    return DASHA_SEQUENCE.index(lord)


# =============================================================================
# LOCAL TIME → UTC
# =============================================================================

local_tz = ZoneInfo(TIMEZONE)

local_birth = datetime(
    YEAR,
    MONTH,
    DAY,
    HOUR,
    MINUTE,
    SECOND,
    tzinfo=local_tz,
)

utc_birth = local_birth.astimezone(
    ZoneInfo("UTC")
)

print()
print("DASHA SETTINGS")
print("-" * 14)

print("Zodiac       : Sidereal")
print("Ayanamsa     : Lahiri")
print("Dasha System : Vimshottari")
print("Cycle        : 120 years")

print()
print("BIRTH INFORMATION")
print("-" * 18)

print(
    f"Local Birth Time : "
    f"{local_birth.strftime('%d/%m/%Y %I:%M:%S %p %z')}"
)

print(
    f"UTC Birth Time   : "
    f"{utc_birth.strftime('%d/%m/%Y %H:%M:%S UTC')}"
)

print(
    f"Birth Place      : {PLACE}"
)


# =============================================================================
# JULIAN DAY
# =============================================================================

ut_hour = (
    utc_birth.hour
    + utc_birth.minute / 60.0
    + utc_birth.second / 3600.0
)

jd_ut = swe.julday(
    utc_birth.year,
    utc_birth.month,
    utc_birth.day,
    ut_hour,
)


# =============================================================================
# SWISS EPHEMERIS
# =============================================================================

swe.set_sid_mode(
    swe.SIDM_LAHIRI
)

flags = (
    swe.FLG_SWIEPH
    | swe.FLG_SIDEREAL
    | swe.FLG_SPEED
)

moon_data, ret_flags = swe.calc_ut(
    jd_ut,
    swe.MOON,
    flags,
)

moon_longitude = normalize_degree(
    moon_data[0]
)


# =============================================================================
# MOON NAKSHATRA
# =============================================================================

(
    moon_nakshatra,
    moon_lord,
    moon_position,
    completed_fraction,
    remaining_fraction,
) = get_nakshatra(
    moon_longitude
)

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
    f"{moon_nakshatra}"
)

print(
    f"Nakshatra Lord       : "
    f"{moon_lord}"
)

print(
    f"Position in Nakshatra: "
    f"{moon_position:.8f}°"
)

print(
    f"Completed            : "
    f"{completed_fraction * 100:.8f}%"
)

print(
    f"Remaining            : "
    f"{remaining_fraction * 100:.8f}%"
)


# =============================================================================
# BIRTH MAHADASHA
# =============================================================================

birth_mahadasha = moon_lord

birth_mahadasha_years = (
    DASHA_YEARS[birth_mahadasha]
)

remaining_birth_years = (
    birth_mahadasha_years
    * remaining_fraction
)

birth_start = local_birth.replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
)

birth_mahadasha_end = (
    birth_start
    + timedelta(
        days=remaining_birth_years
        * DAYS_PER_YEAR
    )
)

print()
print("=" * 80)
print("BIRTH MAHADASHA")
print("=" * 80)

print(
    f"Mahadasha Lord : "
    f"{birth_mahadasha}"
)

print(
    f"Full Years     : "
    f"{birth_mahadasha_years}"
)

print(
    f"Remaining Years : "
    f"{remaining_birth_years:.8f}"
)

print(
    f"End            : "
    f"{format_date(birth_mahadasha_end)}"
)


# =============================================================================
# FIND MERCURY MAHADASHA
# =============================================================================

start_index = dasha_index(
    birth_mahadasha
)

mercury_start = None
mercury_end = None

current_start = birth_mahadasha_end

for step in range(1, 10):

    index = (
        start_index + step
    ) % len(DASHA_SEQUENCE)

    lord = DASHA_SEQUENCE[index]

    duration = DASHA_YEARS[lord]

    current_end = add_years(
        current_start,
        duration
    )

    if lord == "Mercury":

        mercury_start = current_start
        mercury_end = current_end

        break

    current_start = current_end


# =============================================================================
# MERCURY MAHADASHA
# =============================================================================

print()
print("=" * 80)
print("MERCURY MAHADASHA")
print("=" * 80)

print(
    f"Start : {format_date(mercury_start)}"
)

print(
    f"End   : {format_date(mercury_end)}"
)

print(
    f"Years : {DASHA_YEARS['Mercury']}"
)


# =============================================================================
# FIND MERCURY / SATURN ANTARDASHA
# =============================================================================

maha_lord = "Mercury"

antar_lord = "Saturn"

maha_years = DASHA_YEARS[
    maha_lord
]

antar_start_index = dasha_index(
    maha_lord
)

antar_start = mercury_start

saturn_antar_start = None
saturn_antar_end = None

for step in range(9):

    index = (
        antar_start_index + step
    ) % len(DASHA_SEQUENCE)

    lord = DASHA_SEQUENCE[index]

    antar_years = DASHA_YEARS[lord]

    antar_duration_years = (
        maha_years
        * antar_years
        / DASHA_CYCLE
    )

    antar_end = (
        antar_start
        + timedelta(
            days=antar_duration_years
            * DAYS_PER_YEAR
        )
    )

    if lord == antar_lord:

        saturn_antar_start = antar_start
        saturn_antar_end = antar_end

        break

    antar_start = antar_end


# =============================================================================
# MERCURY / SATURN ANTARDASHA
# =============================================================================

print()
print("=" * 80)
print("MERCURY / SATURN ANTARDASHA")
print("=" * 80)

print(
    f"Start : "
    f"{format_date(saturn_antar_start)}"
)

print(
    f"End   : "
    f"{format_date(saturn_antar_end)}"
)

saturn_antar_years = (
    maha_years
    * DASHA_YEARS["Saturn"]
    / DASHA_CYCLE
)

print(
    f"Years : "
    f"{saturn_antar_years:.8f}"
)


# =============================================================================
# PRATYANTARDASHA
# =============================================================================

print()
print("=" * 80)
print("MERCURY / SATURN - PRATYANTARDASHA")
print("=" * 80)

print()

praty_start_index = dasha_index(
    antar_lord
)

praty_start = saturn_antar_start

for step in range(9):

    index = (
        praty_start_index + step
    ) % len(DASHA_SEQUENCE)

    praty_lord = DASHA_SEQUENCE[index]

    praty_years = (
        saturn_antar_years
        * DASHA_YEARS[praty_lord]
        / DASHA_CYCLE
    )

    praty_days = (
        praty_years
        * DAYS_PER_YEAR
    )

    praty_end = (
        praty_start
        + timedelta(
            days=praty_days
        )
    )

    print(
        f"{step + 1:2}. "
        f"Mercury / Saturn / "
        f"{praty_lord}"
    )

    print(
        f"    Start : "
        f"{format_date(praty_start)}"
    )

    print(
        f"    End   : "
        f"{format_date(praty_end)}"
    )

    print(
        f"    Years : "
        f"{praty_years:.10f}"
    )

    print(
        f"    Days  : "
        f"{praty_days:.6f}"
    )

    print()

    praty_start = praty_end


# =============================================================================
# VALIDATION
# =============================================================================

print("=" * 80)
print("PRATYANTARDASHA VALIDATION")
print("=" * 80)

total_praty_years = 0.0

for lord in DASHA_SEQUENCE:

    duration = (
        saturn_antar_years
        * DASHA_YEARS[lord]
        / DASHA_CYCLE
    )

    total_praty_years += duration

print()
print(
    f"Antardasha Years : "
    f"{saturn_antar_years:.10f}"
)

print(
    f"Pratyantardasha Total : "
    f"{total_praty_years:.10f}"
)

difference = abs(
    total_praty_years
    - saturn_antar_years
)

print(
    f"Difference : "
    f"{difference:.12f}"
)

if difference < 0.00000001:
    print()
    print(
        "✓ PRATYANTARDASHA TOTAL "
        "MATCHES ANTARDASHA"
    )
else:
    print()
    print(
        "✗ PRATYANTARDASHA TOTAL "
        "DOES NOT MATCH"
    )


# =============================================================================
# COMPLETE
# =============================================================================

print()
print("=" * 80)
print("THARUMAGA PRATYANTARDASHA CALCULATION COMPLETE")
print("=" * 80)

print()
print("✓ Moon longitude calculated")
print("✓ Moon Nakshatra identified")
print("✓ Birth Mahadasha identified")
print("✓ Mercury Mahadasha identified")
print("✓ Mercury / Saturn Antardasha identified")
print("✓ 9 Pratyantardashas calculated")
print("✓ Pratyantardasha dates generated")
print("✓ Total duration validated")

print()
print("Next module: Dasha Engine Integration")
print("=" * 80)