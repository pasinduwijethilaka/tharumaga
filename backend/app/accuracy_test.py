import swisseph as swe
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# =============================================================================
# THARUMAGA - ACCURACY TEST SUITE v1
# =============================================================================

print("=" * 80)
print("THARUMAGA - ACCURACY TEST SUITE v1")
print("=" * 80)

# =============================================================================
# TEST BIRTH DATA
# =============================================================================

DAY = 15
MONTH = 5
YEAR = 1995

HOUR = 10
MINUTE = 30
SECOND = 0

TIMEZONE = "Asia/Colombo"

LATITUDE = 6.9271
LONGITUDE = 79.8612

# =============================================================================
# SETTINGS
# =============================================================================

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
DAYS_PER_YEAR = 365.2425

PASS_COUNT = 0
FAIL_COUNT = 0


# =============================================================================
# TEST HELPERS
# =============================================================================

def test(name, condition, details=""):
    global PASS_COUNT, FAIL_COUNT

    if condition:
        PASS_COUNT += 1
        print(f"✓ PASS  {name}")

        if details:
            print(f"        {details}")

    else:
        FAIL_COUNT += 1
        print(f"✗ FAIL  {name}")

        if details:
            print(f"        {details}")


def normalize_degree(value):
    return value % 360.0


def get_sign(longitude):
    index = int(normalize_degree(longitude) / 30.0)

    if index >= 12:
        index = 11

    return SIGNS[index]


def get_sign_index(longitude):
    return int(normalize_degree(longitude) / 30.0)


def get_nakshatra(longitude):
    longitude = normalize_degree(longitude)

    index = int(longitude / NAKSHATRA_SIZE)

    if index >= 27:
        index = 26

    name, lord = NAKSHATRAS[index]

    position = longitude - (index * NAKSHATRA_SIZE)

    pada = int(
        position / (NAKSHATRA_SIZE / 4.0)
    ) + 1

    if pada > 4:
        pada = 4

    return (
        name,
        lord,
        pada,
        position,
    )


def get_whole_sign_house(
    lagna_sign_index,
    planet_sign_index,
):
    return (
        (planet_sign_index - lagna_sign_index) % 12
    ) + 1


def add_years(start_date, years):
    return start_date + timedelta(
        days=years * DAYS_PER_YEAR
    )


# =============================================================================
# LOCAL TIME -> UTC
# =============================================================================

print()
print("1. TIME CONVERSION")
print("-" * 25)

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

print(
    f"Local : "
    f"{local_birth.strftime('%d/%m/%Y %H:%M:%S %z')}"
)

print(
    f"UTC   : "
    f"{utc_birth.strftime('%d/%m/%Y %H:%M:%S UTC')}"
)

test(
    "Local → UTC conversion",
    utc_birth.hour == 5
    and utc_birth.minute == 0,
    f"UTC = {utc_birth.strftime('%d/%m/%Y %H:%M:%S')}",
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

print()
print(
    "Julian Day UT : "
    f"{jd_ut:.8f}"
)

test(
    "Julian Day generated",
    jd_ut > 0,
    f"JD = {jd_ut:.8f}",
)


# =============================================================================
# SWISS EPHEMERIS
# =============================================================================

print()
print("2. SWISS EPHEMERIS")
print("-" * 25)

swe.set_sid_mode(
    swe.SIDM_LAHIRI
)

flags = (
    swe.FLG_SWIEPH
    | swe.FLG_SIDEREAL
    | swe.FLG_SPEED
)

planet_ids = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
}

positions = {}

for name, planet_id in planet_ids.items():

    data, ret_flags = swe.calc_ut(
        jd_ut,
        planet_id,
        flags,
    )

    longitude = normalize_degree(
        data[0]
    )

    speed = data[3]

    positions[name] = {
        "longitude": longitude,
        "speed": speed,
    }

    print(
        f"{name:8} : "
        f"{longitude:12.8f}° | "
        f"{get_sign(longitude):12} | "
        f"Speed {speed: .8f}"
    )

    test(
        f"{name} longitude range",
        0.0 <= longitude < 360.0,
        f"{longitude:.8f}°",
    )


# =============================================================================
# RAHU / KETU
# =============================================================================

print()
print("3. RAHU / KETU")
print("-" * 25)

