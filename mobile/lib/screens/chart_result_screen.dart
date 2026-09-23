import 'package:flutter/material.dart';

import 'd1_chart_screen.dart';
import 'planet_positions_screen.dart';
import 'dasha_screen.dart';
import 'interpretation_screen.dart';
import 'yogas_screen.dart';
import '../models/yoga_model.dart';

class ChartResultScreen extends StatelessWidget {
  final Map<String, dynamic> chartData;

  const ChartResultScreen({
    super.key,
    required this.chartData,
  });

  // =============================================================
  // රාශි නාම Sinhala
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
  // නක්ෂත්‍ර නාම Sinhala
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
  // ග්‍රහ නාම Sinhala
  // =============================================================

  String translatePlanet(dynamic value) {
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

    return planets[value?.toString()] ?? value?.toString() ?? '-';
  }

  // =============================================================
  // Calculation system translations
  // =============================================================

  String translateSystem(String key, dynamic value) {
    final text = value?.toString() ?? '-';

    switch (key) {
      case 'zodiac':
        if (text == 'Sidereal') {
          return 'නිරයන';
        }
        return text;

      case 'ayanamsa':
        if (text == 'Lahiri') {
          return 'ලහිරි';
        }
        return text;

      case 'rahu':
        if (text == 'True Node') {
          return 'සත්‍ය රාහු';
        }
        return text;

      case 'ketu':
        if (text == '180° opposite Rahu') {
          return 'රාහුට අංශක 180ක් විරුද්ධ කේතු';
        }
        return text;

      case 'house_system':
        if (text == 'Whole Sign') {
          return 'පූර්ණ රාශි භාව ක්‍රමය';
        }
        return text;

      case 'dasha_system':
        if (text == 'Vimshottari') {
          return 'විංශෝත්තරී දශා ක්‍රමය';
        }
        return text;

      default:
        return text;
    }
  }

  // =============================================================
  // Number format
  // =============================================================

  String formatNumber(dynamic value) {
    if (value == null) {
      return '-';
    }

    if (value is num) {
      return value.toStringAsFixed(4);
    }

    return value.toString();
  }

  // =============================================================
  // Degree format
  //
  // Backend gives absolute zodiac longitude.
  // Example:
  // 201.361211887° -> 21°21′40″
  // =============================================================

  String formatSignDegrees(dynamic value) {
    if (value == null) {
      return '-';
    }

    if (value is num) {
      double totalDegrees = value.toDouble() % 30;

      int degrees = totalDegrees.floor();

      double remainingMinutes = (totalDegrees - degrees) * 60;

      int minutes = remainingMinutes.floor();

      int seconds = ((remainingMinutes - minutes) * 60).round();

      // Handle rounding overflow.
      if (seconds == 60) {
        seconds = 0;
        minutes++;
      }

      if (minutes == 60) {
        minutes = 0;
        degrees++;
      }

      // Safety for a possible 30° rounding result.
      if (degrees == 30) {
        degrees = 0;
      }

      return '$degrees°'
          '${minutes.toString().padLeft(2, '0')}′'
          '${seconds.toString().padLeft(2, '0')}″';
    }

    return value.toString();
  }

  // =============================================================
  // YOGA DATA
  // =============================================================

  List<YogaModel> _getYogas() {
    final yogaData = chartData['yoga_interpretation'];

    if (yogaData is! Map) {
      return [];
    }

    final interpretations = yogaData['interpretations'];

    if (interpretations is! List) {
      return [];
    }

    return interpretations
        .whereType<Map>()
        .map(
          (item) => YogaModel.fromJson(
            Map<String, dynamic>.from(item),
          ),
        )
        .toList();
  }

  // =============================================================
  // BUILD
  // =============================================================

