import 'package:flutter/material.dart';

class D1ChartScreen extends StatelessWidget {
  final Map<String, dynamic> chartData;

  const D1ChartScreen({
    super.key,
    required this.chartData,
  });

  // =============================================================
  // Sinhala Zodiac Names
  // =============================================================

  String signName(int index) {
    const signs = [
      'මේෂ',
      'වෘෂභ',
      'මිථුන',
      'කටක',
      'සිංහ',
      'කන්‍යා',
      'තුලා',
      'වෘශ්චික',
      'ධනු',
      'මකර',
      'කුම්භ',
      'මීන',
    ];

    return signs[index % 12];
  }

  // =============================================================
  // Sinhala Planet Names
  // =============================================================

  String planetName(String key) {
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

    return planets[key] ?? key;
  }

  // =============================================================
  // Build planets directly by HOUSE
  //
  // Backend already provides:
  // planet -> house
  //
  // So we use house directly instead of calculating
  // house from sign_index.
  // =============================================================

  Map<int, List<String>> buildPlanetsByHouse() {
    final Map<int, List<String>> result = {};

    for (int i = 1; i <= 12; i++) {
      result[i] = [];
    }

    // -------------------------------------------------------------
    // Main 7 planets
    // -------------------------------------------------------------

    final planets = chartData['planets'];

    if (planets is Map) {
      planets.forEach((key, value) {
        if (value is Map) {
          final houseValue = value['house'];

          if (houseValue is num) {
            final house = houseValue.toInt();

            if (house >= 1 && house <= 12) {
              result[house]!.add(
                planetName(key.toString()),
              );
            }
          }
        }
      });
    }

    // -------------------------------------------------------------
    // Rahu
    // -------------------------------------------------------------

    final rahu = chartData['rahu'];

    if (rahu is Map) {
      final houseValue = rahu['house'];

      if (houseValue is num) {
        final house = houseValue.toInt();

        if (house >= 1 && house <= 12) {
          result[house]!.add(
            planetName('Rahu'),
          );
        }
      }
    }

    // -------------------------------------------------------------
    // Ketu
    // -------------------------------------------------------------

    final ketu = chartData['ketu'];

    if (ketu is Map) {
      final houseValue = ketu['house'];

      if (houseValue is num) {
        final house = houseValue.toInt();

        if (house >= 1 && house <= 12) {
          result[house]!.add(
            planetName('Ketu'),
          );
        }
      }
    }

    return result;
  }

  // =============================================================
  // Find SIGN for HOUSE
  // =============================================================

  int signForHouse(
    int houseNumber,
    int lagnaSignIndex,
  ) {
    return (lagnaSignIndex + houseNumber - 1) % 12;
  }

  // =============================================================
  // House Content
  // =============================================================

