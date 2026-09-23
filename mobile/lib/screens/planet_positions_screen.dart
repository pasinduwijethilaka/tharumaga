import 'package:flutter/material.dart';

class PlanetPositionsScreen extends StatelessWidget {
  final Map<String, dynamic> chartData;

  const PlanetPositionsScreen({
    super.key,
    required this.chartData,
  });

  // =============================================================
  // රාශි Sinhala
  // =============================================================

  String translateSign(dynamic value) {
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

    return signs[value?.toString()] ?? value?.toString() ?? '-';
  }

  // =============================================================
  // ග්‍රහ නාම Sinhala
  // =============================================================

  String translatePlanet(String value) {
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

    return planets[value] ?? value;
  }

  // =============================================================
  // නක්ෂත්‍ර Sinhala
  // =============================================================

  String translateNakshatra(dynamic value) {
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
      'Magha': 'මා',
      'Purva Phalguni': 'පුවපල්',
      'Uttara Phalguni': 'උත්‍රපල්',
      'Hasta': 'හත',
      'Chitra': 'සිත',
      'Swati': 'ස්වාති',
      'Vishakha': 'විශාඛා',
      'Anuradha': 'අනුරාධා',
      'Jyeshtha': 'ජ්‍යෙෂ්ඨා',
      'Mula': 'මූල',
      'Purva Ashadha': 'පුවසල',
      'Uttara Ashadha': 'උත්‍රසල',
      'Shravana': 'සුවණ',
      'Dhanishta': 'දෙනට',
      'Shatabhisha': 'සියාවස',
      'Purva Bhadrapada': 'පුවපුටුප',
      'Uttara Bhadrapada': 'උත්‍රපුටුප',
      'Revati': 'රේවතී',
    };