  @override
  Widget build(BuildContext context) {
    final engine = chartData['engine'] ?? {};
    final birth = chartData['birth'] ?? {};
    final lagna = chartData['lagna'] ?? {};
    final nakshatra = lagna['nakshatra'] ?? {};

    return Scaffold(
      backgroundColor: const Color(0xFFF8F5FC),

      // =========================================================
      // APP BAR
      // =========================================================

      appBar: AppBar(
        title: const Text(
          'ජන්ම පත්‍රය',
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
        padding: const EdgeInsets.all(20),
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
                  colors: [
                    Color(0xFF6A1B9A),
                    Color(0xFF8E24AA),
                  ],
                ),
                borderRadius: BorderRadius.circular(22),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '✨ ඔබේ ජන්ම පත්‍රය',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    birth['place']?.toString() ?? '',
                    style: const TextStyle(
                      color: Colors.white70,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 22),

            // ===================================================
            // LAGNA
            // ===================================================

            const _SectionTitle(
              icon: Icons.auto_awesome,
              title: 'ලග්නය',
            ),

            const SizedBox(height: 10),

            _InfoCard(
              children: [
                _InfoRow(
                  label: 'ලග්නය',
                  value: translateSign(
                    lagna['sign'],
                  ),
                ),
                _InfoRow(
                  label: 'අංශක',
                  value: formatSignDegrees(
                    lagna['longitude'],
                  ),
                ),
                _InfoRow(
                  label: 'නක්ෂත්‍රය',
                  value: translateNakshatra(
                    nakshatra['name'],
                  ),
                ),
                _InfoRow(
                  label: 'නක්ෂත්‍ර අධිපති',
                  value: translatePlanet(
                    nakshatra['lord'],
                  ),
                ),
                _InfoRow(
                  label: 'පාදය',
                  value: nakshatra['pada']?.toString() ?? '-',
                ),
              ],
            ),

            const SizedBox(height: 24),

            // ===================================================
            // BIRTH DETAILS
            // ===================================================

            const _SectionTitle(
              icon: Icons.person,
              title: 'උපන් තොරතුරු',
            ),

            const SizedBox(height: 10),

            _InfoCard(
              children: [
                _InfoRow(
                  label: 'දිනය',
                  value: birth['date']?.toString() ?? '-',
                ),
                _InfoRow(
                  label: 'දේශීය වේලාව',
                  value: birth['local_time']?.toString() ?? '-',
                ),
                _InfoRow(
                  label: 'වේලා කලාපය',
                  value: birth['timezone']?.toString() ?? '-',
                ),
                _InfoRow(
                  label: 'ස්ථානය',
                  value: birth['place']?.toString() ?? '-',
                ),
              ],
            ),

            const SizedBox(height: 24),

            // ===================================================
            // CALCULATION SYSTEM
            // ===================================================

            const _SectionTitle(
              icon: Icons.settings_suggest,
              title: 'ගණනය කිරීමේ ක්‍රමය',
            ),

            const SizedBox(height: 10),

            _InfoCard(
              children: [
                _InfoRow(
                  label: 'රාශි ක්‍රමය',
                  value: translateSystem(
                    'zodiac',
                    engine['zodiac'],
                  ),
                ),
                _InfoRow(
                  label: 'අයනාංශය',
                  value: translateSystem(
                    'ayanamsa',
                    engine['ayanamsa'],
                  ),
                ),
                _InfoRow(
                  label: 'රාහු',
                  value: translateSystem(
                    'rahu',
                    engine['rahu'],
                  ),
                ),
                _InfoRow(
                  label: 'කේතු',
                  value: translateSystem(
                    'ketu',
                    engine['ketu'],
                  ),
                ),
                _InfoRow(
                  label: 'භාව ක්‍රමය',
                  value: translateSystem(
                    'house_system',
                    engine['house_system'],
                  ),
                ),
                _InfoRow(
                  label: 'දශා ක්‍රමය',
                  value: translateSystem(
                    'dasha_system',
                    engine['dasha_system'],
                  ),
                ),
              ],
            ),

            const SizedBox(height: 30),

            // ===================================================
            // INTERPRETATION BUTTON
            // ===================================================

            SizedBox(
              width: double.infinity,
              height: 58,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => InterpretationScreen(
                        chartData: chartData,
                      ),
                    ),
                  );
                },
                icon: const Icon(
                  Icons.auto_awesome,
                ),
                label: const Text(
                  '🔮 ජන්ම පත්‍ර විශ්ලේෂණය බලන්න',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4A148C),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 12),

            // ===================================================
            // PLANET POSITIONS BUTTON
            // ===================================================

            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => PlanetPositionsScreen(
                        chartData: chartData,
                      ),
                    ),
                  );
                },
                icon: const Icon(
                  Icons.arrow_forward,
                ),
                label: const Text(
                  'ග්‍රහ පිහිටීම් බලන්න',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A1B9A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 12),

            // ===================================================
            // D1 CHART BUTTON
            // ===================================================

            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => D1ChartScreen(
                        chartData: chartData,
                      ),
                    ),
                  );
                },
                icon: const Icon(
                  Icons.grid_4x4,
                ),
                label: const Text(
                  'D1 රාශි චක්‍රය බලන්න',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF8E24AA),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 12),

            // ===================================================
            // DASHA BUTTON
            // ===================================================

            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => DashaScreen(
                        chartData: chartData,
                      ),
                    ),
                  );
                },
                icon: const Icon(
                  Icons.auto_awesome,
                ),
                label: const Text(
                  'දශා විස්තර බලන්න',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A1B9A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 12),

            // ===================================================
            // YOGA BUTTON
            // ===================================================

            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: () {
                  final yogas = _getYogas();

                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => YogasScreen(
                        yogas: yogas,
                      ),
                    ),
                  );
                },
                icon: const Icon(
                  Icons.auto_awesome,
                ),
                label: const Text(
                  'යෝග විස්තර බලන්න',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4A148C),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 25),
          ],
        ),
      ),
    );
  }
}

// =================================================================
// SECTION TITLE
// =================================================================

class _SectionTitle extends StatelessWidget {
  final IconData icon;
  final String title;

  const _SectionTitle({
    required this.icon,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          icon,
          color: const Color(0xFF6A1B9A),
        ),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Color(0xFF4A148C),
          ),
        ),
      ],
    );
  }
}

// =================================================================
// INFO CARD
// =================================================================

class _InfoCard extends StatelessWidget {
  final List<Widget> children;

  const _InfoCard({
    required this.children,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: children,
      ),
    );
  }
}

// =================================================================
// INFO ROW
// =================================================================

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;

  const _InfoRow({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(
        vertical: 7,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 2,
            child: Text(
              label,
              style: const TextStyle(
                fontSize: 14,
                color: Colors.black54,
              ),
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            flex: 3,
            child: Text(
              value,
              textAlign: TextAlign.right,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
