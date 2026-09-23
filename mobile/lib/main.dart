import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const TharuMagaApp());
}

class TharuMagaApp extends StatelessWidget {
  const TharuMagaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'TharuMaga',
      theme: ThemeData(
        useMaterial3: true,
        fontFamily: 'Roboto',
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6A1B9A),
          brightness: Brightness.light,
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