    return nakshatras[value?.toString()] ?? value?.toString() ?? '-';
  }

  // =============================================================
  // අංශක format
  // Example: 265.03° -> 25°01′46″
  // =============================================================

  String formatDegrees(dynamic value) {
    if (value == null) {
      return '-';
    }

    if (value is num) {
      double totalDegrees = value.toDouble() % 30;

      int degrees = totalDegrees.floor();

      double remainingMinutes = (totalDegrees - degrees) * 60;

      int minutes = remainingMinutes.floor();

      int seconds = ((remainingMinutes - minutes) * 60).round();

      if (seconds == 60) {
        seconds = 0;
        minutes++;
      }

      if (minutes == 60) {
        minutes = 0;
        degrees++;
      }

      return '$degrees°'
          '${minutes.toString().padLeft(2, '0')}′'
          '${seconds.toString().padLeft(2, '0')}″';
    }

    return value.toString();
  }

  // =============================================================
  // Planet symbols
  // =============================================================

  String planetSymbol(String planet) {
    const symbols = {
      'Sun': '☉',
      'Moon': '☽',
      'Mars': '♂',
      'Mercury': '☿',
      'Jupiter': '♃',
      'Venus': '♀',
      'Saturn': '♄',
      'Rahu': '☊',
      'Ketu': '☋',
    };

    return symbols[planet] ?? '✦';
  }

  // =============================================================
  // Planet Card
  // =============================================================

  Widget planetCard(
    String planetKey,
    Map<String, dynamic> planet,
  ) {
    final nakshatra = planet['nakshatra'] is Map
        ? Map<String, dynamic>.from(
            planet['nakshatra'],
          )
        : <String, dynamic>{};

    final bool retrograde = planet['retrograde'] == true;

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.06),
            blurRadius: 12,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // =====================================================
          // PLANET HEADER
          // =====================================================

          Row(
            children: [
              Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [
                      Color(0xFFEDE0F5),
                      Color(0xFFF5EAF9),
                    ],
                  ),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: Center(
                  child: Text(
                    planetSymbol(planetKey),
                    style: const TextStyle(
                      fontSize: 25,
                      color: Color(0xFF6A1B9A),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 13),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      translatePlanet(planetKey),
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF4A148C),
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      planetKey,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
              if (retrograde)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF3E0),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                      color: const Color(
                        0xFFFFCC80,
                      ),
                    ),
                  ),
                  child: const Text(
                    'වක්‍ර',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFFE65100),
                    ),
                  ),
                ),
            ],
          ),

          const SizedBox(height: 18),

          // =====================================================
          // MAIN SIGN
          // =====================================================

          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(
              horizontal: 15,
              vertical: 13,
            ),
            decoration: BoxDecoration(
              color: const Color(0xFFF8F1FC),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Row(
              children: [
                const Text(
                  'රාශිය',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.black54,
                  ),
                ),
                const Spacer(),
                Text(
                  translateSign(planet['sign']),
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF6A1B9A),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 12),

          // =====================================================
          // DETAILS
          // =====================================================

          _PlanetRow(
            label: 'අංශක',
            value: formatDegrees(
              planet['longitude'],
            ),
            highlight: true,
          ),

          _PlanetRow(
            label: 'නක්ෂත්‍රය',
            value: translateNakshatra(
              nakshatra['name'],
            ),
          ),

          _PlanetRow(
            label: 'නක්ෂත්‍ර අධිපති',
            value: translatePlanet(
              nakshatra['lord']?.toString() ?? '-',
            ),
          ),

          _PlanetRow(
            label: 'පාදය',
            value: nakshatra['pada']?.toString() ?? '-',
          ),

          _PlanetRow(
            label: 'භාවය',
            value: planet['house'] != null ? '${planet['house']} වන භාවය' : '-',
          ),

          _PlanetRow(
            label: 'චලනය',
            value: retrograde ? 'වක්‍ර ගමනය' : 'සාමාන්‍ය ගමනය',
            last: true,
          ),
        ],
      ),
    );
  }

  // =============================================================
  // BUILD
  // =============================================================

  @override
  Widget build(BuildContext context) {
    final planets = chartData['planets'] is Map
        ? Map<String, dynamic>.from(
            chartData['planets'],
          )
        : <String, dynamic>{};

    final rahu = chartData['rahu'] is Map
        ? Map<String, dynamic>.from(
            chartData['rahu'],
          )
        : <String, dynamic>{};

    final ketu = chartData['ketu'] is Map
        ? Map<String, dynamic>.from(
            chartData['ketu'],
          )
        : <String, dynamic>{};

    const planetOrder = [
      'Sun',
      'Moon',
      'Mars',
      'Mercury',
      'Jupiter',
      'Venus',
      'Saturn',
    ];

    return Scaffold(
      backgroundColor: const Color(0xFFF8F5FC),

      // =========================================================
      // APP BAR
      // =========================================================

      appBar: AppBar(
        title: const Text(
          'ග්‍රහ පිහිටීම්',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),

      // =========================================================
      // BODY
      // =========================================================

      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(
          18,
          8,
          18,
          30,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ===================================================
            // HEADER
            // ===================================================

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(22),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Color(0xFF6A1B9A),
                    Color(0xFF8E24AA),
                  ],
                ),
                borderRadius: BorderRadius.circular(22),
                boxShadow: [
                  BoxShadow(
                    color: const Color(
                      0xFF6A1B9A,
                    ).withOpacity(0.20),
                    blurRadius: 14,
                    offset: const Offset(0, 7),
                  ),
                ],
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '✨ ග්‍රහ පිහිටීම්',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'ඔබගේ ජන්ම පත්‍රයේ ග්‍රහයන්ගේ පිහිටීම',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 26),

            // ===================================================
            // 7 PLANETS
            // ===================================================

            const Text(
              'නවග්‍රහ පිහිටීම්',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Color(0xFF4A148C),
              ),
            ),

            const SizedBox(height: 14),

            ...planetOrder.map(
              (planetName) {
                final planet = planets[planetName];

                if (planet == null || planet is! Map) {
                  return const SizedBox.shrink();
                }

                return planetCard(
                  planetName,
                  Map<String, dynamic>.from(
                    planet,
                  ),
                );
              },
            ),

            // ===================================================
            // RAHU
            // ===================================================

            if (rahu.isNotEmpty) ...[
              const SizedBox(height: 4),
              planetCard(
                'Rahu',
                rahu,
              ),
            ],

            // ===================================================
            // KETU
            // ===================================================

            if (ketu.isNotEmpty)
              planetCard(
                'Ketu',
                ketu,
              ),

            const SizedBox(height: 10),
          ],
        ),
      ),
    );
  }
}

// =================================================================
// PLANET ROW
// =================================================================

class _PlanetRow extends StatelessWidget {
  final String label;
  final String value;
  final bool highlight;
  final bool last;

  const _PlanetRow({
    required this.label,
    required this.value,
    this.highlight = false,
    this.last = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        vertical: 10,
      ),
      decoration: BoxDecoration(
        border: last
            ? null
            : Border(
                bottom: BorderSide(
                  color: Colors.grey.shade200,
                ),
              ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            flex: 2,
            child: Text(
              label,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade700,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            flex: 3,
            child: Text(
              value,
              textAlign: TextAlign.right,
              style: TextStyle(
                fontSize: highlight ? 16 : 14,
                fontWeight: FontWeight.w600,
                color: highlight ? const Color(0xFF6A1B9A) : Colors.black87,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
