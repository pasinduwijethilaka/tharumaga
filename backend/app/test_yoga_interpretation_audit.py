from .yoga_interpretation_engine import TharuMagaYogaInterpretationEngine


def make_yoga(yoga_id, name="Test Yoga"):
    return {
        "id": yoga_id,
        "name": name,
        "category": "Test",
        "status": "detected",
        "planets": ["Moon", "Jupiter"],
        "houses": [4, 7],
        "rule": "Test structural rule.",
        "relationships": ["conjunction"],
    }


def test_all_profiles_exist():
    engine = TharuMagaYogaInterpretationEngine({})

    expected = {
        "gaja_kesari",
        "budha_aditya",
        "dharma_karmadhipati",
        "raja_yoga",
        "dhana_yoga",
        "mahapurusha_mars",
        "mahapurusha_mercury",
        "mahapurusha_jupiter",
        "mahapurusha_venus",
        "mahapurusha_saturn",
    }

    assert expected.issubset(engine.YOGA_LIBRARY.keys())


def test_gaja_kesari_wording():
    engine = TharuMagaYogaInterpretationEngine(
        {"yogas": [make_yoga("gaja_kesari")]}
    )

    card = engine.generate()["interpretations"][0]

    assert "traditionally associated" in card["summary"]
    assert card["caution"]
    assert "guarantee" not in card["summary"].lower()


def test_budha_aditya_wording():
    engine = TharuMagaYogaInterpretationEngine(
        {"yogas": [make_yoga("budha_aditya")]}
    )

    card = engine.generate()["interpretations"][0]

    assert "traditionally associated" in card["summary"]
    assert card["caution"]
    assert "guarantee" not in card["summary"].lower()


def test_dharma_karmadhipati_wording():
    engine = TharuMagaYogaInterpretationEngine(
        {"yogas": [make_yoga("dharma_karmadhipati")]}
    )

    card = engine.generate()["interpretations"][0]

    assert "Traditionally" in card["summary"]
    assert card["caution"]
    assert "guaranteed" in card["caution"].lower()


def test_raja_yoga_wording():
    engine = TharuMagaYogaInterpretationEngine(
        {"yogas": [make_yoga("raja_yoga")]}
    )

    card = engine.generate()["interpretations"][0]

    assert "traditional Jyotisha" in card["summary"]
    assert card["caution"]
    assert "promise" in card["caution"].lower()


def test_dhana_yoga_wording():
    engine = TharuMagaYogaInterpretationEngine(
        {"yogas": [make_yoga("dhana_yoga")]}
    )

    card = engine.generate()["interpretations"][0]

    assert "traditionally connected" in card["summary"]
    assert card["caution"]
    assert "guarantee" in card["caution"].lower()


def test_mahapurusha_profiles_have_caution():
    engine = TharuMagaYogaInterpretationEngine({})

    ids = [
        "mahapurusha_mars",
        "mahapurusha_mercury",
        "mahapurusha_jupiter",
        "mahapurusha_venus",
        "mahapurusha_saturn",
    ]

    for yoga_id in ids:
        card = engine._build_card(make_yoga(yoga_id))

        assert card["category"] == "Pancha Mahapurusha"
        assert "structural indication" in card["caution"].lower()
        assert "wider chart" in card["caution"].lower()


def test_relationship_text():
    engine = TharuMagaYogaInterpretationEngine({})

    yoga = make_yoga("raja_yoga")
    yoga["relationships"] = [
        "same_lord",
        "conjunction",
        "mutual_aspect",
        "sign_exchange",
    ]

    card = engine._build_card(yoga)

    text = card["relationship_summary"]

    assert "same planetary lord" in text
    assert "conjunction in the same house" in text
    assert "mutual planetary aspect" in text
    assert "sign exchange" in text


def test_unknown_yoga_is_safe():
    engine = TharuMagaYogaInterpretationEngine(
        {"yogas": [make_yoga("unknown_yoga", "Unknown Yoga")]}
    )

    card = engine.generate()["interpretations"][0]

    assert card["title"] == "Unknown Yoga"
    assert card["status"] == "detected"
    assert card["caution"]
    assert "limited" in card["caution"].lower()


def test_empty_input():
    engine = TharuMagaYogaInterpretationEngine({})

    result = engine.generate()

    assert result["count"] == 0
    assert result["interpretations"] == []


def run_all():
    tests = [
        test_all_profiles_exist,
        test_gaja_kesari_wording,
        test_budha_aditya_wording,
        test_dharma_karmadhipati_wording,
        test_raja_yoga_wording,
        test_dhana_yoga_wording,
        test_mahapurusha_profiles_have_caution,
        test_relationship_text,
        test_unknown_yoga_is_safe,
        test_empty_input,
    ]

    print("=" * 68)
    print("THARUMAGA YOGA INTERPRETATION DEEP AUDIT")
    print("=" * 68)

    for test in tests:
        test()
        print(f"PASS : {test.__name__}")

    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} audit tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()