# TharuMaga 🌟

**ඔබේ තරු මඟ කියවමු**

TharuMaga is a Vedic astrology application built with a Python/FastAPI backend and Flutter mobile application.

## ✨ Features

- Sidereal zodiac
- Lahiri Ayanamsa
- True Node Rahu
- Ketu calculated 180° opposite Rahu
- Swiss Ephemeris calculations
- Local birth time to UTC conversion
- Vedic Lagna calculation
- D1 / Rasi chart
- Whole Sign Houses
- 27 Nakshatras
- Nakshatra Pada calculation
- Vimshottari Dasha
- Antardasha / Bhukti
- Pratyantardasha
- Planetary positions
- Sinhala astrology interpretations
- Yoga detection
- Yoga interpretations

## 🏗️ Project Structure

```text
tharumaga/
├── backend/
│   └── app/
│       ├── astrology_engine.py
│       ├── interpretation_engine.py
│       ├── dasha_interpretation_engine.py
│       ├── yoga_detection_engine.py
│       ├── yoga_interpretation_engine.py
│       └── main.py
│
├── mobile/
│   ├── lib/
│   │   ├── models/
│   │   ├── screens/
│   │   └── services/
│   └── pubspec.yaml
│
└── README.md
⚙️ Backend

The backend is built with:

Python
FastAPI
Swiss Ephemeris
Pydantic
Uvicorn

Run Backend
From the project root:.
\backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

Health Check
http://127.0.0.1:8000/health

📱 Mobile App
The mobile application is built with Flutter.

From the mobile directory:
cd mobile
flutter pub get
flutter run
🔭 Astrology Engine

TharuMaga uses Swiss Ephemeris as the astronomical calculation foundation.

The current calculation specification includes:

Sidereal zodiac
Lahiri Ayanamsa
True Node Rahu
Ketu opposite Rahu
Whole Sign Houses
27 Nakshatras
4 Nakshatra Padas
Vimshottari Dasha

🧪 Testing
The backend contains multiple calculation, regression, interpretation, Dasha and Yoga tests.

Examples include:
accuracy_test.py
test_engine.py
test_engine_regression.py
test_dasha_interpretation_audit.py
test_overall_chart_interpretation_audit.py
test_yoga_detection.py
test_yoga_interpretation.py
test_final_full_regression.py
📌 Project Status

TharuMaga is currently under active development.

The core astrology calculation engine, interpretation system, Dasha system and Yoga system have been integrated with the Flutter application.

⚠️ Note

Astrology interpretations are provided as traditional astrological interpretations and should not be treated as scientific predictions or professional advice.

👨‍💻 Development

TharuMaga is developed as a personal software project combining:

Astrology calculation
Python backend development
Flutter mobile development
Sinhala user experience