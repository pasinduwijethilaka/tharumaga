import 'package:flutter/material.dart';

class DashaScreen extends StatefulWidget {
  final Map<String, dynamic> chartData;

  const DashaScreen({
    super.key,
    required this.chartData,
  });

  @override
  State<DashaScreen> createState() => _DashaScreenState();
}

class _DashaScreenState extends State<DashaScreen> {
  // =============================================================
  // Sinhala Planet Names
  // =============================================================

  String planetName(dynamic value) {
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
  // Sinhala Nakshatra Names
  // =============================================================

  String nakshatraName(dynamic value) {
    const nakshatras = {
      'Ashwini': 'අශ්විනී',
      'Bharani': 'භරණී',
      'Krittika': 'කෘත්තිකා',
      'Rohini': 'රෝහිණී',
      'Mrigashira': 'මෘගශීර්ෂ',
      'Ardra': 'ආර්ද්‍රා',
      'Punarvasu': 'පුනර්වසු',
      'Pushya': 'පුෂ්‍ය',
      'Ashlesha': 'අශ්ලේෂා',
      'Magha': 'මාඝා',
      'Purva Phalguni': 'පූර්වඵල්ගුණී',
      'Uttara Phalguni': 'උත්තරඵල්ගුණී',
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
      'Purva Bhadrapada': 'පූර්ව භාද්‍රපද',
      'Uttara Bhadrapada': 'උත්තර භාද්‍රපද',
      'Revati': 'රේවතී',
    };

    return nakshatras[value?.toString()] ?? value?.toString() ?? '-';
  }

  String translateNakshatraText(String text) {
    var result = text;
    const nakshatras = {
      'Ashwini': 'අශ්විනී',
      'Bharani': 'භරණී',
      'Krittika': 'කෘත්තිකා',
      'Rohini': 'රෝහිණී',
      'Mrigashira': 'මෘගශීර්ෂ',
      'Ardra': 'ආර්ද්‍රා',
      'Punarvasu': 'පුනර්වසු',
      'Pushya': 'පුෂ්‍ය',
      'Ashlesha': 'අශ්ලේෂා',
      'Magha': 'මාඝා',
      'Purva Phalguni': 'පූර්වඵල්ගුණී',
      'Uttara Phalguni': 'උත්තරඵල්ගුණී',
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
      'Purva Bhadrapada': 'පූර්ව භාද්‍රපද',
      'Uttara Bhadrapada': 'උත්තර භාද්‍රපද',
      'Revati': 'රේවතී',
    };

    for (final entry in nakshatras.entries) {
      result = result.replaceAll(entry.key, entry.value);
    }

    return result;
  }

  // =============================================================
  // Planet Symbols
  // =============================================================

  String planetSymbol(String value) {
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

    return symbols[value] ?? '✦';
  }

  // =============================================================
  // Format Date
  // =============================================================

  String formatDate(dynamic value) {
    if (value == null) {
      return '-';
    }

    final text = value.toString();

    if (text.length >= 10) {
      final parts = text.substring(0, 10).split('-');

      if (parts.length == 3) {
        return '${parts[2]}/${parts[1]}/${parts[0]}';
      }
    }

    return text;
  }

  // =============================================================
  // Format Years
  // =============================================================

  String formatYears(dynamic value) {
    if (value == null) {
      return '-';
    }

    if (value is num) {
      return value.toStringAsFixed(2);
    }

    return value.toString();
  }

  // =============================================================
  // Check Date Range
  // =============================================================

  bool isDateInRange(
    DateTime today,
    dynamic startValue,
    dynamic endValue,
  ) {
    if (startValue == null || endValue == null) {
      return false;
    }

    final start = DateTime.tryParse(
      startValue.toString(),
    );

    final end = DateTime.tryParse(
      endValue.toString(),
    );

    if (start == null || end == null) {
      return false;
    }

    final endInclusive = end.add(
      const Duration(days: 1),
    );

    return !today.isBefore(start) && today.isBefore(endInclusive);
  }

  // =============================================================
  // Find Current Dasha
  //
  // Returns:
  // mahadasha
  // antardasha
  // pratyantardasha
  // =============================================================

  Map<String, dynamic>? getCurrentDasha(
    List<dynamic> dashas,
  ) {
    final today = DateTime.now();

    for (final dashaItem in dashas) {
      if (dashaItem is! Map) {
        continue;
      }

      final dasha = Map<String, dynamic>.from(
        dashaItem,
      );

      // ---------------------------------------------------------
      // Current Mahadasha
      // ---------------------------------------------------------

      if (!isDateInRange(
        today,
        dasha['start'],
        dasha['end'],
      )) {
        continue;
      }

      // ---------------------------------------------------------
      // Find Current Antardasha
      // ---------------------------------------------------------

      final antardashas = dasha['antardasha'] is List
          ? List<dynamic>.from(
              dasha['antardasha'],
            )
          : <dynamic>[];

      Map<String, dynamic>? currentAntardasha;

      Map<String, dynamic>? currentPratyantardasha;

      for (final antardashaItem in antardashas) {
        if (antardashaItem is! Map) {
          continue;
        }

        final antardasha = Map<String, dynamic>.from(
          antardashaItem,
        );

        if (!isDateInRange(
          today,
          antardasha['start'],
          antardasha['end'],
        )) {
          continue;
        }

        currentAntardasha = antardasha;

        // -------------------------------------------------------
        // Find Current Pratyantardasha
        // -------------------------------------------------------

        final pratyantardashas = antardasha['pratyantardasha'] is List
            ? List<dynamic>.from(
                antardasha['pratyantardasha'],
              )
            : <dynamic>[];

        for (final pratyItem in pratyantardashas) {
          if (pratyItem is! Map) {
            continue;
          }

          final praty = Map<String, dynamic>.from(
            pratyItem,
          );

          if (isDateInRange(
            today,
            praty['start'],
            praty['end'],
          )) {
            currentPratyantardasha = praty;
            break;
          }
        }

        break;
      }

      return {
        'mahadasha': dasha,
        'antardasha': currentAntardasha,
        'pratyantardasha': currentPratyantardasha,
      };
    }

    return null;
  }

  // =============================================================
  // Current Dasha Card
  // =============================================================

  Widget currentDashaCard(
    Map<String, dynamic> mahadasha,
    Map<String, dynamic>? antardasha,
    Map<String, dynamic>? pratyantardasha,
  ) {
    final mahaLord = mahadasha['lord']?.toString() ?? '-';

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(19),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFF6A1B9A),
            Color(0xFF8E24AA),
          ],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: const Color(
              0xFF6A1B9A,
            ).withOpacity(0.20),
            blurRadius: 14,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // =====================================================
          // TITLE
          // =====================================================

