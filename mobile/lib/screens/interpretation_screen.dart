import 'package:flutter/material.dart';

class InterpretationScreen extends StatelessWidget {
  final Map<String, dynamic> chartData;

  const InterpretationScreen({
    super.key,
    required this.chartData,
  });

  static const Color primary = Color(0xFF6A1B9A);
  static const Color darkPurple = Color(0xFF4A148C);
  static const Color pageBackground = Color(0xFFF7F4FA);

  String translateSign(String? sign) {
    const signs = {
      'Aries': 'මේෂ',
      'Taurus': 'වෘෂභ',
      'Gemini': 'මිථුන',
      'Cancer': 'කටක',
      'Leo': 'සිංහ',
      'Virgo': 'කන්‍යා',
      'Libra': 'තුලා',
      'Scorpio': 'වෘශ්චික',
      'Sagittarius': 'ධනු',
      'Capricorn': 'මකර',
      'Aquarius': 'කුම්භ',
      'Pisces': 'මීන',
    };

    return signs[sign] ?? sign ?? '';
  }

  String translateNakshatra(String? nakshatra) {
    const nakshatras = {
      'Ashwini': 'අශ්විනී',
      'Bharani': 'භරණී',
      'Krittika': 'කෘත්තිකා',
      'Rohini': 'රෝහිණී',
      'Mrigashira': 'මුවසිරස',
      'Ardra': 'ආර්ද්‍රා',
      'Punarvasu': 'පුනාවස',
      'Pushya': 'පුෂ්‍ය',
      'Ashlesha': 'අස්ලිස',
      'Magha': 'මාඝා',
      'Purva Phalguni': 'පූර්ව ඵල්ගුණී',
      'Uttara Phalguni': 'උත්තර ඵල්ගුණී',
      'Hasta': 'හස්ත',
      'Chitra': 'චිත්‍රා',
      'Swati': 'ස්වාතී',
      'Vishakha': 'විශාඛා',
      'Anuradha': 'අනුරාධා',
      'Jyeshtha': 'ජ්‍යේෂ්ඨා',
      'Mula': 'මූල',
      'Purva Ashadha': 'පූර්වාෂාඪා',
      'Uttara Ashadha': 'උත්තරාෂාඪා',
      'Shravana': 'ශ්‍රවණ',
      'Dhanishta': 'ධනිෂ්ඨා',
      'Shatabhisha': 'ශතභිෂා',
      'Purva Bhadrapada': 'පූර්ව භාද්‍රපදා',
      'Uttara Bhadrapada': 'උත්තර භාද්‍රපදා',
      'Revati': 'රේවතී',
    };

    return nakshatras[nakshatra] ?? nakshatra ?? '';
  }

  String planetName(String? planet) {
    const planets = {
      'Sun': 'රවි',
      'Moon': 'සඳු',
      'Mars': 'කුජ',
      'Mercury': 'බුධ',
      'Jupiter': 'ගුරු',
      'Venus': 'සිකුරු',
      'Saturn': 'ශනි',
      'Rahu': 'රාහු',
      'Ketu': 'කේතු',
    };

    return planets[planet] ?? planet ?? '';
  }

  String houseTitle(int house) {
    const titles = {
      1: 'ස්වභාවය, පෞරුෂය සහ ශරීරය',
      2: 'ධනය, පවුල සහ කථනය',
      3: 'ධෛර්යය සහ සන්නිවේදනය',
      4: 'නිවස සහ අභ්‍යන්තර සැනසීම',
      5: 'බුද්ධිය, නිර්මාණශීලීත්වය සහ ආදරය',
      6: 'සේවය, දෛනික වැඩ සහ තරඟකාරීත්වය',
      7: 'විවාහය සහ හවුල්කාරිත්වය',
      8: 'පරිවර්තනය සහ ගැඹුරු කරුණු',
      9: 'භාග්‍යය සහ උසස් අධ්‍යාපනය',
      10: 'වෘත්තිය, කීර්තිය සහ වගකීම්',
      11: 'ලාභ, ආදායම් සහ බලාපොරොත්තු',
      12: 'වියදම්, විදේශ සම්බන්ධතා සහ අභ්‍යන්තර ලෝකය',
    };

    return titles[house] ?? '';
  }

