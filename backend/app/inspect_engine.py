from astrology_engine import TharuMagaEngine


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

result = engine.calculate()


print("=" * 80)
print("TOP LEVEL STRUCTURE")
print("=" * 80)

for key, value in result.items():
    print(f"{key} -> {type(value).__name__}")

    if isinstance(value, dict):
        print("  keys:", list(value.keys()))

    elif isinstance(value, list):
        print("  list length:", len(value))

        if len(value) > 0:
            print("  first item type:", type(value[0]).__name__)

            if isinstance(value[0], dict):
                print("  first item keys:", list(value[0].keys()))


print("\n")
print("=" * 80)
print("D1")
print("=" * 80)

d1 = result.get("d1")

print("Type:", type(d1).__name__)

if isinstance(d1, dict):
    print("Keys:", list(d1.keys()))

    for key, value in d1.items():
        print(f"{key} -> {type(value).__name__}")

        if isinstance(value, list):
            print("  Length:", len(value))

        elif isinstance(value, dict):
            print("  Keys:", list(value.keys()))


print("\n")
print("=" * 80)
print("BIRTH MAHADASHA")
print("=" * 80)

birth = result.get("birth_mahadasha")

print("Type:", type(birth).__name__)

if isinstance(birth, dict):
    for key, value in birth.items():
        print(f"{key} -> {value}")
else:
    print(birth)


print("\n")
print("=" * 80)
print("DASHA")
print("=" * 80)

dasha = result.get("dasha")

print("Type:", type(dasha).__name__)

if isinstance(dasha, list):

    print("Length:", len(dasha))

    for i, item in enumerate(dasha[:3]):
        print(f"\nItem {i + 1}:")
        print("Type:", type(item).__name__)

        if isinstance(item, dict):
            for key, value in item.items():
                print(f"  {key} -> {type(value).__name__}: {value}")

elif isinstance(dasha, dict):

    print("Keys:", list(dasha.keys()))

    for key, value in dasha.items():
        print(f"{key} -> {type(value).__name__}")

else:
    print(dasha)


print("\n")
print("=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)