          const Row(
            children: [
              Icon(
                Icons.auto_awesome,
                color: Colors.white,
                size: 20,
              ),
              SizedBox(width: 8),
              Text(
                'දැනට ක්‍රියාත්මක දශාව',
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),

          const SizedBox(height: 15),

          // =====================================================
          // MAHADASHA
          // =====================================================

          Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(
                    0.14,
                  ),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Center(
                  child: Text(
                    planetSymbol(mahaLord),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 23,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'මහ දශාව',
                      style: TextStyle(
                        color: Colors.white70,
                        fontSize: 11,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      '${planetName(mahaLord)} මහ දශාව',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 21,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${formatDate(mahadasha['start'])} → ${formatDate(mahadasha['end'])}',
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 11,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),

          // =====================================================
          // ANTARDASHA
          // =====================================================

          if (antardasha != null) ...[
            const SizedBox(height: 14),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(13),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(
                  0.12,
                ),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(
                children: [
                  Container(
                    width: 38,
                    height: 38,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(
                        0.10,
                      ),
                      borderRadius: BorderRadius.circular(
                        10,
                      ),
                    ),
                    child: Center(
                      child: Text(
                        planetSymbol(
                          antardasha['lord']?.toString() ?? '',
                        ),
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 19,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'අන්තර් දශාව',
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 10,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '${planetName(mahaLord)} / ${planetName(antardasha['lord'])}',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '${formatDate(antardasha['start'])} → ${formatDate(antardasha['end'])}',
                          style: const TextStyle(
                            color: Colors.white70,
                            fontSize: 10,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],

          // =====================================================
          // PRATYANTARDASHA
          // =====================================================

          if (pratyantardasha != null) ...[
            const SizedBox(height: 10),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(13),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(
                  0.18,
                ),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(
                children: [
                  Container(
                    width: 38,
                    height: 38,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(
                        0.10,
                      ),
                      borderRadius: BorderRadius.circular(
                        10,
                      ),
                    ),
                    child: Center(
                      child: Text(
                        planetSymbol(
                          pratyantardasha['lord']?.toString() ?? '',
                        ),
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 19,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'ප්‍රත්‍යන්තර දශාව',
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 10,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '${planetName(mahaLord)} / ${planetName(antardasha?['lord'])} / ${planetName(pratyantardasha['lord'])}',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '${formatDate(pratyantardasha['start'])} → ${formatDate(pratyantardasha['end'])}',
                          style: const TextStyle(
                            color: Colors.white70,
                            fontSize: 10,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  // =============================================================
  // Dasha Interpretation Card
  // =============================================================

  // =============================================================
  // Dasha Interpretation Card
  // =============================================================

  Widget dashaInterpretationCard(
    Map<String, dynamic> dashaInterpretation,
  ) {
    final current = dashaInterpretation['current'] is Map
        ? Map<String, dynamic>.from(
            dashaInterpretation['current'],
          )
        : <String, dynamic>{};

    final mahadasha = current['mahadasha'] is Map
        ? Map<String, dynamic>.from(
            current['mahadasha'],
          )
        : null;

    final antardasha = current['antardasha'] is Map
        ? Map<String, dynamic>.from(
            current['antardasha'],
          )
        : null;

    final pratyantardasha = current['pratyantardasha'] is Map
        ? Map<String, dynamic>.from(
            current['pratyantardasha'],
          )
        : null;

    final combinedText = dashaInterpretation['combined_text']?.toString() ?? '';

    Widget infoChip(String label, String value) {
      if (value.trim().isEmpty || value == '-') {
        return const SizedBox.shrink();
      }

      return Container(
        padding: const EdgeInsets.symmetric(
          horizontal: 9,
          vertical: 7,
        ),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(
            color: const Color(0xFFE4D5EC),
          ),
        ),
        child: RichText(
          text: TextSpan(
            children: [
              TextSpan(
                text: '$label: ',
                style: const TextStyle(
                  fontSize: 11,
                  color: Color(0xFF7A6883),
                  fontWeight: FontWeight.w500,
                ),
              ),
              TextSpan(
                text: value,
                style: const TextStyle(
                  fontSize: 11,
                  color: Color(0xFF4A148C),
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      );
    }

    Widget interpretationBlock({
      required String title,
      required String subtitle,
      required String planet,
      required Map<String, dynamic> data,
      required String text,
      required Color backgroundColor,
      required IconData icon,
    }) {
      final sign = data['sign_si']?.toString() ?? '';
      final house = data['house']?.toString() ?? '';
      final signLord = data['sign_lord_si']?.toString() ?? '';
      final signLordHouse = data['sign_lord_house']?.toString() ?? '';
      final nakshatra = nakshatraName(data['nakshatra']);
      final nakshatraLord = data['nakshatra_lord_si']?.toString() ?? '';
      final pada = data['pada']?.toString() ?? '';
      final retrograde = data['retrograde'] == true;

      return Container(
        width: double.infinity,
        margin: const EdgeInsets.only(bottom: 14),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: backgroundColor,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(
            color: const Color(0xFFE8D9F0),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // -------------------------------------------------------
            // CARD HEADER
            // -------------------------------------------------------

            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [
                        Color(0xFF6A1B9A),
                        Color(0xFF8E24AA),
                      ],
                    ),
                    borderRadius: BorderRadius.circular(13),
                  ),
                  child: Center(
                    child: Text(
                      planetSymbol(planet),
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 21,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 11),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF4A148C),
                        ),
                      ),
                      const SizedBox(height: 3),
                      Text(
                        subtitle,
                        style: TextStyle(
                          fontSize: 11,
                          color: Colors.grey.shade600,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),

            const SizedBox(height: 14),

            // -------------------------------------------------------
            // PLANET PLACEMENT
            // -------------------------------------------------------

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.72),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(
                        Icons.my_location_outlined,
                        size: 16,
                        color: Color(0xFF6A1B9A),
                      ),
                      SizedBox(width: 6),
                      Text(
                        'ග්‍රහ පිහිටීම',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF4A148C),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 9),
                  Wrap(
                    spacing: 7,
                    runSpacing: 7,
                    children: [
                      infoChip(
                        'ග්‍රහය',
                        planetName(planet),
                      ),
                      infoChip(
                        'රාශිය',
                        sign,
                      ),
                      infoChip(
                        'භාවය',
                        house.isNotEmpty ? '$house වන භාවය' : '',
                      ),
                      infoChip(
                        'රාශි අධිපති',
                        signLord,
                      ),
                      infoChip(
                        'අධිපතිගේ භාවය',
                        signLordHouse.isNotEmpty
                            ? '$signLordHouse වන භාවය'
                            : '',
                      ),
                      infoChip(
                        'නක්ෂත්‍රය',
                        nakshatra,
                      ),
                      infoChip(
                        'නක්ෂත්‍ර අධිපති',
                        nakshatraLord,
                      ),
                      infoChip(
                        'පාදය',
                        pada.isNotEmpty ? pada : '',
                      ),
                      if (retrograde)
                        infoChip(
                          'ගමනය',
                          'වක්‍ර',
                        ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 13),

            // -------------------------------------------------------
            // INTERPRETATION
            // -------------------------------------------------------

            const Row(
              children: [
                Icon(
                  Icons.auto_awesome,
                  size: 17,
                  color: Color(0xFF6A1B9A),
                ),
                SizedBox(width: 6),
                Text(
                  'විශ්ලේෂණය',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF4A148C),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 8),

            Text(
              text.isNotEmpty ? text : 'විශ්ලේෂණ දත්ත නොමැත.',
              style: const TextStyle(
                fontSize: 14,
                height: 1.7,
                color: Colors.black87,
              ),
            ),
          ],
        ),
      );
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(17),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 12,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ---------------------------------------------------------
          // CURRENT PERIOD SUMMARY
          // ---------------------------------------------------------

          if (combinedText.isNotEmpty) ...[
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Color(0xFFF3E5F5),
                    Color(0xFFFAF3FC),
                  ],
                ),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: const Color(0xFFE5D3ED),
                ),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Center(
                      child: Text(
                        '🔮',
                        style: TextStyle(fontSize: 21),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'දැනට පවතින දශා තේමාව',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF4A148C),
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          combinedText,
                          style: const TextStyle(
                            fontSize: 13,
                            height: 1.65,
                            color: Color(0xFF5D4667),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
          ],

          // ---------------------------------------------------------
          // MAHADASHA
          // ---------------------------------------------------------

          if (mahadasha != null)
            interpretationBlock(
              title: '${planetName(mahadasha['planet'])} මහ දශා විශ්ලේෂණය',
              subtitle: 'ප්‍රධාන කාල පරාසය',
              planet: mahadasha['planet']?.toString() ?? '',
              data: mahadasha,
              text: translateNakshatraText(mahadasha['text']?.toString() ?? ''),
              backgroundColor: const Color(0xFFFBF7FD),
              icon: Icons.auto_awesome,
            ),

          // ---------------------------------------------------------
          // ANTARDASHA
          // ---------------------------------------------------------

          if (antardasha != null)
            interpretationBlock(
              title: '${planetName(antardasha['planet'])} අන්තර් දශා විශ්ලේෂණය',
              subtitle: 'මහ දශාව තුළ ක්‍රියාත්මක උප කාලය',
              planet: antardasha['planet']?.toString() ?? '',
              data: antardasha,
              text:
                  translateNakshatraText(antardasha['text']?.toString() ?? ''),
              backgroundColor: const Color(0xFFFDF9FE),
              icon: Icons.account_tree_outlined,
            ),

          // ---------------------------------------------------------
          // PRATYANTARDASHA
          // ---------------------------------------------------------

          if (pratyantardasha != null)
            interpretationBlock(
              title:
                  '${planetName(pratyantardasha['planet'])} ප්‍රත්‍යන්තර දශා විශ්ලේෂණය',
              subtitle: 'කෙටි කාල පරාසයේ ක්‍රියාත්මක තේමාව',
              planet: pratyantardasha['planet']?.toString() ?? '',
              data: pratyantardasha,
              text: translateNakshatraText(
                  pratyantardasha['text']?.toString() ?? ''),
              backgroundColor: const Color(0xFFFFFBFF),
              icon: Icons.schedule_outlined,
            ),
        ],
      ),
    );
  }

  String currentPlacementText(
    Map<String, dynamic>? data,
  ) {
    if (data == null) {
      return '-';
    }

    final sign = data['sign_si']?.toString();
    final house = data['house']?.toString();

    if (sign != null && house != null) {
      return '$sign • $house වන භාවය';
    }

    if (sign != null) {
      return sign;
    }

    if (house != null) {
      return '$house වන භාවය';
    }

    return '-';
  }

  // =============================================================
  // Mahadasha Card
  // =============================================================

  Widget mahadashaCard(
    Map<String, dynamic> dasha,
    int index,
  ) {
    final lord = dasha['lord']?.toString() ?? '-';

    final start = dasha['start'];
    final end = dasha['end'];
    final years = dasha['years'];

    final antardasha = dasha['antardasha'] is List
        ? List<dynamic>.from(
            dasha['antardasha'],
          )
        : <dynamic>[];

    return Container(
      margin: const EdgeInsets.only(
        bottom: 16,
      ),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(
              0.06,
            ),
            blurRadius: 12,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          dividerColor: Colors.transparent,
        ),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(
            horizontal: 18,
            vertical: 8,
          ),
          childrenPadding: const EdgeInsets.fromLTRB(
            18,
            0,
            18,
            18,
          ),
          leading: Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: const Color(0xFFF1E4F8),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Center(
              child: Text(
                planetSymbol(lord),
                style: const TextStyle(
                  fontSize: 23,
                  color: Color(0xFF6A1B9A),
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          title: Text(
            '${index + 1}. ${planetName(lord)} මහ දශාව',
            style: const TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.bold,
              color: Color(0xFF4A148C),
            ),
          ),
          subtitle: Padding(
            padding: const EdgeInsets.only(
              top: 5,
            ),
            child: Text(
              '${formatDate(start)}  →  ${formatDate(end)}',
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey.shade600,
              ),
            ),
          ),
          children: [
            // ===================================================
            // MAHADASHA SUMMARY
            // ===================================================

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: const Color(0xFFF8F1FC),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(
                children: [
                  const Expanded(
                    child: Text(
                      'කාලය',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.black54,
                      ),
                    ),
                  ),
                  Text(
                    '${formatYears(years)} වසර',
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF6A1B9A),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 16),

            // ===================================================
            // ANTARDASHA TITLE
            // ===================================================

            const Row(
              children: [
                Icon(
                  Icons.account_tree_outlined,
                  size: 19,
                  color: Color(0xFF6A1B9A),
                ),
                SizedBox(width: 8),
                Text(
                  'අන්තර් දශා',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF4A148C),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 10),

            // ===================================================
            // ANTARDASHA LIST
            // ===================================================

            ...antardasha.asMap().entries.map(
              (entry) {
                final antardashaData = entry.value;

                if (antardashaData is! Map) {
                  return const SizedBox.shrink();
                }

                return antardashaCard(
                  Map<String, dynamic>.from(
                    antardashaData,
                  ),
                  entry.key,
                  lord,
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  // =============================================================
  // Antardasha Card
  // =============================================================

  Widget antardashaCard(
    Map<String, dynamic> data,
    int index,
    String mahadashaLord,
  ) {
    final lord = data['lord']?.toString() ?? '-';

    final start = data['start'];
    final end = data['end'];
    final years = data['years'];

    final pratyantardasha = data['pratyantardasha'] is List
        ? List<dynamic>.from(
            data['pratyantardasha'],
          )
        : <dynamic>[];

    return Container(
      margin: const EdgeInsets.only(
        top: 8,
      ),
      decoration: BoxDecoration(
        border: Border.all(
          color: Colors.grey.shade200,
        ),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          dividerColor: Colors.transparent,
        ),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(
            horizontal: 12,
            vertical: 4,
          ),
          childrenPadding: const EdgeInsets.fromLTRB(
            12,
            0,
            12,
            12,
          ),
          leading: Container(
            width: 38,
            height: 38,
            decoration: BoxDecoration(
              color: const Color(0xFFF8F1FC),
              borderRadius: BorderRadius.circular(11),
            ),
            child: Center(
              child: Text(
                planetSymbol(lord),
                style: const TextStyle(
                  fontSize: 18,
                  color: Color(0xFF8E24AA),
                ),
              ),
            ),
          ),
          title: Text(
            '${planetName(mahadashaLord)} / ${planetName(lord)}',
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
          ),
          subtitle: Text(
            '${formatDate(start)} → ${formatDate(end)}',
            style: TextStyle(
              fontSize: 11,
              color: Colors.grey.shade600,
            ),
          ),
          children: [
            Row(
              children: [
                const Text(
                  'කාලය: ',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.black54,
                  ),
                ),
                Text(
                  '${formatYears(years)} වසර',
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF6A1B9A),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 12),

            // =================================================
            // PRATYANTARDASHA
            // =================================================

            if (pratyantardasha.isNotEmpty) ...[
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'ප්‍රත්‍යන්තර දශා',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey.shade800,
                  ),
                ),
              ),
              const SizedBox(height: 8),
              ...pratyantardasha.asMap().entries.map(
                (entry) {
                  final item = entry.value;

                  if (item is! Map) {
                    return const SizedBox.shrink();
                  }

                  return pratyantardashaRow(
                    Map<String, dynamic>.from(
                      item,
                    ),
                    entry.key,
                  );
                },
              ),
            ],
          ],
        ),
      ),
    );
  }

  // =============================================================
  // Pratyantardasha Row
  // =============================================================

  Widget pratyantardashaRow(
    Map<String, dynamic> data,
    int index,
  ) {
    final lord = data['lord']?.toString() ?? '-';

    final start = data['start'];
    final end = data['end'];
    final years = data['years'];

    return Container(
      margin: const EdgeInsets.only(
        bottom: 7,
      ),
      padding: const EdgeInsets.symmetric(
        horizontal: 10,
        vertical: 9,
      ),
      decoration: BoxDecoration(
        color: const Color(0xFFFBF8FD),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Container(
            width: 30,
            height: 30,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Center(
              child: Text(
                planetSymbol(lord),
                style: const TextStyle(
                  fontSize: 15,
                  color: Color(0xFF6A1B9A),
                ),
              ),
            ),
          ),
          const SizedBox(width: 9),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  planetName(lord),
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  '${formatDate(start)} → ${formatDate(end)}',
                  style: TextStyle(
                    fontSize: 10,
                    color: Colors.grey.shade600,
                  ),
                ),
              ],
            ),
          ),
          Text(
            '${formatYears(years)}y',
            style: const TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.bold,
              color: Color(0xFF6A1B9A),
            ),
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
    final birthMahadasha = widget.chartData['birth_mahadasha'];

    final dashaData = widget.chartData['dasha'];

    final List<dynamic> dashas = dashaData is List
        ? List<dynamic>.from(
            dashaData,
          )
        : <dynamic>[];

    // ===========================================================
    // CURRENT DASHA
    // ===========================================================

    final currentDasha = getCurrentDasha(dashas);

    final currentMahadasha = currentDasha?['mahadasha'] is Map
        ? Map<String, dynamic>.from(
            currentDasha!['mahadasha'],
          )
        : null;

    final currentAntardasha = currentDasha?['antardasha'] is Map
        ? Map<String, dynamic>.from(
            currentDasha!['antardasha'],
          )
        : null;

    final currentPratyantardasha = currentDasha?['pratyantardasha'] is Map
        ? Map<String, dynamic>.from(
            currentDasha!['pratyantardasha'],
          )
        : null;

    return Scaffold(
      backgroundColor: const Color(0xFFF8F5FC),

      // =========================================================
      // APP BAR
      // =========================================================

      appBar: AppBar(
        title: const Text(
          'දශා විස්තර',
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
                    '🪐 විංශෝත්තරී දශා',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'මහ දශා • අන්තර් දශා • ප්‍රත්‍යන්තර දශා',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),

            // ===================================================
            // CURRENT DASHA
            // ===================================================

            if (currentMahadasha != null) ...[
              const SizedBox(height: 24),
              const Text(
                'දැනට ක්‍රියාත්මක දශාව',
                style: TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF4A148C),
                ),
              ),
              const SizedBox(height: 12),
              currentDashaCard(
                currentMahadasha,
                currentAntardasha,
                currentPratyantardasha,
              ),

              // ===================================================
              // CURRENT DASHA INTERPRETATION
              // ===================================================

              if (widget.chartData['dasha_interpretation'] is Map) ...[
                const SizedBox(height: 22),
                const Text(
                  'දැනට ක්‍රියාත්මක දශාවේ විශ්ලේෂණය',
                  style: TextStyle(
                    fontSize: 19,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF4A148C),
                  ),
                ),
                const SizedBox(height: 12),
                dashaInterpretationCard(
                  Map<String, dynamic>.from(
                    widget.chartData['dasha_interpretation'],
                  ),
                ),
              ],
            ],

            const SizedBox(height: 28),

            // ===================================================
            // BIRTH MAHADASHA
            // ===================================================

            if (birthMahadasha is Map) ...[
              const Text(
                'උපන් අවස්ථාවේ මහ දශාව',
                style: TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF4A148C),
                ),
              ),
              const SizedBox(height: 12),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(
                    18,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(
                        0.05,
                      ),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    Container(
                      width: 52,
                      height: 52,
                      decoration: BoxDecoration(
                        color: const Color(
                          0xFFF1E4F8,
                        ),
                        borderRadius: BorderRadius.circular(
                          15,
                        ),
                      ),
                      child: Center(
                        child: Text(
                          planetSymbol(
                            birthMahadasha['lord']?.toString() ?? '',
                          ),
                          style: const TextStyle(
                            fontSize: 25,
                            color: Color(
                              0xFF6A1B9A,
                            ),
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
                            planetName(
                              birthMahadasha['lord']?.toString() ?? '-',
                            ),
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Color(
                                0xFF4A148C,
                              ),
                            ),
                          ),
                          const SizedBox(
                            height: 5,
                          ),
                          Text(
                            '${formatDate(birthMahadasha['start'])} → ${formatDate(birthMahadasha['end'])}',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey.shade600,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          'ඉතිරි',
                          style: TextStyle(
                            fontSize: 11,
                            color: Colors.grey.shade600,
                          ),
                        ),
                        const SizedBox(
                          height: 3,
                        ),
                        Text(
                          '${formatYears(birthMahadasha['remaining_years'])}y',
                          style: const TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Color(
                              0xFF6A1B9A,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 28),
            ],

            // ===================================================
            // MAHADASHA LIST
            // ===================================================

            const Text(
              'මහ දශා අනුපිළිවෙල',
              style: TextStyle(
                fontSize: 19,
                fontWeight: FontWeight.bold,
                color: Color(0xFF4A148C),
              ),
            ),

            const SizedBox(height: 12),

            if (dashas.isEmpty)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(
                  20,
                ),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(
                    18,
                  ),
                ),
                child: const Text(
                  'දශා දත්ත ලබාගත නොහැක.',
                  textAlign: TextAlign.center,
                ),
              )
            else
              ...dashas.asMap().entries.map(
                (entry) {
                  final item = entry.value;

                  if (item is! Map) {
                    return const SizedBox.shrink();
                  }

                  return mahadashaCard(
                    Map<String, dynamic>.from(
                      item,
                    ),
                    entry.key,
                  );
                },
              ),
          ],
        ),
      ),
    );
  }
}