  String houseNumberSinhala(int house) {
    const numbers = {
      1: '1 වන',
      2: '2 වන',
      3: '3 වන',
      4: '4 වන',
      5: '5 වන',
      6: '6 වන',
      7: '7 වන',
      8: '8 වන',
      9: '9 වන',
      10: '10 වන',
      11: '11 වන',
      12: '12 වන',
    };

    return numbers[house] ?? '$house වන';
  }

  String safeValue(dynamic value, {String fallback = '-'}) {
    if (value == null) return fallback;
    final text = value.toString().trim();
    return text.isEmpty ? fallback : text;
  }

  String padaText(dynamic pada) {
    if (pada == null) return '-';
    return '${pada.toString()} පාදය';
  }

  Widget sectionTitle(String title, IconData icon) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: primary.withOpacity(0.12),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: primary),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            title,
            style: const TextStyle(
              fontSize: 21,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }

  Widget infoCard({
    required String title,
    required String text,
    IconData icon = Icons.auto_awesome,
  }) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.all(17),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.06),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(9),
            decoration: BoxDecoration(
              color: primary.withOpacity(0.10),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, size: 21, color: primary),
          ),
          const SizedBox(width: 13),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 7),
                Text(
                  text,
                  style: const TextStyle(
                    fontSize: 15,
                    height: 1.55,
                    color: Colors.black87,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget dataChip(String label, String value) {
    return Expanded(
      child: Container(
        constraints: const BoxConstraints(minHeight: 68),
        padding: const EdgeInsets.symmetric(
          horizontal: 9,
          vertical: 10,
        ),
        decoration: BoxDecoration(
          color: const Color(0xFFF7F1FA),
          borderRadius: BorderRadius.circular(13),
          border: Border.all(
            color: primary.withOpacity(0.10),
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              label,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey.shade700,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              value,
              textAlign: TextAlign.center,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
                color: darkPurple,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget placementGrid({
    required String sign,
    required String house,
    required String signLord,
    required String signLordHouse,
  }) {
    return Column(
      children: [
        Row(
          children: [
            dataChip('රාශිය', sign),
            const SizedBox(width: 8),
            dataChip('භාවය', house),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            dataChip('රාශි අධිපති', signLord),
            const SizedBox(width: 8),
            dataChip('අධිපතිගේ භාවය', signLordHouse),
          ],
        ),
      ],
    );
  }

  Widget nakshatraGrid({
    required String nakshatra,
    required String lord,
    required String pada,
  }) {
    return Row(
      children: [
        dataChip('නක්ෂත්‍රය', nakshatra),
        const SizedBox(width: 8),
        dataChip('අධිපති', lord),
        const SizedBox(width: 8),
        dataChip('පාදය', pada),
      ],
    );
  }

  Widget buildLagnaCard(Map<String, dynamic> lagna) {
    final String sign = translateSign(lagna['sign']?.toString());
    final String nakshatra = translateNakshatra(lagna['nakshatra']?.toString());
    final String lord = planetName(lagna['lord']?.toString());

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: primary.withOpacity(0.12)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.055),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 50,
                height: 50,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [primary, Color(0xFF8E24AA)],
                  ),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: const Icon(
                  Icons.person_outline,
                  color: Colors.white,
                  size: 27,
                ),
              ),
              const SizedBox(width: 13),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'ලග්නය — $sign',
                      style: const TextStyle(
                        fontSize: 19,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'රාශි අධිපති: $lord',
                      style: TextStyle(
                        color: Colors.grey.shade700,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 15),
          placementGrid(
            sign: sign,
            house: '1 වන',
            signLord: lord,
            signLordHouse: '-',
          ),
          const SizedBox(height: 8),
          nakshatraGrid(
            nakshatra: nakshatra,
            lord: planetName(lagna['lord']?.toString()),
            pada: padaText(lagna['pada']),
          ),
          if (safeValue(lagna['text']) != '-') ...[
            const SizedBox(height: 15),
            Text(
              safeValue(lagna['text']),
              style: const TextStyle(
                fontSize: 15,
                height: 1.6,
                color: Colors.black87,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget buildMoonCard(Map<String, dynamic> moon) {
    final String sign = translateSign(moon['sign']?.toString());
    final String house = safeValue(moon['house']);
    final String nakshatra = translateNakshatra(moon['nakshatra']?.toString());
    final String nakshatraLord = planetName(moon['nakshatra_lord']?.toString());
    final String signLord = planetName(moon['sign_lord']?.toString());

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: primary.withOpacity(0.12)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.055),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 50,
                height: 50,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: const Color(0xFFEDE7F6),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: const Icon(
                  Icons.nightlight_round,
                  color: darkPurple,
                  size: 28,
                ),
              ),
              const SizedBox(width: 13),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'සඳු — $sign',
                      style: const TextStyle(
                        fontSize: 19,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '$house වන භාවය',
                      style: TextStyle(
                        color: Colors.grey.shade700,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 15),
          placementGrid(
            sign: sign,
            house: house,
            signLord: signLord,
            signLordHouse: safeValue(moon['sign_lord_house']),
          ),
          const SizedBox(height: 8),
          nakshatraGrid(
            nakshatra: nakshatra,
            lord: nakshatraLord,
            pada: padaText(moon['pada']),
          ),
          if (safeValue(moon['text']) != '-') ...[
            const SizedBox(height: 15),
            Text(
              safeValue(moon['text']),
              style: const TextStyle(
                fontSize: 15,
                height: 1.6,
                color: Colors.black87,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget buildPlanetCard(Map<String, dynamic> planet) {
    final String name = planetName(planet['planet']?.toString());
    final String sign = translateSign(planet['sign']?.toString());
    final String house = safeValue(planet['house']);
    final String signLord = planetName(planet['sign_lord']?.toString());

    final String signLordHouse = safeValue(planet['sign_lord_house']);

    final String nakshatra =
        translateNakshatra(planet['nakshatra']?.toString());

    final String nakshatraLord =
        planetName(planet['nakshatra_lord']?.toString());

    final bool retrograde = planet['retrograde'] == true;
    final String text = safeValue(planet['text']);

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: retrograde
              ? Colors.orange.withOpacity(0.30)
              : primary.withOpacity(0.10),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.055),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 46,
                height: 46,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: retrograde
                      ? const Color(0xFFFFF3E0)
                      : const Color(0xFFEDE7F6),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(
                  Icons.brightness_7,
                  color: retrograde ? Colors.orange.shade800 : darkPurple,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      name,
                      style: const TextStyle(
                        fontSize: 19,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      '$sign • $house වන භාවය',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade700,
                      ),
                    ),
                  ],
                ),
              ),
              if (retrograde)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 9,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF3E0),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: const Text(
                    'වක්‍ර',
                    style: TextStyle(
                      color: Colors.deepOrange,
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 15),
          placementGrid(
            sign: sign,
            house: house,
            signLord: signLord,
            signLordHouse: signLordHouse,
          ),
          const SizedBox(height: 8),
          nakshatraGrid(
            nakshatra: nakshatra,
            lord: nakshatraLord,
            pada: padaText(planet['pada']),
          ),
          if (text != '-') ...[
            const SizedBox(height: 15),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFFFAF7FC),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Text(
                text,
                style: const TextStyle(
                  fontSize: 15,
                  height: 1.65,
                  color: Colors.black87,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget buildHouseCard(Map<String, dynamic> houseData) {
    final int house = int.tryParse(
          houseData['house']?.toString() ?? '',
        ) ??
        0;

    final String meaning =
        safeValue(houseData['meaning'], fallback: houseTitle(house));

    final List<dynamic> planets =
        (houseData['planets'] as List<dynamic>?) ?? [];

    final String text = safeValue(houseData['text']);

    final String sign = safeValue(houseData['sign_si'],
        fallback: translateSign(
          houseData['sign']?.toString(),
        ));

    final String lord = safeValue(houseData['lord_si'],
        fallback: planetName(
          houseData['lord']?.toString(),
        ));

    final String lordSign = safeValue(houseData['lord_sign'],
        fallback: translateSign(
          houseData['lord_sign_en']?.toString(),
        ));

    final String lordHouse = safeValue(houseData['lord_house']);

    final List<String> translatedPlanets =
        planets.map((planet) => planetName(planet.toString())).toList();

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(17),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: primary.withOpacity(0.10),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.055),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 43,
                height: 43,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: primary,
                  borderRadius: BorderRadius.circular(13),
                ),
                child: Text(
                  '$house',
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${houseNumberSinhala(house)} භාවය',
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      meaning,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade700,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              dataChip('රාශිය', sign),
              const SizedBox(width: 8),
              dataChip('භාව අධිපති', lord),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              dataChip('අධිපති සිටින රාශිය', lordSign),
              const SizedBox(width: 8),
              dataChip('අධිපතිගේ භාවය', lordHouse),
            ],
          ),
          if (translatedPlanets.isNotEmpty) ...[
            const SizedBox(height: 14),
            Wrap(
              spacing: 7,
              runSpacing: 7,
              children: translatedPlanets.map((planet) {
                return Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 11,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF3CD),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    planet,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                    ),
                  ),
                );
              }).toList(),
            ),
          ] else ...[
            const SizedBox(height: 12),
            Text(
              'මෙම භාවයේ සෘජුව පිහිටි ග්‍රහයෙක් නොමැත.',
              style: TextStyle(
                color: Colors.grey.shade600,
                fontSize: 14,
              ),
            ),
          ],
          if (text != '-') ...[
            const SizedBox(height: 13),
            Text(
              text,
              style: const TextStyle(
                fontSize: 15,
                height: 1.55,
                color: Colors.black87,
              ),
            ),
          ],
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> interpretation =
        (chartData['interpretation'] as Map<String, dynamic>?) ?? {};

    final Map<String, dynamic> lagna =
        (interpretation['lagna'] as Map<String, dynamic>?) ?? {};

    final Map<String, dynamic> moon =
        (interpretation['moon'] as Map<String, dynamic>?) ?? {};

    final List<dynamic> planets =
        (interpretation['planets'] as List<dynamic>?) ?? [];

    final List<dynamic> houses =
        (interpretation['houses'] as List<dynamic>?) ?? [];

    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        title: const Text(
          'ජන්ම පත්‍ර විශ්ලේෂණය',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: primary,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [
                    primary,
                    Color(0xFF8E24AA),
                  ],
                ),
                borderRadius: BorderRadius.circular(22),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '🔮 තරුමග විශ්ලේෂණය',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 23,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'ඔබේ ජන්ම පත්‍රයේ ප්‍රධාන කරුණු සරලව බලන්න.',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 15,
                      height: 1.5,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 25),
            sectionTitle(
              'ලග්න විශ්ලේෂණය',
              Icons.person_outline,
            ),
            if (lagna.isEmpty)
              infoCard(
                title: 'ලග්න දත්ත නොමැත',
                text: 'Lagna interpretation data ලබාගෙන නොමැත.',
                icon: Icons.info_outline,
              )
            else
              buildLagnaCard(lagna),
            const SizedBox(height: 25),
            sectionTitle(
              'සඳු සහ මානසික ස්වභාවය',
              Icons.nightlight_round,
            ),
            if (moon.isEmpty)
              infoCard(
                title: 'සඳු දත්ත නොමැත',
                text: 'Moon interpretation data ලබාගෙන නොමැත.',
                icon: Icons.info_outline,
              )
            else
              buildMoonCard(moon),
            const SizedBox(height: 25),
            sectionTitle(
              'ග්‍රහ විශ්ලේෂණය',
              Icons.public,
            ),
            const SizedBox(height: 4),
            if (planets.isEmpty)
              infoCard(
                title: 'ග්‍රහ දත්ත නොමැත',
                text: 'Planet interpretation data ලබාගෙන නොමැත.',
                icon: Icons.info_outline,
              )
            else
              ...planets.map((planetData) {
                return buildPlanetCard(
                  planetData as Map<String, dynamic>,
                );
              }),
            const SizedBox(height: 25),
            sectionTitle(
              'භාව සහ භාව අධිපති විශ්ලේෂණය',
              Icons.home_work_outlined,
            ),
            const SizedBox(height: 5),
            if (houses.isEmpty)
              infoCard(
                title: 'භාව දත්ත නොමැත',
                text:
                    'භාව විශ්ලේෂණ දත්ත ලබාගෙන නොමැත. Backend interpretation engine එක පරීක්ෂා කරන්න.',
                icon: Icons.info_outline,
              )
            else
              ...houses.map((houseData) {
                return buildHouseCard(
                  houseData as Map<String, dynamic>,
                );
              }),
            const SizedBox(height: 20),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(17),
              decoration: BoxDecoration(
                color: const Color(0xFFEDE7F6),
                borderRadius: BorderRadius.circular(18),
              ),
              child: const Text(
                '🌟 TharuMaga — ඔබේ තරු මඟ කියවමු',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: darkPurple,
                  fontSize: 15,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