rahu_data, rahu_flags = swe.calc_ut(
    jd_ut,
    swe.TRUE_NODE,
    flags,
)

rahu_longitude = normalize_degree(
    rahu_data[0]
)

ketu_longitude = normalize_degree(
    rahu_longitude + 180.0
)

print(
    f"Rahu : "
    f"{rahu_longitude:.8f}° | "
    f"{get_sign(rahu_longitude)}"
)

print(
    f"Ketu : "
    f"{ketu_longitude:.8f}° | "
    f"{get_sign(ketu_longitude)}"
)

test(
    "Rahu longitude range",
    0 <= rahu_longitude < 360,
    f"{rahu_longitude:.8f}°",
)

test(
    "Ketu longitude range",
    0 <= ketu_longitude < 360,
    f"{ketu_longitude:.8f}°",
)

opposite_difference = (
    ketu_longitude - rahu_longitude
) % 360

test(
    "Rahu/Ketu 180° opposition",
    abs(
        opposite_difference - 180.0
    ) < 0.000001,
    f"Difference = "
    f"{opposite_difference:.8f}°",
)


# =============================================================================
# LAGNA
# =============================================================================

print()
print("4. LAGNA")
print("-" * 25)

cusps, ascmc = swe.houses_ex(
    jd_ut,
    LATITUDE,
    LONGITUDE,
    b"P",
    swe.FLG_SIDEREAL,
)

lagna_longitude = normalize_degree(
    ascmc[0]
)

lagna_sign_index = get_sign_index(
    lagna_longitude
)

lagna_sign = get_sign(
    lagna_longitude
)

print(
    f"Lagna Longitude : "
    f"{lagna_longitude:.8f}°"
)

print(
    f"Lagna Sign      : "
    f"{lagna_sign}"
)

test(
    "Lagna longitude range",
    0 <= lagna_longitude < 360,
    f"{lagna_longitude:.8f}°",
)

test(
    "Lagna sign identified",
    lagna_sign in SIGNS,
    lagna_sign,
)


# =============================================================================
# NAKSHATRA TESTS
# =============================================================================

print()
print("5. NAKSHATRA")
print("-" * 25)

moon_longitude = positions[
    "Moon"
]["longitude"]

(
    moon_nakshatra,
    moon_lord,
    moon_pada,
    moon_position,
) = get_nakshatra(
    moon_longitude
)

print(
    f"Moon Longitude : "
    f"{moon_longitude:.8f}°"
)

print(
    f"Nakshatra      : "
    f"{moon_nakshatra}"
)

print(
    f"Lord           : "
    f"{moon_lord}"
)

print(
    f"Pada           : "
    f"{moon_pada}"
)

test(
    "Moon Nakshatra identified",
    moon_nakshatra == "Anuradha",
    moon_nakshatra,
)

test(
    "Moon Nakshatra Lord",
    moon_lord == "Saturn",
    moon_lord,
)

test(
    "Moon Nakshatra Pada",
    moon_pada == 1,
    f"Pada = {moon_pada}",
)

test(
    "Nakshatra Pada range",
    1 <= moon_pada <= 4,
    f"Pada = {moon_pada}",
)


# =============================================================================
# WHOLE SIGN HOUSE TEST
# =============================================================================

print()
print("6. WHOLE SIGN D1 HOUSE TEST")
print("-" * 30)

print(
    f"Lagna Sign : "
    f"{lagna_sign}"
)

for name, data in positions.items():

    planet_longitude = data[
        "longitude"
    ]

    planet_sign_index = get_sign_index(
        planet_longitude
    )

    house = get_whole_sign_house(
        lagna_sign_index,
        planet_sign_index,
    )

    print(
        f"{name:8} : "
        f"{get_sign(planet_longitude):12} "
        f"→ House {house}"
    )

    test(
        f"{name} house range",
        1 <= house <= 12,
        f"House = {house}",
    )


# =============================================================================
# RAHU / KETU HOUSES
# =============================================================================

rahu_house = get_whole_sign_house(
    lagna_sign_index,
    get_sign_index(
        rahu_longitude
    ),
)

ketu_house = get_whole_sign_house(
    lagna_sign_index,
    get_sign_index(
        ketu_longitude
    ),
)

