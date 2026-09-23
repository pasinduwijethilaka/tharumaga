import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mobile/services/astrology_api_service.dart';
import 'chart_result_screen.dart';

class BirthPlaceScreen extends StatefulWidget {
  final String name;
  final DateTime birthDate;
  final TimeOfDay birthTime;

  const BirthPlaceScreen({
    super.key,
    required this.name,
    required this.birthDate,
    required this.birthTime,
  });

  @override
  State<BirthPlaceScreen> createState() => _BirthPlaceScreenState();
}

class _BirthPlaceScreenState extends State<BirthPlaceScreen> {
  // ==========================================================
  // COUNTRIES
  // ==========================================================

  final List<Country> countries = const [
    Country(
      name: 'Sri Lanka',
      code: 'LK',
      flag: '🇱🇰',
    ),
    Country(
      name: 'India',
      code: 'IN',
      flag: '🇮🇳',
    ),
    Country(
      name: 'Australia',
      code: 'AU',
      flag: '🇦🇺',
    ),
    Country(
      name: 'United Kingdom',
      code: 'GB',
      flag: '🇬🇧',
    ),
    Country(
      name: 'United States',
      code: 'US',
      flag: '🇺🇸',
    ),
    Country(
      name: 'Canada',
      code: 'CA',
      flag: '🇨🇦',
    ),
    Country(
      name: 'New Zealand',
      code: 'NZ',
      flag: '🇳🇿',
    ),
    Country(
      name: 'Singapore',
      code: 'SG',
      flag: '🇸🇬',
    ),
    Country(
      name: 'United Arab Emirates',
      code: 'AE',
      flag: '🇦🇪',
    ),
    Country(
      name: 'Japan',
      code: 'JP',
      flag: '🇯🇵',
    ),
  ];

  Country? selectedCountry;

  // ==========================================================
  // CONTROLLERS
  // ==========================================================

  final TextEditingController placeController = TextEditingController();

  // ==========================================================
  // SEARCH STATE
  // ==========================================================

  Timer? _debounce;

  List<PlaceResult> suggestions = [];

  bool isSearching = false;

  PlaceResult? selectedPlace;

  // ==========================================================
  // COUNTRY CHANGE
  // ==========================================================

  void onCountryChanged(Country? country) {
    setState(() {
      selectedCountry = country;

      placeController.clear();

      suggestions = [];

      selectedPlace = null;

      isSearching = false;
    });
  }

  // ==========================================================
  // PLACE TEXT CHANGE
  // ==========================================================

  void onPlaceChanged(String value) {
    selectedPlace = null;

    _debounce?.cancel();

    if (selectedCountry == null) {
      return;
    }

    if (value.trim().length < 3) {
      setState(() {
        suggestions = [];
        isSearching = false;
      });

      return;
    }

    setState(() {
      isSearching = true;
    });

    _debounce = Timer(
      const Duration(milliseconds: 700),
      () {
        searchPlaces(value.trim());
      },
    );
  }

  // ==========================================================
  // SEARCH PLACES
  // ==========================================================

