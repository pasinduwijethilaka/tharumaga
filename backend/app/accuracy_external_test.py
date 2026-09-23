from astrology_engine import TharuMagaEngine


print("=" * 80)
print("THARUMAGA EXTERNAL ACCURACY VALIDATION")
print("=" * 80)


# ============================================================
# TEST BIRTH DATA
# ============================================================

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
    place="Colombo, Sri Lanka"
)


# ============================================================
# CALCULATE
# ============================================================

result = engine.calculate()


# ============================================================
# BIRTH DATA
# ============================================================

print("\nBIRTH DATA")
print("-" * 80)

birth = result["birth"]

print("Date       :", birth["date"])
print("Local Time :", birth["local_time"])
print("Timezone   :", birth["timezone"])
print("UTC        :", birth["utc"])
print("Julian Day :", birth["julian_day_ut"])


# ============================================================
# LAGNA
# ============================================================

print("\nLAGNA")
print("-" * 80)

lagna = result["lagna"]

print("Longitude  :", lagna["longitude"])
print("Sign       :", lagna["sign"])
print("Nakshatra  :", lagna["nakshatra"])


# ============================================================
# PLANETS
# ============================================================

print("\nPLANETS")
print("-" * 80)

for name, planet in result["planets"].items():

    print(
        f"{name:<10} "
        f"{planet['longitude']:>15.8f}°  "
        f"{planet['sign']}"
    )


# ============================================================
# RAHU
# ============================================================

print("\nRAHU")
print("-" * 80)

rahu = result["rahu"]

print("Longitude  :", rahu["longitude"])
print("Sign       :", rahu["sign"])
print("Retrograde :", rahu["retrograde"])
print("Nakshatra  :", rahu["nakshatra"])


# ============================================================
# KETU
# ============================================================

print("\nKETU")
print("-" * 80)

ketu = result["ketu"]

print("Longitude  :", ketu["longitude"])
print("Sign       :", ketu["sign"])
print("Retrograde :", ketu["retrograde"])
print("Nakshatra  :", ketu["nakshatra"])


# ============================================================
# RAHU / KETU DIFFERENCE
# ============================================================

print("\nRAHU / KETU AXIS")
print("-" * 80)

difference = (
    ketu["longitude"] -
    rahu["longitude"]
) % 360

print("Difference :", difference)
print("Expected   : 180.00000000°")


# ============================================================
# MOON NAKSHATRA
# ============================================================

print("\nMOON NAKSHATRA")
print("-" * 80)

moon_nakshatra = result["moon_nakshatra"]

print("Name       :", moon_nakshatra["name"])
print("Lord       :", moon_nakshatra["lord"])
print("Pada       :", moon_nakshatra["pada"])
print(
    "Position   :",
    moon_nakshatra["position_degrees"]
)


# ============================================================
# BIRTH MAHADASHA
# ============================================================

print("\nBIRTH MAHADASHA")
print("-" * 80)

birth_dasha = result["birth_mahadasha"]

print("Lord       :", birth_dasha["lord"])
print("Full Years :", birth_dasha["full_years"])
print(
    "Remaining  :",
    birth_dasha["remaining_years"]
)
print("Start      :", birth_dasha["start"])
print("End        :", birth_dasha["end"])


# ============================================================
# MAHADASHA
# ============================================================

print("\nVIMSHOTTARI MAHADASHA")
print("-" * 80)

for dasha in result["dasha"]:

    print(
        f"{dasha['lord']:<10} "
        f"{dasha['start']} → {dasha['end']} "
        f"({dasha['years']} years)"
    )


# ============================================================
# FINAL
# ============================================================

print("\n")
print("=" * 80)
print("EXTERNAL VALIDATION DATA READY")
print("=" * 80)
print()
print("Use the above values to compare against")
print("an independent Swiss Ephemeris / astrology reference.")
print()
print("IMPORTANT:")
print("Do not change astrology_engine.py based on a random")
print("website result. First compare the calculation settings.")
print("=" * 80)