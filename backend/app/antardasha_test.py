import swisseph as swe
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# =============================================================================
# THARUMAGA - ANTARDASHA / BHUKTI ENGINE v1
# =============================================================================

print("=" * 80)
print("THARUMAGA - ANTARDASHA / BHUKTI ENGINE")
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

DASHA_CYCLE = 120

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
DAYS_PER_YEAR = 365.2425


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def normalize_degree(value):
    return value % 360.0


def get_nakshatra(longitude):
    longitude = normalize_degree(longitude)

    nakshatra_index = int(longitude / NAKSHATRA_SIZE)

    if nakshatra_index >= 27:
        nakshatra_index = 26

    nakshatra_name, lord = NAKSHATRAS[nakshatra_index]

    position_in_nakshatra = (
        longitude - (nakshatra_index * NAKSHATRA_SIZE)
    )

    completed_percent = (
        position_in_nakshatra / NAKSHATRA_SIZE
    ) * 100.0

    remaining_percent = 100.0 - completed_percent

    return (
        nakshatra_name,
        lord,
        position_in_nakshatra,
        completed_percent,
        remaining_percent,
    )


def get_dasha_start_index(lord):
    return DASHA_SEQUENCE.index(lord)


def add_dasha_years(start_date, years):
    days = years * DAYS_PER_YEAR
    return start_date + timedelta(days=days)


def format_date(date_value):
    return date_value.strftime("%d/%m/%Y")


# =============================================================================
# LOCAL TIME -> UTC
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

utc_birth = local_birth.astimezone(ZoneInfo("UTC"))

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
print(f"Birth Place      : {PLACE}")


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

swe.set_sid_mode(swe.SIDM_LAHIRI)

flags = (
    swe.FLG_SWIEPH
    | swe.FLG_SIDEREAL
    | swe.FLG_SPEED
)

moon_data, moon_flags = swe.calc_ut(
    jd_ut,
    swe.MOON,
    flags,
)

moon_longitude = normalize_degree(moon_data[0])


# =============================================================================
# MOON NAKSHATRA
# =============================================================================

(
    nakshatra_name,
    nakshatra_lord,
    position_in_nakshatra,
    completed_percent,
    remaining_percent,
) = get_nakshatra(moon_longitude)

print()
print("=" * 80)
print("MOON NAKSHATRA")
print("=" * 80)

print(f"Moon Longitude       : {moon_longitude:.8f}°")
print(f"Nakshatra            : {nakshatra_name}")
print(f"Nakshatra Lord       : {nakshatra_lord}")
print(f"Position in Nakshatra: {position_in_nakshatra:.8f}°")
print(f"Completed            : {completed_percent:.8f}%")
print(f"Remaining            : {remaining_percent:.8f}%")


# =============================================================================
# BIRTH MAHADASHA
# =============================================================================

birth_mahadasha_lord = nakshatra_lord
birth_mahadasha_years = DASHA_YEARS[birth_mahadasha_lord]

elapsed_fraction = completed_percent / 100.0

elapsed_years = birth_mahadasha_years * elapsed_fraction
remaining_years = birth_mahadasha_years - elapsed_years

remaining_days = remaining_years * DAYS_PER_YEAR

birth_mahadasha_end = (
    local_birth.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    + timedelta(days=remaining_days)
)

print()
print("=" * 80)
print("BIRTH MAHADASHA")
print("=" * 80)

print(f"Mahadasha Lord       : {birth_mahadasha_lord}")
print(f"Full Mahadasha       : {birth_mahadasha_years} years")
print(f"Elapsed              : {elapsed_years:.8f} years")
print(f"Remaining            : {remaining_years:.8f} years")
print(f"Remaining Days       : {remaining_days:.4f}")
print(
    f"Mahadasha End        : "
    f"{format_date(birth_mahadasha_end)}"
)


# =============================================================================
# FIND MERCURY MAHADASHA
# =============================================================================

current_start = local_birth.replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
)

start_index = get_dasha_start_index(birth_mahadasha_lord)

# First Mahadasha
if birth_mahadasha_lord == "Mercury":
    mercury_start = current_start
    mercury_end = birth_mahadasha_end

else:
    current_start = birth_mahadasha_end

    for i in range(1, 10):

        lord_index = (start_index + i) % len(DASHA_SEQUENCE)

        lord = DASHA_SEQUENCE[lord_index]

        duration_years = DASHA_YEARS[lord]

        current_end = add_dasha_years(
            current_start,
            duration_years,
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

print(f"Start : {format_date(mercury_start)}")
print(f"End   : {format_date(mercury_end)}")
print(f"Years : {DASHA_YEARS['Mercury']}")


# =============================================================================
# ANTARDASHA CALCULATION
# =============================================================================

print()
print("=" * 80)
print("MERCURY MAHADASHA - ANTARDASHA / BHUKTI")
print("=" * 80)

print()

antardasha_start_index = get_dasha_start_index("Mercury")

ad_start = mercury_start

for i in range(9):

    antardasha_index = (
        antardasha_start_index + i
    ) % len(DASHA_SEQUENCE)

    antardasha_lord = DASHA_SEQUENCE[antardasha_index]

    maha_years = DASHA_YEARS["Mercury"]
    antar_years = DASHA_YEARS[antardasha_lord]

    # Vimshottari Antardasha formula
    antar_duration_years = (
        maha_years
        * antar_years
        / DASHA_CYCLE
    )

    antar_duration_days = (
        antar_duration_years
        * DAYS_PER_YEAR
    )

    ad_end = ad_start + timedelta(
        days=antar_duration_days
    )

    print(
        f"{i + 1:2}. Mercury / {antardasha_lord}"
    )
    print(
        f"    Start : {format_date(ad_start)}"
    )
    print(
        f"    End   : {format_date(ad_end)}"
    )
    print(
        f"    Years : {antar_duration_years:.8f}"
    )
    print(
        f"    Days  : {antar_duration_days:.4f}"
    )
    print()

    ad_start = ad_end


# =============================================================================
# COMPLETE
# =============================================================================

print("=" * 80)
print("THARUMAGA ANTARDASHA CALCULATION COMPLETE")
print("=" * 80)

print()
print("✓ Moon longitude calculated")
print("✓ Moon Nakshatra identified")
print("✓ Birth Mahadasha identified")
print("✓ Mercury Mahadasha identified")
print("✓ 9 Antardashas calculated")
print("✓ Antardasha dates generated")
print()
print("Next module: Pratyantardasha / Sookshma Dasha")
print("=" * 80)