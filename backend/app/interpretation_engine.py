class TharuMagaInterpretationEngine:
    """
    TharuMaga Vedic Astrology Interpretation Engine

    This layer converts calculated chart data into
    traditional Vedic astrology interpretations.

    Calculation is NOT performed here.
    Swiss Ephemeris remains responsible for astronomy.
    """

    # ==========================================================
    # SIGN NAMES
    # ==========================================================

    SIGN_NAMES_SI = {
        "Aries": "මේෂ",
        "Taurus": "වෘෂභ",
        "Gemini": "මිථුන",
        "Cancer": "කටක",
        "Leo": "සිංහ",
        "Virgo": "කන්‍යා",
        "Libra": "තුලා",
        "Scorpio": "වෘශ්චික",
        "Sagittarius": "ධනු",
        "Capricorn": "මකර",
        "Aquarius": "කුම්භ",
        "Pisces": "මීන",
    }

    # ==========================================================
    # PLANET NAMES
    # ==========================================================

    PLANET_NAMES_SI = {
        "Sun": "රවි",
        "Moon": "සඳු",
        "Mars": "කුජ",
        "Mercury": "බුධ",
        "Jupiter": "ගුරු",
        "Venus": "සිකුරු",
        "Saturn": "ශනි",
        "Rahu": "රාහු",
        "Ketu": "කේතු",
    }

    # ==========================================================
    # HOUSE MEANINGS
    # ==========================================================

    HOUSE_MEANINGS = {
        1: "ස්වභාවය, පෞරුෂය සහ ශරීරය",
        2: "ධනය, පවුල, කථනය සහ සම්පත්",
        3: "ධෛර්යය, සහෝදරයන්, සන්නිවේදනය සහ උත්සාහය",
        4: "නිවස, මව, අධ්‍යාපනය සහ අභ්‍යන්තර සැනසීම",
        5: "බුද්ධිය, නිර්මාණශීලීත්වය, දරුවන් සහ ආදරය",
        6: "සේවය, දෛනික වැඩ, තරඟකාරීත්වය සහ බාධක",
        7: "විවාහය, හවුල්කාරිත්වය සහ සමාජ සම්බන්ධතා",
        8: "පරිවර්තනය, ගැඹුරු කරුණු, රහස් සහ හදිසි වෙනස්කම්",
        9: "භාග්‍යය, උසස් අධ්‍යාපනය, ආගමික/දාර්ශනික කරුණු සහ දුර ගමන්",
        10: "වෘත්තිය, කීර්තිය, වගකීම් සහ සමාජ තත්ත්වය",
        11: "ලාභ, ආදායම්, මිතුරන් සහ බලාපොරොත්තු",
        12: "වියදම්, විදේශ සම්බන්ධතා, නිදහස සහ අභ්‍යන්තර ලෝකය",
    }

    # ==========================================================
    # SIGN LORDS
    # ==========================================================

    SIGN_LORDS = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter",
    }

    # ==========================================================
    # PLANET + HOUSE THEMES
    # ==========================================================

    PLANET_HOUSE_THEMES = {

        "Sun": {
            1: "නායකත්වය සහ ස්වයං විශ්වාසය කෙරෙහි අවධානයක් යොමු විය හැක.",
            2: "පවුල, ධනය සහ කථන හැකියාව සම්බන්ධ කරුණු ප්‍රමුඛ විය හැක.",
            3: "ධෛර්යය, උත්සාහය සහ සන්නිවේදනයට වැඩි වැදගත්කමක් ලැබිය හැක.",
            4: "නිවස, පවුල සහ අභ්‍යන්තර ආරක්ෂාව පිළිබඳ අවධානය වැඩි විය හැක.",
            5: "නිර්මාණශීලීත්වය, ඉගෙනීම සහ ස්වයං ප්‍රකාශනය වැදගත් විය හැක.",
            6: "සේවය, තරඟකාරීත්වය සහ දෛනික වගකීම් ප්‍රමුඛ විය හැක.",
            7: "සම්බන්ධතා සහ හවුල්කාරිත්වය තුළ තම අනන්‍යතාවය ප්‍රකාශ කිරීමට උත්සාහයක් තිබිය හැක.",
            8: "ගැඹුරු පරිවර්තන සහ ජීවිතයේ අභ්‍යන්තර පැති පිළිබඳ අවධානය යොමු විය හැක.",
            9: "දැනුම, විශ්වාසයන් සහ උසස් අධ්‍යයනය කෙරෙහි උනන්දුවක් තිබිය හැක.",
            10: "වෘත්තිය, වගකීම සහ සමාජ පිළිගැනීම වැදගත් තේමාවන් විය හැක.",
            11: "ලාභ, සමාජ ජාල සහ අරමුණු සම්බන්ධයෙන් අවධානය වැඩි විය හැක.",
            12: "විදේශ සම්බන්ධතා, පෞද්ගලික අවකාශය සහ අභ්‍යන්තර සෙවීම වැදගත් විය හැක.",
        },

        "Moon": {
            1: "හැඟීම් සහ මානසික ස්වභාවය පෞරුෂයේ ප්‍රධාන කොටසක් විය හැක.",
            2: "පවුල, ආරක්ෂාව සහ වචන භාවිතය හැඟීම් සමඟ සම්බන්ධ විය හැක.",
            3: "සන්නිවේදනය සහ සමීප සම්බන්ධතා මානසික ලෝකයට බලපානු හැක.",
            4: "නිවස සහ පවුල මානසික සැනසීම සඳහා විශේෂ වැදගත්කමක් ගත හැක.",
            5: "නිර්මාණශීලීත්වය, ආදරය සහ ඉගෙනීම හැඟීම් සමඟ දැඩිව සම්බන්ධ විය හැක.",
            6: "දෛනික වගකීම් සහ සේවා කටයුතු මානසික අවධානයට බලපානු හැක.",
            7: "අනෙක් පුද්ගලයන් සමඟ සම්බන්ධතාවය මානසික තත්ත්වයට වැදගත් විය හැක.",
            8: "ගැඹුරු හැඟීම් සහ අභ්‍යන්තර පරිවර්තන ප්‍රමුඛ විය හැක.",
            9: "විශ්වාසයන්, දැනුම සහ ජීවිතයේ අර්ථය සෙවීම වැදගත් විය හැක.",
            10: "වෘත්තීය සහ සමාජ වගකීම් මානසික ලෝකයට බලපෑමක් කළ හැක.",
            11: "මිතුරන්, සමාජ ජාල සහ අනාගත බලාපොරොත්තු හැඟීම් සමඟ සම්බන්ධ විය හැක.",
            12: "පෞද්ගලික අවකාශය, විවේකය සහ අභ්‍යන්තර ලෝකය වැදගත් විය හැක.",
        },

        "Mars": {
            1: "ක්‍රියාශීලීත්වය, තීරණ ගැනීම සහ තරඟකාරී ස්වභාවය ප්‍රමුඛ විය හැක.",
            2: "ධනය සහ කථනය සම්බන්ධයෙන් ශක්තිමත් ප්‍රකාශනයක් තිබිය හැක.",
            3: "ධෛර්යය, උත්සාහය සහ ස්වාධීන ක්‍රියාකාරීත්වය ශක්තිමත් විය හැක.",
            4: "නිවස සහ පවුල් කටයුතු තුළ ක්‍රියාශීලීත්වය වැඩි විය හැක.",
            5: "නිර්මාණශීලීත්වය සහ තරඟකාරී හැකියාවන් ශක්තිමත් විය හැක.",
            6: "බාධකවලට මුහුණ දීම සහ තරඟකාරී තත්ත්වයන් සමඟ කටයුතු කිරීමේ ශක්තිය පෙන්විය හැක.",
            7: "හවුල්කාරිත්වය තුළ ශක්තිමත් අදහස් සහ ස්වාධීනත්වයක් තිබිය හැක.",
            8: "ගැඹුරු වෙනස්කම් සහ අභියෝගාත්මක තත්ත්වයන් තුළ ක්‍රියාශීලීත්වය පෙන්විය හැක.",
            9: "දැනුම, ගමන් සහ විශ්වාසයන් සම්බන්ධයෙන් ක්‍රියාශීලීත්වයක් තිබිය හැක.",
            10: "වෘත්තීය අරමුණු සහ ජයග්‍රහණ සඳහා දැඩි උත්සාහයක් පෙන්විය හැක.",
            11: "අරමුණු සහ ආදායම් සම්බන්ධයෙන් ශක්තිමත් උත්සාහයක් තිබිය හැක.",
            12: "වියදම්, විදේශ කටයුතු සහ පෞද්ගලික අරගල සම්බන්ධයෙන් ක්‍රියාශීලීත්වය වැඩි විය හැක.",
        },

        "Mercury": {
            1: "බුද්ධිය, සන්නිවේදනය සහ ඉගෙනීම පෞරුෂයේ වැදගත් කොටස් විය හැක.",
            2: "කථන හැකියාව සහ ගණනය/ව්‍යාපාරික සිතීම වැදගත් විය හැක.",
            3: "ලිවීම, කථනය, තොරතුරු හුවමාරුව සහ ඉගෙනීම ප්‍රමුඛ විය හැක.",
            4: "අධ්‍යාපනය සහ නිවස ආශ්‍රිත බුද්ධිමය කටයුතු වැදගත් විය හැක.",
            5: "විශ්ලේෂණාත්මක සිතීම සහ නිර්මාණශීලී බුද්ධිය ප්‍රමුඛ විය හැක.",
            6: "ගැටලු විසඳීම, තොරතුරු විශ්ලේෂණය සහ සේවා කටයුතු වැදගත් විය හැක.",
            7: "සම්බන්ධතා තුළ සංවාදය සහ බුද්ධිමය ගැළපීම වැදගත් විය හැක.",
            8: "ගැඹුරු පර්යේෂණ, රහස් තොරතුරු සහ විශ්ලේෂණයට උනන්දුවක් තිබිය හැක.",
            9: "උසස් අධ්‍යාපනය, භාෂා සහ දාර්ශනික අදහස් කෙරෙහි උනන්දුවක් තිබිය හැක.",
            10: "වෘත්තියේ සන්නිවේදනය, තාක්ෂණය සහ විශ්ලේෂණාත්මක කටයුතු වැදගත් විය හැක.",
            11: "මිතුරු ජාල, ව්‍යාපාර සහ තොරතුරු හරහා ලාභ සම්බන්ධතා ඇති විය හැක.",
            12: "විදේශ සම්බන්ධතා, පර්යේෂණ සහ පෞද්ගලික අධ්‍යයනය වැදගත් විය හැක.",
        },

        "Jupiter": {
            1: "දැනුම, වර්ධනය සහ උපදේශන ස්වභාවය පෞරුෂයට බලපානු හැක.",
            2: "ධනය, පවුල සහ දැනුම සම්බන්ධ කරුණු ප්‍රමුඛ විය හැක.",
            3: "ඉගෙනීම සහ දැනුම බෙදාගැනීම කෙරෙහි උනන්දුවක් තිබිය හැක.",
            4: "අධ්‍යාපනය, නිවස සහ පවුල් වටිනාකම් වැදගත් විය හැක.",
            5: "අධ්‍යාපනය, නිර්මාණශීලීත්වය සහ දැනුමට විශේෂ අවධානයක් ලැබිය හැක.",
            6: "සේවය, දැනුම සහ ගැටලු විසඳීම සම්බන්ධයෙන් අවධානය යොමු විය හැක.",
            7: "විවාහය සහ හවුල්කාරිත්වය තුළ දැනුම සහ වර්ධනය වැදගත් විය හැක.",
            8: "ගැඹුරු දැනුම, පර්යේෂණ සහ අභ්‍යන්තර අවබෝධය ප්‍රමුඛ විය හැක.",
            9: "උසස් දැනුම, භාග්‍යය සහ දාර්ශනික සෙවීම ප්‍රමුඛ විය හැක.",
            10: "වෘත්තීය වර්ධනය, උපදේශනය සහ සමාජ වගකීම් වැදගත් විය හැක.",
            11: "ආදායම්, ජාල සහ අනාගත අරමුණු සම්බන්ධයෙන් වර්ධන අවස්ථා සලකා බැලිය හැක.",
            12: "විදේශ අත්දැකීම්, අධ්‍යාත්මික සෙවීම සහ පරිත්‍යාගශීලීත්වය වැදගත් විය හැක.",
        },

        "Venus": {
            1: "ආකර්ෂණය, සෞන්දර්යය සහ සම්බන්ධතා පෞරුෂයේ වැදගත් කොටස් විය හැක.",
            2: "ධනය, සෞන්දර්යය සහ පවුල් සුවපහසුව කෙරෙහි අවධානයක් තිබිය හැක.",
            3: "කලාත්මක සන්නිවේදනය සහ සමාජ සම්බන්ධතා වැදගත් විය හැක.",
            4: "නිවසේ සුවපහසුව, කලාත්මක රුචිය සහ පවුල් සතුට වැදගත් විය හැක.",
            5: "ආදරය, කලාව සහ නිර්මාණශීලීත්වය ප්‍රමුඛ විය හැක.",
            6: "සේවා පරිසරය තුළ සම්බන්ධතා සහ සහයෝගීත්වය වැදගත් විය හැක.",
            7: "විවාහය, ආදරය සහ හවුල්කාරිත්වය විශේෂ වැදගත්කමක් ගත හැක.",
            8: "ගැඹුරු සම්බන්ධතා සහ පරිවර්තනීය අත්දැකීම් වැදගත් විය හැක.",
            9: "කලා, සංස්කෘතිය සහ ගමන් සම්බන්ධ අත්දැකීම් වැදගත් විය හැක.",
            10: "වෘත්තිය තුළ සෞන්දර්යය, නිර්මාණශීලීත්වය සහ සමාජ සම්බන්ධතා වැදගත් විය හැක.",
            11: "සමාජ ජාල සහ සම්බන්ධතා හරහා ලාභ හෝ අවස්ථා සම්බන්ධ විය හැක.",
            12: "විදේශ අත්දැකීම්, සුවපහසුව සහ පෞද්ගලික සම්බන්ධතා වැදගත් විය හැක.",
        },

        "Saturn": {
            1: "වගකීම, ඉවසීම සහ ස්වයං පාලනය ප්‍රමුඛ ජීවන තේමාවන් විය හැක.",
            2: "ධනය සහ පවුල් වගකීම් සම්බන්ධයෙන් ඉවසීම සහ සැලසුම් කිරීම වැදගත් විය හැක.",
            3: "දිගුකාලීන උත්සාහය සහ ඉවසීම හරහා දියුණුව සලකා බැලිය හැක.",
            4: "නිවස සහ පවුල් වගකීම් සම්බන්ධයෙන් ඉවසීම අවශ්‍ය විය හැක.",
            5: "අධ්‍යාපනය සහ නිර්මාණශීලීත්වය තුළ ක්‍රමවත් සහ වගකීම් සහිත ප්‍රවේශයක් තිබිය හැක.",
            6: "දෛනික වැඩ, සේවය සහ අභියෝගවලට දිගුකාලීනව මුහුණ දීමේ තේමාවක් තිබිය හැක.",
            7: "සම්බන්ධතා සහ හවුල්කාරිත්වය තුළ වගකීම සහ ඉවසීම වැදගත් විය හැක.",
            8: "ගැඹුරු පරිවර්තන සහ ජීවිතයේ අභියෝග හරහා ඉගෙනීමේ තේමාවක් තිබිය හැක.",
            9: "විශ්වාසයන් සහ උසස් අධ්‍යාපනය සම්බන්ධයෙන් ක්‍රමවත් ප්‍රවේශයක් තිබිය හැක.",
            10: "වෘත්තීය වගකීම්, ඉවසීම සහ දිගුකාලීන ගොඩනැගීම ප්‍රමුඛ විය හැක.",
            11: "ලාභ සහ අරමුණු සම්බන්ධයෙන් මන්දගාමී නමුත් ස්ථාවර ප්‍රගතියක් පිළිබඳ තේමාවක් තිබිය හැක.",
            12: "පෞද්ගලික සීමා, වියදම් සහ අභ්‍යන්තර වගකීම් පිළිබඳ අවධානයක් තිබිය හැක.",
        },
    }

    # ==========================================================
    # CONSTRUCTOR
    # ==========================================================

    def __init__(self, chart_data: dict):
        self.chart = chart_data or {}

    # ==========================================================
    # COMMON HELPERS
    # ==========================================================

    def _house(self, planet_data):
        if not isinstance(planet_data, dict):
            return None

        house = planet_data.get("house")

        try:
            return int(house) if house is not None else None
        except (TypeError, ValueError):
            return None

    def _sign_si(self, sign):
        return self.SIGN_NAMES_SI.get(
            sign,
            sign or "-"
        )

    def _planet_si(self, planet):
        return self.PLANET_NAMES_SI.get(
            planet,
            planet
        )


    # ==========================================================
    # DEEP PLANET INTERPRETATION
    # ==========================================================

    def _build_deep_planet_text(
        self,
        planet,
        sign,
        house,
        sign_lord,
        sign_lord_house,
        nakshatra,
        nakshatra_lord,
        pada,
        retrograde,
    ):
        """
        Build a context-rich traditional interpretation.

        This method does not calculate astronomical positions.
        It only combines already calculated chart data with
        the interpretation rules defined in this engine.
        """

        planet_si = self._planet_si(planet)
        sign_si = self._sign_si(sign)
        sign_lord_si = self._planet_si(sign_lord)
        nakshatra_lord_si = self._planet_si(nakshatra_lord)

        house_meaning = self.HOUSE_MEANINGS.get(
            house,
            "ජීවන කරුණු"
        )

        parts = []

        # ------------------------------------------------------
        # BASIC PLACEMENT
        # ------------------------------------------------------

        parts.append(
            f"{planet_si} {sign_si} රාශියේ "
            f"{house or '-'} වන භාවයේ පිහිටා ඇත."
        )

        # ------------------------------------------------------
        # PLANET + HOUSE THEME
        # ------------------------------------------------------

        planet_theme = (
            self.PLANET_HOUSE_THEMES
            .get(planet, {})
            .get(house)
        )

        if planet_theme:
            parts.append(planet_theme)

        # ------------------------------------------------------
        # HOUSE MEANING
        # ------------------------------------------------------

        if house in self.HOUSE_MEANINGS:
            parts.append(
                f"මෙම පිහිටීම {house_meaning} සම්බන්ධ "
                f"ජීවන අත්දැකීම් විශ්ලේෂණයේදී වැදගත් "
                f"සන්දර්භයක් ලබා දෙයි."
            )

        # ------------------------------------------------------
        # SIGN LORD
        # ------------------------------------------------------

        if sign_lord:
            if sign_lord_house:
                parts.append(
                    f"{sign_si} රාශියේ අධිපති {sign_lord_si} වන අතර, "
                    f"එම අධිපති {sign_lord_house} වන භාවයේ "
                    f"පිහිටා ඇත."
                )
            else:
                parts.append(
                    f"{sign_si} රාශියේ අධිපති "
                    f"{sign_lord_si} වේ."
                )

        # ------------------------------------------------------
        # NAKSHATRA
        # ------------------------------------------------------

        if nakshatra and nakshatra != "-":
            nakshatra_text = f"{nakshatra} නක්ෂත්‍රයේ "

            if pada is not None:
                nakshatra_text += f"{pada} පාදයේ "

            nakshatra_text += "මෙම ග්‍රහ පිහිටීම සටහන් වේ."
            parts.append(nakshatra_text)

        # ------------------------------------------------------
        # NAKSHATRA LORD
        # ------------------------------------------------------

        if nakshatra_lord:
            parts.append(
                f"මෙම නක්ෂත්‍රයේ අධිපති "
                f"{nakshatra_lord_si} වේ."
            )

        # ------------------------------------------------------
        # RETROGRADE
        # ------------------------------------------------------

        if retrograde:
            parts.append(
                f"{planet_si} වක්‍ර ගමනක පවතින බැවින්, "
                f"සාම්ප්‍රදායික ජ්‍යෝතිෂ විශ්ලේෂණයේදී "
                f"එම ග්‍රහ තේමාවන් අභ්‍යන්තරව හෝ "
                f"වෙනස් ආකාරයකින් අත්දැකිය හැකි බව "
                f"සලකා බලයි."
            )
        else:
            parts.append(
                f"{planet_si} සෘජු ගමනක පවතින බව "
                f"ගණනය කර ඇත."
            )

        # ------------------------------------------------------
        # FINAL CONTEXT
        # ------------------------------------------------------

        parts.append(
            f"මෙම කරුණු සියල්ල එකට සලකා බැලීමෙන් "
            f"{planet_si} සම්බන්ධ ජීවන තේමාවන් පිළිබඳ "
            f"වඩා සම්පූර්ණ විශ්ලේෂණයක් ගොඩනගා ගත හැක."
        )

        return " ".join(parts)

    # ==========================================================
    # LAGNA INTERPRETATION
    # ==========================================================

    def interpret_lagna(self):

        lagna = self.chart.get("lagna", {})

        sign = lagna.get("sign")
        nakshatra = lagna.get("nakshatra", {})

        if isinstance(nakshatra, dict):
            nakshatra_name = nakshatra.get("name", "-")
        else:
            nakshatra_name = str(nakshatra or "-")

        return {
            "title": "ලග්න විශ්ලේෂණය",
            "sign": self._sign_si(sign),
            "nakshatra": nakshatra_name,
            "text": (
                f"ඔබගේ ලග්නය {self._sign_si(sign)} රාශියයි. "
                f"ලග්න පිහිටීම අනුව ඔබගේ පෞරුෂය, "
                f"ජීවන ප්‍රවේශය සහ බාහිර හැසිරීම් පිළිබඳ "
                f"ප්‍රධාන තේමාවන් විශ්ලේෂණය කළ හැක."
            ),
        }

    # ==========================================================
    # MOON INTERPRETATION
    # ==========================================================

    def interpret_moon(self):

        planets = self.chart.get("planets", {})

        if not isinstance(planets, dict):
            planets = {}

        moon = planets.get("Moon", {})

        if not isinstance(moon, dict):
            moon = {}

        sign = moon.get("sign")
        house = self._house(moon)

        text = (
            f"සඳු {self._sign_si(sign)} රාශියේ "
            f"{house or '-'} වන භාවයේ පිහිටා ඇත. "
        )

        if house in self.HOUSE_MEANINGS:
            text += (
                f"මෙම පිහිටීම {self.HOUSE_MEANINGS[house]} "
                f"සම්බන්ධ මානසික තේමාවන් විශ්ලේෂණයට භාවිතා කළ හැක."
            )

        return {
            "title": "සඳු සහ මානසික ස්වභාවය",
            "sign": self._sign_si(sign),
            "house": house,
            "text": text,
        }

    # ==========================================================
    # PLANET INTERPRETATION
    # ==========================================================

    def interpret_planets(self):
        """
        Generate detailed interpretation data for the main planets,
        Rahu and Ketu.

        This method does NOT perform astronomy calculations.
        It only uses values already calculated by the astrology engine.
        """

        results = []

        planets = self.chart.get("planets", {})
        if not isinstance(planets, dict):
            planets = {}

        # ----------------------------------------------------------
        # Helper: find where a planet is placed
        # ----------------------------------------------------------

        def get_planet_house(planet_name):
            if not planet_name:
                return None

            planet_data = planets.get(planet_name)

            if isinstance(planet_data, dict):
                return self._house(planet_data)

            return None

        # ----------------------------------------------------------
        # Helper: detailed planet result
        # ----------------------------------------------------------

        def build_planet_result(planet, data):
            if not isinstance(data, dict):
                return None

            house = self._house(data)
            sign = data.get("sign")

            # ------------------------------------------------------
            # Sign lord
            # ------------------------------------------------------

            sign_lord = self.SIGN_LORDS.get(sign)
            sign_lord_si = self._planet_si(sign_lord)
            sign_lord_house = get_planet_house(sign_lord)

            # ------------------------------------------------------
            # Nakshatra information
            #
            # Current astrology engine stores nakshatra/lord/pada
            # as planet-level values. This also safely supports a
            # nested nakshatra dictionary if that structure is used.
            # ------------------------------------------------------

            nakshatra_data = data.get("nakshatra")

            if isinstance(nakshatra_data, dict):
                nakshatra = nakshatra_data.get("name", "-")
                nakshatra_lord = (
                    nakshatra_data.get("lord")
                    or data.get("nakshatra_lord")
                    or data.get("lord")
                )
                pada = (
                    nakshatra_data.get("pada")
                    or data.get("pada")
                )
            else:
                nakshatra = str(nakshatra_data or "-")
                nakshatra_lord = (
                    data.get("nakshatra_lord")
                    or data.get("lord")
                )
                pada = data.get("pada")

            nakshatra_lord_si = self._planet_si(nakshatra_lord)

            # ------------------------------------------------------
            # Deep planet interpretation
            # ------------------------------------------------------

            theme = self._build_deep_planet_text(
                planet=planet,
                sign=sign,
                house=house,
                sign_lord=sign_lord,
                sign_lord_house=sign_lord_house,
                nakshatra=nakshatra,
                nakshatra_lord=nakshatra_lord,
                pada=pada,
                retrograde=data.get("retrograde", False),
            )

            return {
                "planet": planet,
                "planet_si": self._planet_si(planet),

                # Sign
                "sign": self._sign_si(sign),
                "sign_en": sign,

                # House
                "house": house,

                # Sign lord
                "sign_lord": sign_lord,
                "sign_lord_si": sign_lord_si,
                "sign_lord_house": sign_lord_house,

                # Nakshatra
                "nakshatra": nakshatra,
                "nakshatra_lord": nakshatra_lord,
                "nakshatra_lord_si": nakshatra_lord_si,
                "pada": pada,

                # Other calculated information
                "retrograde": data.get("retrograde", False),

                # Existing interpretation
                "text": theme,
            }

        # ==========================================================
        # MAIN PLANETS
        # ==========================================================

        for planet, data in planets.items():

            result = build_planet_result(planet, data)

            if result is not None:
                results.append(result)

        # ==========================================================
        # RAHU
        # ==========================================================

        rahu = self.chart.get("rahu")

        if isinstance(rahu, dict):

            house = self._house(rahu)
            sign = rahu.get("sign")

            sign_lord = self.SIGN_LORDS.get(sign)
            sign_lord_house = get_planet_house(sign_lord)

            nakshatra_data = rahu.get("nakshatra")

            if isinstance(nakshatra_data, dict):
                nakshatra = nakshatra_data.get("name", "-")
                nakshatra_lord = (
                    nakshatra_data.get("lord")
                    or rahu.get("nakshatra_lord")
                    or rahu.get("lord")
                )
                pada = (
                    nakshatra_data.get("pada")
                    or rahu.get("pada")
                )
            else:
                nakshatra = str(nakshatra_data or "-")
                nakshatra_lord = (
                    rahu.get("nakshatra_lord")
                    or rahu.get("lord")
                )
                pada = rahu.get("pada")

            results.append({
                "planet": "Rahu",
                "planet_si": "රාහු",

                "sign": self._sign_si(sign),
                "sign_en": sign,

                "house": house,

                "sign_lord": sign_lord,
                "sign_lord_si": self._planet_si(sign_lord),
                "sign_lord_house": sign_lord_house,

                "nakshatra": nakshatra,
                "nakshatra_lord": nakshatra_lord,
                "nakshatra_lord_si": self._planet_si(nakshatra_lord),
                "pada": pada,

                "retrograde": rahu.get("retrograde", True),

                "text": self._build_deep_planet_text(
                    planet="Rahu",
                    sign=sign,
                    house=house,
                    sign_lord=sign_lord,
                    sign_lord_house=sign_lord_house,
                    nakshatra=nakshatra,
                    nakshatra_lord=nakshatra_lord,
                    pada=pada,
                    retrograde=rahu.get("retrograde", True),
                ),
            })

        # ==========================================================
        # KETU
        # ==========================================================

        ketu = self.chart.get("ketu")

        if isinstance(ketu, dict):

            house = self._house(ketu)
            sign = ketu.get("sign")

            sign_lord = self.SIGN_LORDS.get(sign)
            sign_lord_house = get_planet_house(sign_lord)

            nakshatra_data = ketu.get("nakshatra")

            if isinstance(nakshatra_data, dict):
                nakshatra = nakshatra_data.get("name", "-")
                nakshatra_lord = (
                    nakshatra_data.get("lord")
                    or ketu.get("nakshatra_lord")
                    or ketu.get("lord")
                )
                pada = (
                    nakshatra_data.get("pada")
                    or ketu.get("pada")
                )
            else:
                nakshatra = str(nakshatra_data or "-")
                nakshatra_lord = (
                    ketu.get("nakshatra_lord")
                    or ketu.get("lord")
                )
                pada = ketu.get("pada")

            results.append({
                "planet": "Ketu",
                "planet_si": "කේතු",

                "sign": self._sign_si(sign),
                "sign_en": sign,

                "house": house,

                "sign_lord": sign_lord,
                "sign_lord_si": self._planet_si(sign_lord),
                "sign_lord_house": sign_lord_house,

                "nakshatra": nakshatra,
                "nakshatra_lord": nakshatra_lord,
                "nakshatra_lord_si": self._planet_si(nakshatra_lord),
                "pada": pada,

                "retrograde": ketu.get("retrograde", True),

                "text": self._build_deep_planet_text(
                    planet="Ketu",
                    sign=sign,
                    house=house,
                    sign_lord=sign_lord,
                    sign_lord_house=sign_lord_house,
                    nakshatra=nakshatra,
                    nakshatra_lord=nakshatra_lord,
                    pada=pada,
                    retrograde=ketu.get("retrograde", True),
                ),
            })

        return results

    # ==========================================================
    # 12 HOUSE INTERPRETATION
    # ==========================================================

    def interpret_houses(self):

        results = []

        # ------------------------------------------------------
        # Create house -> planets mapping
        # ------------------------------------------------------

        house_planets = {
            house: []
            for house in range(1, 13)
        }

        planets = self.chart.get("planets", {})

        for planet, data in planets.items():

            if not isinstance(data, dict):
                continue

            house = self._house(data)

            if house in house_planets:
                house_planets[house].append(
                    self._planet_si(planet)
                )

        # ------------------------------------------------------
        # Rahu
        # ------------------------------------------------------

        rahu = self.chart.get("rahu")

        if isinstance(rahu, dict):

            house = self._house(rahu)

            if house in house_planets:
                house_planets[house].append("රාහු")

        # ------------------------------------------------------
        # Ketu
        # ------------------------------------------------------

        ketu = self.chart.get("ketu")

        if isinstance(ketu, dict):

            house = self._house(ketu)

            if house in house_planets:
                house_planets[house].append("කේතු")

        # ------------------------------------------------------
        # Generate interpretation for all 12 houses
        # ------------------------------------------------------

        for house in range(1, 13):

            meaning = self.HOUSE_MEANINGS.get(
                house,
                "ජීවන තේමාවන්"
            )

            placed_planets = house_planets.get(
                house,
                []
            )

            # --------------------------------------------------
            # No planets
            # --------------------------------------------------

            if not placed_planets:

                text = (
                    f"{house} වන භාවය {meaning} සම්බන්ධ "
                    f"ජීවන කරුණු නිරූපණය කරයි. "
                    f"මෙම භාවයේ ග්‍රහයන් සෘජුව පිහිටා නොමැත."
                )

            # --------------------------------------------------
            # One or more planets
            # --------------------------------------------------

            else:

                planet_text = " සහ ".join(
                    placed_planets
                )

                text = (
                    f"{house} වන භාවය {meaning} සම්බන්ධ "
                    f"ජීවන කරුණු නිරූපණය කරයි. "
                    f"මෙම භාවයේ {planet_text} "
                    f"පිහිටා ඇත. "
                )

                # ----------------------------------------------
                # Add individual planet themes
                # ----------------------------------------------

                theme_parts = []

                for planet_name in placed_planets:

                    # Convert Sinhala name back to English key
                    english_planet = None

                    for key, value in self.PLANET_NAMES_SI.items():

                        if value == planet_name:
                            english_planet = key
                            break

                    if english_planet is None:
                        continue

                    theme = (
                        self.PLANET_HOUSE_THEMES
                        .get(english_planet, {})
                        .get(house)
                    )

                    if theme:
                        theme_parts.append(theme)

                if theme_parts:

                    text += " ".join(theme_parts)

                # ----------------------------------------------
                # Special Rahu/Ketu themes
                # ----------------------------------------------

                if "රාහු" in placed_planets:

                    text += (
                        " රාහු නිසා මෙම භාවයට සම්බන්ධ "
                        "අත්දැකීම්, ආශාවන් සහ නව මාර්ග පිළිබඳ "
                        "විශේෂ අවධානයක් යොමු විය හැක."
                    )

                if "කේතු" in placed_planets:

                    text += (
                        " කේතු නිසා මෙම භාවයට සම්බන්ධ "
                        "අත්දැකීම් තුළ අභ්‍යන්තර සෙවීම, "
                        "වෙන්වීම හෝ ගැඹුරු අවබෝධය පිළිබඳ "
                        "තේමාවන් සලකා බැලිය හැක."
                    )

            # --------------------------------------------------
            # Add house result
            # --------------------------------------------------

            results.append({
                "house": house,
                "meaning": meaning,
                "planets": placed_planets,
                "text": text,
            })

        return results

    # ==========================================================
    # HOUSE LORD INTERPRETATION
    # ==========================================================

    def interpret_house_lords(self, houses):

        """
        Calculate the lord of each house based on the Ascendant.

        The house lord is determined from:
        Ascendant sign -> Whole Sign house sequence -> Sign lord.

        This method does NOT perform astronomy calculations.
        It only interprets already calculated chart data.
        """

        lagna = self.chart.get("lagna", {})

        if not isinstance(lagna, dict):
            return houses

        lagna_sign = lagna.get("sign")

        sign_order = [
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

        # ------------------------------------------------------
        # Validate Ascendant sign
        # ------------------------------------------------------

        if lagna_sign not in sign_order:
            return houses

        lagna_index = sign_order.index(lagna_sign)

        planets = self.chart.get("planets", {})

        if not isinstance(planets, dict):
            planets = {}

        # ------------------------------------------------------
        # Calculate each house sign and lord
        # ------------------------------------------------------

        for house_data in houses:

            if not isinstance(house_data, dict):
                continue

            house = house_data.get("house")

            if not isinstance(house, int):
                try:
                    house = int(house)
                except (TypeError, ValueError):
                    continue

            if house < 1 or house > 12:
                continue

            # Whole Sign house calculation
            house_sign_index = (
                lagna_index + house - 1
            ) % 12

            house_sign = sign_order[house_sign_index]

            lord = self.SIGN_LORDS.get(house_sign)

            # --------------------------------------------------
            # Lord placement
            # --------------------------------------------------

            lord_data = planets.get(lord, {})

            if not isinstance(lord_data, dict):
                lord_data = {}

            lord_house = self._house(lord_data)

            lord_sign = lord_data.get("sign")

            # --------------------------------------------------
            # Add House Lord information
            # --------------------------------------------------

            house_data["sign"] = house_sign

            house_data["sign_si"] = self._sign_si(
                house_sign
            )

            house_data["lord"] = lord

            house_data["lord_si"] = self._planet_si(
                lord
            )

            house_data["lord_sign"] = (
                self._sign_si(lord_sign)
                if lord_sign
                else "-"
            )

            house_data["lord_house"] = lord_house

            # --------------------------------------------------
            # Add readable lord information
            # --------------------------------------------------

            if lord:

                if lord_house:

                    house_data["lord_text"] = (
                        f"{house_data['sign_si']} රාශියේ "
                        f"{house} වන භාවයේ අධිපති "
                        f"{house_data['lord_si']} වේ. "
                        f"{house_data['lord_si']} "
                        f"{house_data['lord_sign']} රාශියේ "
                        f"{lord_house} වන භාවයේ පිහිටා ඇත."
                    )

                else:

                    house_data["lord_text"] = (
                        f"{house_data['sign_si']} රාශියේ "
                        f"{house} වන භාවයේ අධිපති "
                        f"{house_data['lord_si']} වේ."
                    )

            else:

                house_data["lord_text"] = (
                    "මෙම භාවයට අධිපති ග්‍රහයා හඳුනාගත නොහැක."
                )

        return houses

    # ==========================================================
    # GENERATE COMPLETE INTERPRETATION
    # ==========================================================

    def generate(self):

        # First generate the basic 12-house interpretation
        houses = self.interpret_houses()

        # Then calculate house signs and house lords
        houses = self.interpret_house_lords(houses)

        return {
            "lagna": self.interpret_lagna(),
            "moon": self.interpret_moon(),
            "planets": self.interpret_planets(),
            "houses": houses,
        }