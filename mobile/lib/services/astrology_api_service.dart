import 'dart:convert';
import 'package:http/http.dart' as http;

class AstrologyApiService {
  // Flutter Web / Chrome එකෙන් local FastAPI server එක access කරන URL එක
  static const String baseUrl = 'http://10.0.2.2:8000';

  static Future<Map<String, dynamic>> calculateChart({
    required DateTime birthDate,
    required int hour,
    required int minute,
    required double latitude,
    required double longitude,
    required String timezone,
    required String place,
  }) async {
    final Uri url = Uri.parse('$baseUrl/api/v1/chart');

    final Map<String, dynamic> requestBody = {
      'day': birthDate.day,
      'month': birthDate.month,
      'year': birthDate.year,
      'hour': hour,
      'minute': minute,
      'second': 0,
      'latitude': latitude,
      'longitude': longitude,
      'timezone': timezone,
      'place': place,
    };

    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode(requestBody),
    );

    final Map<String, dynamic> responseData =
        jsonDecode(utf8.decode(response.bodyBytes));

    if (response.statusCode == 200) {
      return responseData;
    }

    throw Exception(
      responseData['detail'] ?? 'Chart calculation failed',
    );
  }
}
