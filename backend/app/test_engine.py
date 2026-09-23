from astrology_engine import TharuMagaEngine


passed = 0
failed = 0


# ============================================================
# TEST HELPER
# ============================================================

def test(name, condition):
    global passed, failed

    if condition:
        print(f"✓ {name}")
        passed += 1
    else:
        print(f"✗ {name}")
        failed += 1


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 80)
    print("THARUMAGA ENGINE INTEGRATION TEST")
    print("=" * 80)

    # ========================================================
    # TEST BIRTH DATA
    # ========================================================

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

    # ========================================================
    # 1. BASIC ENGINE
    # ========================================================

    print("\n[1] BASIC ENGINE")

    test(
        "Engine initialized",
        engine is not None
    )

    test(
        "Calculation result generated",
        isinstance(result, dict)
    )

    # ========================================================
    # 2. RESULT STRUCTURE
    # ========================================================

    print("\n[2] RESULT STRUCTURE")

    expected_keys = [
        "engine",
        "birth",
        "lagna",
        "planets",
        "rahu",
        "ketu",
        "d1",
        "moon_nakshatra",
        "birth_mahadasha",
        "dasha"
    ]

    for key in expected_keys:

        test(
            f"'{key}' exists",
            key in result
        )

    # ========================================================
    # 3. ENGINE SETTINGS
    # ========================================================

    print("\n[3] ENGINE SETTINGS")

    engine_info = result["engine"]

    test(
        "Engine name exists",
        bool(engine_info.get("name"))
    )

    test(
        "Engine version exists",
        bool(engine_info.get("version"))
    )

    test(
        "Zodiac = Sidereal",
        engine_info.get("zodiac") == "Sidereal"
    )

    test(
        "Ayanamsa = Lahiri",
        engine_info.get("ayanamsa") == "Lahiri"
    )

    test(
        "Rahu = True Node",
        engine_info.get("rahu") == "True Node"
    )

    test(
        "Ketu setting exists",
        bool(engine_info.get("ketu"))
    )

    test(
        "House system = Whole Sign",
        engine_info.get("house_system") == "Whole Sign"
    )

    test(
        "Dasha system exists",
        bool(engine_info.get("dasha_system"))
    )

    # ========================================================
    # 4. BIRTH DATA
    # ========================================================

    print("\n[4] BIRTH DATA")

    birth = result["birth"]

    test(
        "Birth date correct",
        birth.get("date") == "1995-05-15"
    )

    test(
        "Local time correct",
        birth.get("local_time") == "10:30:00"
    )

    test(
        "Timezone correct",
        birth.get("timezone") == "Asia/Colombo"
    )

    test(
        "UTC exists",
        bool(birth.get("utc"))
    )

    test(
        "Place correct",
        birth.get("place") == "Colombo, Sri Lanka"
    )

    test(
        "Latitude correct",
        abs(
            birth.get("latitude") - 6.9271
        ) < 0.000001
    )

    test(
        "Longitude correct",
        abs(
            birth.get("longitude") - 79.8612
        ) < 0.000001
    )

    test(
        "Julian Day exists",
        birth.get("julian_day_ut") is not None
    )

    test(
        "Julian Day correct",
        abs(
            birth.get("julian_day_ut")
            - 2449852.70833333
        ) < 0.000001
    )

    # ========================================================
    # 5. LAGNA
    # ========================================================

    print("\n[5] LAGNA")

    lagna = result["lagna"]

    lagna_longitude = lagna.get("longitude")

    test(
        "Lagna longitude exists",
        lagna_longitude is not None
    )

    test(
        "Lagna longitude valid",
        lagna_longitude is not None
        and 0 <= lagna_longitude < 360
    )

    test(
        "Lagna = Cancer",
        lagna.get("sign") == "Cancer"
    )

    test(
        "Lagna sign index valid",
        lagna.get("sign_index") is not None
        and 0 <= lagna.get("sign_index") <= 11
    )

    test(
        "Lagna Nakshatra exists",
        bool(lagna.get("nakshatra"))
    )

    test(
        "Lagna longitude regression",
        lagna_longitude is not None
        and abs(
            lagna_longitude - 94.05609279
        ) < 0.00001
    )

    # ========================================================
    # 6. PLANETS
    # ========================================================

    print("\n[6] PLANETS")

    planets = result["planets"]

    required_planets = [
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn"
    ]

    for planet_name in required_planets:

        planet = planets.get(planet_name)

        test(
            f"{planet_name} exists",
            isinstance(planet, dict)
        )

        if isinstance(planet, dict):

            longitude = planet.get("longitude")

            test(
                f"{planet_name} longitude valid",
                longitude is not None
                and 0 <= longitude < 360
            )

            test(
                f"{planet_name} sign exists",
                bool(planet.get("sign"))
            )

    # ========================================================
    # 7. PLANET LONGITUDE REGRESSION
    # ========================================================

    print("\n[7] PLANET LONGITUDE REGRESSION")

    expected_planets = {
        "Sun": 30.12336003,
        "Moon": 214.96032285,
        "Mars": 121.69895641,
        "Mercury": 51.20788307,
        "Jupiter": 228.84091076,
        "Venus": 4.06639217,
        "Saturn": 328.79112801,
    }

    tolerance = 0.00001

    for planet_name, expected in expected_planets.items():

        actual = planets[planet_name]["longitude"]

        test(
            f"{planet_name} regression",
            abs(actual - expected) < tolerance
        )

    # ========================================================
    # 8. MOON
    # ========================================================

    print("\n[8] MOON")

    moon = planets["Moon"]

    test(
        "Moon = Scorpio",
        moon["sign"] == "Scorpio"
    )

    test(
        "Moon longitude valid",
        0 <= moon["longitude"] < 360
    )

    # ========================================================
    # 9. RAHU
    # ========================================================

    print("\n[9] RAHU")

    rahu = result["rahu"]

    rahu_longitude = rahu.get("longitude")

    test(
        "Rahu exists",
        isinstance(rahu, dict)
    )

    test(
        "Rahu = Libra",
        rahu.get("sign") == "Libra"
    )

    test(
        "Rahu longitude valid",
        rahu_longitude is not None
        and 0 <= rahu_longitude < 360
    )

    test(
        "Rahu longitude regression",
        rahu_longitude is not None
        and abs(
            rahu_longitude - 191.77625229
        ) < tolerance
    )

    test(
        "Rahu retrograde exists",
        rahu.get("retrograde") is not None
    )

    test(
        "Rahu Nakshatra exists",
        bool(rahu.get("nakshatra"))
    )

    # ========================================================
    # 10. KETU
    # ========================================================

    print("\n[10] KETU")

    ketu = result["ketu"]

    ketu_longitude = ketu.get("longitude")

    test(
        "Ketu exists",
        isinstance(ketu, dict)
    )

    test(
        "Ketu = Aries",
        ketu.get("sign") == "Aries"
    )

    test(
        "Ketu longitude valid",
        ketu_longitude is not None
        and 0 <= ketu_longitude < 360
    )

    test(
        "Ketu longitude regression",
        ketu_longitude is not None
        and abs(
            ketu_longitude - 11.77625229
        ) < tolerance
    )

    # ========================================================
    # 11. RAHU / KETU AXIS
    # ========================================================

    print("\n[11] RAHU / KETU AXIS")

    difference = (
        ketu_longitude -
        rahu_longitude
    ) % 360

    test(
        "Rahu/Ketu exactly 180° apart",
        abs(difference - 180) < 0.000001
    )

    # ========================================================
    # 12. D1 RASI
    # ========================================================

    print("\n[12] D1 RASI")

    d1 = result["d1"]

    test(
        "D1 exists",
        isinstance(d1, dict)
    )

    test(
        "D1 house system = Whole Sign",
        d1.get("house_system") == "Whole Sign"
    )

    test(
        "D1 Lagna sign = Cancer",
        d1.get("lagna_sign") == "Cancer"
    )

    test(
        "D1 Lagna sign index valid",
        d1.get("lagna_sign_index") is not None
        and 0 <= d1.get("lagna_sign_index") <= 11
    )

    # ========================================================
    # 13. MOON NAKSHATRA
    # ========================================================

    print("\n[13] MOON NAKSHATRA")

    nakshatra = result["moon_nakshatra"]

    test(
        "Nakshatra exists",
        bool(nakshatra.get("name"))
    )

    test(
        "Nakshatra = Anuradha",
        nakshatra.get("name") == "Anuradha"
    )

    test(
        "Nakshatra Lord = Saturn",
        nakshatra.get("lord") == "Saturn"
    )

    test(
        "Pada = 1",
        nakshatra.get("pada") == 1
    )

    test(
        "Position degrees exists",
        nakshatra.get("position_degrees") is not None
    )

    test(
        "Completed percent exists",
        nakshatra.get("completed_percent") is not None
    )

    test(
        "Remaining percent exists",
        nakshatra.get("remaining_percent") is not None
    )

    test(
        "Completed fraction exists",
        nakshatra.get("completed_fraction") is not None
    )

    test(
        "Remaining fraction exists",
        nakshatra.get("remaining_fraction") is not None
    )

    # ========================================================
    # 14. BIRTH MAHADASHA
    # ========================================================

    print("\n[14] BIRTH MAHADASHA")

    birth_dasha = result["birth_mahadasha"]

    test(
        "Birth Dasha = Saturn",
        birth_dasha.get("lord") == "Saturn"
    )

    test(
        "Full years = 19",
        birth_dasha.get("full_years") == 19
    )

    test(
        "Remaining years valid",
        birth_dasha.get("remaining_years") is not None
        and birth_dasha.get("remaining_years") > 0
    )

    test(
        "Birth Dasha start correct",
        birth_dasha.get("start") == "1995-05-15"
    )

    test(
        "Birth Dasha end correct",
        birth_dasha.get("end") == "2012-01-18"
    )

    # ========================================================
    # 15. VIMSHOTTARI DASHA
    # ========================================================

    print("\n[15] VIMSHOTTARI DASHA")

    dasha = result["dasha"]

    test(
        "Dasha is a list",
        isinstance(dasha, list)
    )

    test(
        "9 Mahadashas generated",
        len(dasha) == 9
    )

    # ========================================================
    # 16. MAHADASHA ORDER
    # ========================================================

    print("\n[16] MAHADASHA ORDER")

    expected_order = [
        "Saturn",
        "Mercury",
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter"
    ]

    actual_order = [
        item["lord"]
        for item in dasha
    ]

    test(
        "Mahadasha order correct",
        actual_order == expected_order
    )

    # ========================================================
    # 17. MAHADASHA DATA STRUCTURE
    # ========================================================

    print("\n[17] MAHADASHA STRUCTURE")

    for item in dasha:

        test(
            f"{item['lord']} start exists",
            bool(item.get("start"))
        )

        test(
            f"{item['lord']} end exists",
            bool(item.get("end"))
        )

        test(
            f"{item['lord']} years exists",
            item.get("years") is not None
        )

        test(
            f"{item['lord']} Antardasha exists",
            isinstance(
                item.get("antardasha"),
                list
            )
        )

    # ========================================================
    # 18. MERCURY MAHADASHA
    # ========================================================

    print("\n[18] MERCURY MAHADASHA")

    mercury_md = next(
        item
        for item in dasha
        if item["lord"] == "Mercury"
    )

    test(
        "Mercury Mahadasha exists",
        mercury_md is not None
    )

    test(
        "Mercury Mahadasha starts 2012-01-18",
        mercury_md["start"] == "2012-01-18"
    )

    test(
        "Mercury Mahadasha ends 2029-01-17",
        mercury_md["end"] == "2029-01-17"
    )

    test(
        "Mercury Mahadasha = 17 years",
        mercury_md["years"] == 17
    )

    # ========================================================
    # 19. ANTARDASHA
    # ========================================================

    print("\n[19] ANTARDASHA")

    antardashas = mercury_md["antardasha"]

    test(
        "Mercury Antardasha list exists",
        isinstance(antardashas, list)
    )

    test(
        "9 Mercury Antardashas",
        len(antardashas) == 9
    )

    expected_ad_order = [
        "Mercury",
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn"
    ]

    actual_ad_order = [
        item["lord"]
        for item in antardashas
    ]

    test(
        "Mercury Antardasha order correct",
        actual_ad_order == expected_ad_order
    )

    # ========================================================
    # 20. ANTARDASHA STRUCTURE
    # ========================================================

    print("\n[20] ANTARDASHA STRUCTURE")

    for item in antardashas:

        test(
            f"Mercury/{item['lord']} start exists",
            bool(item.get("start"))
        )

        test(
            f"Mercury/{item['lord']} end exists",
            bool(item.get("end"))
        )

        test(
            f"Mercury/{item['lord']} years exists",
            item.get("years") is not None
        )

        test(
            f"Mercury/{item['lord']} Pratyantardasha exists",
            isinstance(
                item.get("pratyantardasha"),
                list
            )
        )

    # ========================================================
    # 21. MERCURY / SATURN
    # ========================================================

    print("\n[21] MERCURY / SATURN")

    mercury_saturn = next(
        item
        for item in antardashas
        if item["lord"] == "Saturn"
    )

    test(
        "Mercury/Saturn exists",
        mercury_saturn is not None
    )

    test(
        "Mercury/Saturn starts 2026-05-10",
        mercury_saturn["start"] == "2026-05-10"
    )

    test(
        "Mercury/Saturn ends 2029-01-17",
        mercury_saturn["end"] == "2029-01-17"
    )

    test(
        "Mercury/Saturn years valid",
        mercury_saturn["years"] > 0
    )

    # ========================================================
    # 22. PRATYANTARDASHA
    # ========================================================

    print("\n[22] PRATYANTARDASHA")

    pratyantar = mercury_saturn["pratyantardasha"]

    test(
        "Pratyantardasha list exists",
        isinstance(pratyantar, list)
    )

    test(
        "9 Pratyantardashas generated",
        len(pratyantar) == 9
    )

    expected_pd_order = [
        "Saturn",
        "Mercury",
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter"
    ]

    actual_pd_order = [
        item["lord"]
        for item in pratyantar
    ]

    test(
        "Pratyantardasha order correct",
        actual_pd_order == expected_pd_order
    )

    # ========================================================
    # 23. PRATYANTARDASHA STRUCTURE
    # ========================================================

    print("\n[23] PRATYANTARDASHA STRUCTURE")

    for item in pratyantar:

        test(
            f"Mercury/Saturn/{item['lord']} start exists",
            bool(item.get("start"))
        )

        test(
            f"Mercury/Saturn/{item['lord']} end exists",
            bool(item.get("end"))
        )

        test(
            f"Mercury/Saturn/{item['lord']} years exists",
            item.get("years") is not None
        )

        test(
            f"Mahadasha field correct for {item['lord']}",
            item.get("mahadasha") == "Mercury"
        )

        test(
            f"Antardasha field correct for {item['lord']}",
            item.get("antardasha") == "Saturn"
        )

    # ========================================================
    # 24. CURRENT TEST PERIOD
    # ========================================================

    print("\n[24] CURRENT TEST PERIOD")

    first_pd = pratyantar[0]

    test(
        "Mercury/Saturn/Saturn starts 2026-05-10",
        first_pd["start"] == "2026-05-10"
    )

    test(
        "Mercury/Saturn/Saturn ends 2026-10-13",
        first_pd["end"] == "2026-10-13"
    )

    # ========================================================
    # 25. PRATYANTARDASHA TOTAL
    # ========================================================

    print("\n[25] DASHA DURATION CONSISTENCY")

    pd_total = sum(
        item["years"]
        for item in pratyantar
    )

    ad_years = mercury_saturn["years"]

    test(
        "Pratyantardasha total = Antardasha",
        abs(pd_total - ad_years) < 0.000000001
    )

    # ========================================================
    # 26. MAHADASHA / ANTARDASHA TOTAL
    # ========================================================

    print("\n[26] MAHADASHA / ANTARDASHA CONSISTENCY")

    for md in dasha:

        ad_total = sum(
            ad["years"]
            for ad in md["antardasha"]
        )

        # Birth Mahadasha is a partial Mahadasha.
        # Full Mahadashas should equal their declared years.
        if md["lord"] != birth_dasha["lord"]:

            test(
                f"{md['lord']} AD total = MD years",
                abs(
                    ad_total - md["years"]
                ) < 0.000000001
            )

    # ========================================================
    # 27. DATE CONTINUITY
    # ========================================================

    print("\n[27] DASHA DATE CONTINUITY")

    for index in range(len(dasha) - 1):

        current = dasha[index]
        next_md = dasha[index + 1]

        test(
            f"{current['lord']} → {next_md['lord']} date continuity",
            current["end"] == next_md["start"]
        )

    # ========================================================
    # 28. ANTARDASHA DATE CONTINUITY
    # ========================================================

    print("\n[28] ANTARDASHA DATE CONTINUITY")

    for index in range(len(antardashas) - 1):

        current = antardashas[index]
        next_ad = antardashas[index + 1]

        test(
            f"AD {current['lord']} → {next_ad['lord']} continuity",
            current["end"] == next_ad["start"]
        )

    # ========================================================
    # 29. PRATYANTARDASHA DATE CONTINUITY
    # ========================================================

    print("\n[29] PRATYANTARDASHA DATE CONTINUITY")

    for index in range(len(pratyantar) - 1):

        current = pratyantar[index]
        next_pd = pratyantar[index + 1]

        test(
            f"PD {current['lord']} → {next_pd['lord']} continuity",
            current["end"] == next_pd["start"]
        )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n")
    print("=" * 80)
    print("FINAL TEST SUMMARY")
    print("=" * 80)

    print(f"Passed : {passed}")
    print(f"Failed : {failed}")
    print(f"Total  : {passed + failed}")

    print("=" * 80)

    if failed == 0:

        print("✓ ALL ENGINE TESTS PASSED")

    else:

        print("✗ ENGINE TESTS FAILED")

        raise AssertionError(
            f"{failed} test(s) failed"
        )

    print("=" * 80)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()