  Future<void> searchPlaces(String query) async {
    if (selectedCountry == null) {
      return;
    }

    try {
      final uri = Uri.https(
        'photon.komoot.io',
        '/api/',
        {
          'q': '$query, ${selectedCountry!.name}',
          'limit': '8',
        },
      );

      final response = await http.get(
        uri,
        headers: {
          'User-Agent': 'TharuMaga/1.0',
        },
      );

      if (response.statusCode != 200) {
        throw Exception(
          'Location search failed',
        );
      }

      final Map<String, dynamic> json = jsonDecode(
        utf8.decode(
          response.bodyBytes,
        ),
      );

      final List features = json['features'] ?? [];

      final results = features
          .map(
            (item) => PlaceResult.fromJson(
              item as Map<String, dynamic>,
            ),
          )
          .where(
            (place) =>
                place.latitude != null &&
                place.longitude != null &&
                place.countryCode == selectedCountry!.code,
          )
          .toList();

      if (!mounted) {
        return;
      }

      setState(() {
        suggestions = results;
        isSearching = false;
      });
    } catch (error) {
      if (!mounted) {
        return;
      }

      setState(() {
        suggestions = [];
        isSearching = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'ස්ථානය සෙවීමේදී ගැටලුවක් ඇතිවුණා.',
          ),
        ),
      );
    }
  }

  // ==========================================================
  // SELECT PLACE
  // ==========================================================

  void selectPlace(PlaceResult place) {
    setState(() {
      selectedPlace = place;

      suggestions = [];

      placeController.text = place.name;
    });
  }

  // ==========================================================
  // CALCULATE CHART
  // ==========================================================
  Future<void> calculateChart() async {
    if (selectedCountry == null) {
      showMessage('කරුණාකර රට තෝරන්න.');
      return;
    }

    if (selectedPlace == null) {
      showMessage(
        'කරුණාකර search results වලින් උපන් ස්ථානය තෝරන්න.',
      );
      return;
    }

    if (selectedPlace!.latitude == null || selectedPlace!.longitude == null) {
      showMessage('ස්ථානයේ coordinates ලබාගත නොහැක.');
      return;
    }

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) {
        return const AlertDialog(
          content: Row(
            children: [
              CircularProgressIndicator(),
              SizedBox(width: 20),
              Expanded(
                child: Text(
                  'ජන්ම පත්‍රය ගණනය කරමින්...',
                ),
              ),
            ],
          ),
        );
      },
    );

    try {
      final result = await AstrologyApiService.calculateChart(
        birthDate: widget.birthDate,
        hour: widget.birthTime.hour,
        minute: widget.birthTime.minute,
        latitude: selectedPlace!.latitude!,
        longitude: selectedPlace!.longitude!,
        timezone: selectedCountry!.code == 'LK' ? 'Asia/Colombo' : 'UTC',
        place: selectedPlace!.displayName,
      );

      if (!mounted) return;

      // Close loading dialog
      Navigator.pop(context);

      // Open Chart Result Screen
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ChartResultScreen(
            chartData: result['data'] ?? {},
          ),
        ),
      );
    } catch (error) {
      if (!mounted) return;

      // Close loading dialog
      Navigator.pop(context);

      showMessage(
        'ජන්ම පත්‍රය ගණනය කිරීමේදී දෝෂයක් ඇතිවුණා.\n$error',
      );
    }
  }
  // ==========================================================
  // MESSAGE
  // ==========================================================

  void showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
      ),
    );
  }

  // ==========================================================
  // DISPOSE
  // ==========================================================

  @override
  void dispose() {
    _debounce?.cancel();

    placeController.dispose();

    super.dispose();
  }

  // ==========================================================
  // UI
  // ==========================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F5FC),

      // ======================================================
      // APP BAR
      // ======================================================

      appBar: AppBar(
        title: const Text(
          'උපන් ස්ථානය',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),

      // ======================================================
      // BODY
      // ======================================================

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'ඔබ උපන් ස්ථානය',
              style: TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Color(0xFF4A148C),
              ),
            ),

            const SizedBox(height: 8),

            const Text(
              'මුලින් රට තෝරන්න. ඉන්පසු එම රටට අදාළ නගරයක් හෝ ප්‍රදේශයක් search කරන්න.',
              style: TextStyle(
                fontSize: 14,
                color: Colors.black54,
                height: 1.5,
              ),
            ),

            const SizedBox(height: 30),

            // =================================================
            // COUNTRY
            // =================================================

            const Text(
              'රට',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 8),

            DropdownButtonFormField<Country>(
              value: selectedCountry,
              isExpanded: true,
              decoration: InputDecoration(
                filled: true,
                fillColor: Colors.white,
                prefixIcon: const Icon(
                  Icons.public,
                  color: Color(0xFF6A1B9A),
                ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(16),
                  borderSide: BorderSide.none,
                ),
              ),
              hint: const Text(
                'රට තෝරන්න',
              ),
              items: countries.map(
                (country) {
                  return DropdownMenuItem<Country>(
                    value: country,
                    child: Row(
                      children: [
                        Text(
                          country.flag,
                          style: const TextStyle(
                            fontSize: 22,
                          ),
                        ),
                        const SizedBox(
                          width: 12,
                        ),
                        Text(
                          country.name,
                          style: const TextStyle(
                            fontSize: 15,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ).toList(),
              onChanged: onCountryChanged,
            ),

            const SizedBox(height: 25),

            // =================================================
            // PLACE
            // =================================================

            const Text(
              'නගරය / ප්‍රදේශය',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 8),

            TextField(
              controller: placeController,
              enabled: selectedCountry != null,
              onChanged: onPlaceChanged,
              decoration: InputDecoration(
                hintText: selectedCountry == null
                    ? 'මුලින් රට තෝරන්න'
                    : 'උදා: Colombo',
                prefixIcon: const Icon(
                  Icons.location_on,
                  color: Color(0xFF6A1B9A),
                ),
                suffixIcon: isSearching
                    ? const Padding(
                        padding: EdgeInsets.all(
                          14,
                        ),
                        child: SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                          ),
                        ),
                      )
                    : null,
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(16),
                  borderSide: BorderSide.none,
                ),
              ),
            ),

            const SizedBox(height: 8),

            // =================================================
            // SUGGESTIONS
            // =================================================

            if (suggestions.isNotEmpty)
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(
                    16,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.08),
                      blurRadius: 12,
                      offset: const Offset(0, 5),
                    ),
                  ],
                ),
                child: Column(
                  children: suggestions.map(
                    (place) {
                      return ListTile(
                        leading: const CircleAvatar(
                          backgroundColor: Color(
                            0xFFEDE0F5,
                          ),
                          child: Icon(
                            Icons.location_on,
                            color: Color(
                              0xFF6A1B9A,
                            ),
                          ),
                        ),
                        title: Text(
                          place.name,
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        subtitle: Text(
                          place.subtitle,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        onTap: () {
                          selectPlace(
                            place,
                          );
                        },
                      );
                    },
                  ).toList(),
                ),
              ),

            const SizedBox(height: 25),

            // =================================================
            // SELECTED PLACE
            // =================================================

            if (selectedPlace != null)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(
                  18,
                ),
                decoration: BoxDecoration(
                  color: const Color(
                    0xFFEDE0F5,
                  ),
                  borderRadius: BorderRadius.circular(
                    18,
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(
                          Icons.check_circle,
                          color: Color(
                            0xFF6A1B9A,
                          ),
                        ),
                        SizedBox(
                          width: 8,
                        ),
                        Text(
                          'තෝරාගත් ස්ථානය',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(
                      height: 12,
                    ),
                    Text(
                      selectedPlace!.displayName,
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    Text(
                      'Latitude: '
                      '${selectedPlace!.latitude}\n'
                      'Longitude: '
                      '${selectedPlace!.longitude}',
                      style: const TextStyle(
                        fontSize: 13,
                        color: Colors.black54,
                      ),
                    ),
                  ],
                ),
              ),

            const SizedBox(height: 30),

            // =================================================
            // CALCULATE BUTTON
            // =================================================

            SizedBox(
              width: double.infinity,
              height: 58,
              child: ElevatedButton.icon(
                onPressed: calculateChart,
                icon: const Icon(
                  Icons.auto_awesome,
                ),
                label: const Text(
                  'ජන්ම පත්‍රය ගණනය කරන්න',
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(
                    0xFF6A1B9A,
                  ),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(
                      18,
                    ),
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            const Center(
              child: Text(
                '© OpenStreetMap contributors',
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.black45,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// COUNTRY MODEL
// ============================================================

class Country {
  final String name;
  final String code;
  final String flag;

  const Country({
    required this.name,
    required this.code,
    required this.flag,
  });
}

// ============================================================
// PLACE RESULT MODEL
// ============================================================

class PlaceResult {
  final String name;
  final String subtitle;
  final String countryCode;
  final double? latitude;
  final double? longitude;

  PlaceResult({
    required this.name,
    required this.subtitle,
    required this.countryCode,
    required this.latitude,
    required this.longitude,
  });

  String get displayName {
    if (subtitle.isEmpty) {
      return name;
    }

    return '$name, $subtitle';
  }

  factory PlaceResult.fromJson(
    Map<String, dynamic> json,
  ) {
    final properties = (json['properties'] ?? {}) as Map<String, dynamic>;

    final geometry = (json['geometry'] ?? {}) as Map<String, dynamic>;

    final coordinates = (geometry['coordinates'] ?? []) as List;

    double? longitude;
    double? latitude;

    if (coordinates.length >= 2) {
      longitude = (coordinates[0] as num).toDouble();

      latitude = (coordinates[1] as num).toDouble();
    }

    final name = (properties['name'] ?? 'Unknown place').toString();

    final city = properties['city']?.toString();

    final state = properties['state']?.toString();

    final country = properties['country']?.toString();

    final countryCode =
        (properties['countrycode'] ?? '').toString().toUpperCase();

    final parts = <String>[];

    if (city != null && city.isNotEmpty && city != name) {
      parts.add(city);
    }

    if (state != null && state.isNotEmpty && !parts.contains(state)) {
      parts.add(state);
    }

    if (country != null && country.isNotEmpty && !parts.contains(country)) {
      parts.add(country);
    }

    return PlaceResult(
      name: name,
      subtitle: parts.join(', '),
      countryCode: countryCode,
      latitude: latitude,
      longitude: longitude,
    );
  }
}