  Widget houseContentWidget({
    required int houseNumber,
    required int lagnaSignIndex,
    required Map<int, List<String>> planetsByHouse,
  }) {
    final signIndex = signForHouse(
      houseNumber,
      lagnaSignIndex,
    );

    final planets = planetsByHouse[houseNumber] ?? [];

    final isLagna = houseNumber == 1;

    return Padding(
      padding: const EdgeInsets.all(2),
      child: FittedBox(
        fit: BoxFit.scaleDown,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // House number
            Text(
              '$houseNumber',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: isLagna ? const Color(0xFF4A148C) : Colors.black87,
              ),
            ),

            const SizedBox(height: 1),

            // Zodiac sign
            Text(
              signName(signIndex),
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w600,
                color: Color(0xFF6A1B9A),
              ),
            ),

            // Planets
            if (planets.isNotEmpty) ...[
              const SizedBox(height: 2),
              Wrap(
                alignment: WrapAlignment.center,
                spacing: 3,
                runSpacing: 1,
                children: planets.map(
                  (planet) {
                    return Text(
                      planet,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF6A1B9A),
                      ),
                    );
                  },
                ).toList(),
              ),
            ] else ...[
              const SizedBox(height: 3),
              const Text(
                '—',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                  color: Colors.black26,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  // =============================================================
  // Build
  // =============================================================

  @override
  Widget build(BuildContext context) {
    final lagna = chartData['lagna'] ?? {};

    final lagnaSignIndex =
        lagna['sign_index'] is num ? (lagna['sign_index'] as num).toInt() : 0;

    // IMPORTANT:
    // Use backend house values directly.
    final planetsByHouse = buildPlanetsByHouse();

    return Scaffold(
      backgroundColor: const Color(0xFFF8F5FC),

      // =========================================================
      // APP BAR
      // =========================================================

      appBar: AppBar(
        title: const Text(
          'D1 රාශි චක්‍රය',
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
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ===================================================
            // HEADER
            // ===================================================

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [
                    Color(0xFF6A1B9A),
                    Color(0xFF8E24AA),
                  ],
                ),
                borderRadius: BorderRadius.circular(22),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '🔮 D1 රාශි චක්‍රය',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 23,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 7),
                  Text(
                    'ඔබගේ ජන්ම පත්‍රයේ රාශි හා ග්‍රහ පිහිටීම්',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 22),

            // ===================================================
            // CHART TITLE
            // ===================================================

            const Text(
              'රාශි චක්‍රය',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Color(0xFF4A148C),
              ),
            ),

            const SizedBox(height: 12),

            // ===================================================
            // SRI LANKAN TRADITIONAL KENDRA CHART
            // ===================================================

            Center(
              child: AspectRatio(
                aspectRatio: 1,
                child: Container(
                  decoration: BoxDecoration(
                    color: Colors.white,
                    border: Border.all(
                      color: const Color(0xFF6A1B9A),
                      width: 2,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.08),
                        blurRadius: 12,
                        offset: const Offset(0, 5),
                      ),
                    ],
                  ),
                  child: CustomPaint(
                    painter: KendraChartPainter(),
                    child: LayoutBuilder(
                      builder: (context, constraints) {
                        final w = constraints.maxWidth;
                        final h = constraints.maxHeight;

                        final cellW = w / 3;
                        final cellH = h / 3;

                        return Stack(
                          children: [
                            // =========================================
                            // HOUSE 1
                            // =========================================

                            Positioned(
                              left: cellW,
                              top: 0,
                              width: cellW,
                              height: cellH,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 1,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 2
                            // =========================================

                            Positioned(
                              left: 0,
                              top: 0,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 2,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 3
                            // =========================================

                            Positioned(
                              left: 0,
                              top: cellH / 2,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 3,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 12
                            // =========================================

                            Positioned(
                              left: cellW * 2,
                              top: 0,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 12,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 11
                            // =========================================

                            Positioned(
                              left: cellW * 2,
                              top: cellH / 2,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 11,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 4
                            // =========================================

                            Positioned(
                              left: 0,
                              top: cellH,
                              width: cellW,
                              height: cellH,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 4,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 10
                            // =========================================

                            Positioned(
                              left: cellW * 2,
                              top: cellH,
                              width: cellW,
                              height: cellH,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 10,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 5
                            // =========================================

                            Positioned(
                              left: 0,
                              top: cellH * 2,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 5,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 6
                            // =========================================

                            Positioned(
                              left: 0,
                              top: cellH * 2 + cellH / 2,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 6,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 7
                            // =========================================

                            Positioned(
                              left: cellW,
                              top: cellH * 2,
                              width: cellW,
                              height: cellH,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 7,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 8
                            // =========================================

                            Positioned(
                              left: cellW * 2,
                              top: cellH * 2,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 8,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // HOUSE 9
                            // =========================================

                            Positioned(
                              left: cellW * 2,
                              top: cellH * 2 + cellH / 2,
                              width: cellW,
                              height: cellH / 2,
                              child: Center(
                                child: houseContentWidget(
                                  houseNumber: 9,
                                  lagnaSignIndex: lagnaSignIndex,
                                  planetsByHouse: planetsByHouse,
                                ),
                              ),
                            ),

                            // =========================================
                            // CENTER / LAGNA
                            // =========================================

                            Positioned(
                              left: cellW,
                              top: cellH,
                              width: cellW,
                              height: cellH,
                              child: Center(
                                child: FittedBox(
                                  fit: BoxFit.scaleDown,
                                  child: Text(
                                    'ලග්න\n${signName(lagnaSignIndex)}',
                                    textAlign: TextAlign.center,
                                    style: const TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                      color: Color(0xFF4A148C),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        );
                      },
                    ),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 22),

            // ===================================================
            // LAGNA SUMMARY
            // ===================================================

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFFEDE0F5),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.auto_awesome,
                    color: Color(0xFF6A1B9A),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'ලග්නය: ${signName(lagnaSignIndex)}',
                      style: const TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF4A148C),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // ===================================================
            // PLANET NAMES
            // ===================================================

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'ග්‍රහ නාම',
                    style: TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF4A148C),
                    ),
                  ),
                  SizedBox(height: 12),
                  Text(
                    'රවි   සඳු   කුජ   බුධ   ගුරු   සිකුරු   ශනි',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF6A1B9A),
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'රාහු   කේතු',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF6A1B9A),
                    ),
                  ),
                ],
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
// KENDRA CHART PAINTER
// =================================================================

class KendraChartPainter extends CustomPainter {
  @override
  void paint(
    Canvas canvas,
    Size size,
  ) {
    final paint = Paint()
      ..color = const Color(0xFF6A1B9A)
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    final w = size.width;
    final h = size.height;

    final cellW = w / 3;
    final cellH = h / 3;

    // =============================================================
    // OUTER BORDER
    // =============================================================

    canvas.drawRect(
      Rect.fromLTWH(
        0,
        0,
        w,
        h,
      ),
      paint,
    );

    // =============================================================
    // VERTICAL LINES
    // =============================================================

    canvas.drawLine(
      Offset(cellW, 0),
      Offset(cellW, h),
      paint,
    );

    canvas.drawLine(
      Offset(cellW * 2, 0),
      Offset(cellW * 2, h),
      paint,
    );

    // =============================================================
    // HORIZONTAL LINES
    // =============================================================

    canvas.drawLine(
      Offset(0, cellH),
      Offset(w, cellH),
      paint,
    );

    canvas.drawLine(
      Offset(0, cellH * 2),
      Offset(w, cellH * 2),
      paint,
    );

    // =============================================================
    // TOP LEFT DIAGONAL
    // =============================================================

    canvas.drawLine(
      const Offset(0, 0),
      Offset(cellW, cellH),
      paint,
    );

    // =============================================================
    // TOP RIGHT DIAGONAL
    // =============================================================

    canvas.drawLine(
      Offset(w, 0),
      Offset(cellW * 2, cellH),
      paint,
    );

    // =============================================================
    // BOTTOM LEFT DIAGONAL
    // =============================================================

    canvas.drawLine(
      Offset(0, h),
      Offset(cellW, cellH * 2),
      paint,
    );

    // =============================================================
    // BOTTOM RIGHT DIAGONAL
    // =============================================================

    canvas.drawLine(
      Offset(w, h),
      Offset(cellW * 2, cellH * 2),
      paint,
    );

    // =============================================================
    // CENTER BORDER
    // =============================================================

    canvas.drawRect(
      Rect.fromLTWH(
        cellW,
        cellH,
        cellW,
        cellH,
      ),
      paint,
    );
  }

  @override
  bool shouldRepaint(
    covariant CustomPainter oldDelegate,
  ) {
    return false;
  }
}