print(
    f"{'Rahu':8} : "
    f"{get_sign(rahu_longitude):12} "
    f"→ House {rahu_house}"
)

print(
    f"{'Ketu':8} : "
    f"{get_sign(ketu_longitude):12} "
    f"→ House {ketu_house}"
)

test(
    "Rahu house range",
    1 <= rahu_house <= 12,
    f"House = {rahu_house}",
)

test(
    "Ketu house range",
    1 <= ketu_house <= 12,
    f"House = {ketu_house}",
)


# =============================================================================
# VIMSHOTTARI DASHA TEST
# =============================================================================

print()
print("7. VIMSHOTTARI DASHA TEST")
print("-" * 30)

birth_mahadasha = moon_lord

birth_mahadasha_years = DASHA_YEARS[
    birth_mahadasha
]

completed_fraction = (
    moon_position
    / NAKSHATRA_SIZE
)

remaining_fraction = (
    1.0 - completed_fraction
)

remaining_years = (
    birth_mahadasha_years
    * remaining_fraction
)

print(
    f"Birth Mahadasha : "
    f"{birth_mahadasha}"
)

print(
    f"Full Years      : "
    f"{birth_mahadasha_years}"
)

print(
    f"Remaining Years : "
    f"{remaining_years:.8f}"
)

test(
    "Birth Mahadasha identified",
    birth_mahadasha == "Saturn",
    birth_mahadasha,
)

test(
    "Dasha lord exists",
    birth_mahadasha in DASHA_YEARS,
    birth_mahadasha,
)

test(
    "Remaining years valid",
    0 < remaining_years
    <= birth_mahadasha_years,
    f"{remaining_years:.8f}",
)


# =============================================================================
# ANTARDASHA FORMULA TEST
# =============================================================================

print()
print("8. ANTARDASHA FORMULA TEST")
print("-" * 30)

mercury_years = DASHA_YEARS[
    "Mercury"
]

expected_total = 0.0

for lord in DASHA_SEQUENCE:

    duration = (
        mercury_years
        * DASHA_YEARS[lord]
        / 120.0
    )

    expected_total += duration

    print(
        f"Mercury / {lord:8} : "
        f"{duration:.8f} years"
    )

test(
    "Antardasha total = Mahadasha",
    abs(
        expected_total
        - mercury_years
    ) < 0.00000001,
    f"Total = {expected_total:.8f} years",
)


# =============================================================================
# CORE EXPECTED VALUE TESTS
# =============================================================================

print()
print("9. CORE EXPECTED VALUE TESTS")
print("-" * 30)

# Moon
test(
    "Expected Moon longitude",
    abs(
        moon_longitude
        - 214.96032285
    ) < 0.0001,
    f"Actual = "
    f"{moon_longitude:.8f}°",
)

# Rahu
test(
    "Expected Rahu longitude",
    abs(
        rahu_longitude
        - 191.77625229
    ) < 0.001,
    f"Actual = "
    f"{rahu_longitude:.8f}°",
)

# Ketu
test(
    "Expected Ketu longitude",
    abs(
        ketu_longitude
        - 11.77625229
    ) < 0.001,
    f"Actual = "
    f"{ketu_longitude:.8f}°",
)

# Lagna
test(
    "Expected Lagna sign",
    lagna_sign == "Cancer",
    f"Actual = "
    f"{lagna_sign}",
)


# =============================================================================
# FINAL RESULT
# =============================================================================

print()
print("=" * 80)
print("ACCURACY TEST RESULT")
print("=" * 80)

total_tests = (
    PASS_COUNT
    + FAIL_COUNT
)

print()
print(
    f"Total Tests : "
    f"{total_tests}"
)

print(
    f"Passed      : "
    f"{PASS_COUNT}"
)

print(
    f"Failed      : "
    f"{FAIL_COUNT}"
)

if FAIL_COUNT == 0:

    print()
    print("✓ ALL TESTS PASSED")
    print()
    print(
        "TharuMaga calculation foundation "
        "is internally consistent."
    )

else:

    print()
    print("⚠ SOME TESTS FAILED")
    print()
    print(
        "Review the failed tests "
        "before continuing."
    )

print()
print("=" * 80)
print("THARUMAGA ACCURACY TEST COMPLETE")
print("=" * 80)