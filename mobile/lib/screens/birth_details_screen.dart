import 'package:flutter/material.dart';
import 'package:mobile/screens/birth_place_screen.dart';

class BirthDetailsScreen extends StatefulWidget {
  const BirthDetailsScreen({super.key});

  @override
  State<BirthDetailsScreen> createState() => _BirthDetailsScreenState();
}

class _BirthDetailsScreenState extends State<BirthDetailsScreen> {
  final TextEditingController nameController = TextEditingController();

  DateTime? selectedDate;
  TimeOfDay? selectedTime;

  // ==========================================================
  // SELECT DATE
  // ==========================================================

  Future<void> selectDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime(2000),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );

    if (picked != null) {
      setState(() {
        selectedDate = picked;
      });
    }
  }

  // ==========================================================
  // SELECT TIME
  // ==========================================================

  Future<void> selectTime() async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: const TimeOfDay(
        hour: 12,
        minute: 0,
      ),
    );

    if (picked != null) {
      setState(() {
        selectedTime = picked;
      });
    }
  }

  // ==========================================================
  // CONTINUE
  // ==========================================================

  void continueToBirthPlace() {
    if (selectedDate == null) {
      showMessage(
        'කරුණාකර උපන් දිනය තෝරන්න.',
      );
      return;
    }

    if (selectedTime == null) {
      showMessage(
        'කරුණාකර උපන් වේලාව තෝරන්න.',
      );
      return;
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => BirthPlaceScreen(
          name: nameController.text.trim(),
          birthDate: selectedDate!,
          birthTime: selectedTime!,
        ),
      ),
    );
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
    nameController.dispose();
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
          'ජන්ම තොරතුරු',
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
            // --------------------------------------------------
            // TITLE
            // --------------------------------------------------

            const Text(
              'ඔබේ තොරතුරු ඇතුළත් කරන්න',
              style: TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
                color: Color(0xFF4A148C),
              ),
            ),

            const SizedBox(height: 8),

            const Text(
              'නිවැරදි ජන්ම පත්‍රයක් සඳහා උපන් දිනය සහ වේලාව නිවැරදිව ලබා දෙන්න.',
              style: TextStyle(
                fontSize: 14,
                color: Colors.black54,
                height: 1.5,
              ),
            ),

            const SizedBox(height: 30),

            // --------------------------------------------------
            // NAME
            // --------------------------------------------------

            const Text(
              'නම',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 8),

            TextField(
              controller: nameController,
              textInputAction: TextInputAction.next,
              decoration: InputDecoration(
                hintText: 'ඔබේ නම ඇතුළත් කරන්න',
                prefixIcon: const Icon(
                  Icons.person_outline,
                ),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(16),
                  borderSide: BorderSide.none,
                ),
              ),
            ),

            const SizedBox(height: 22),

            // --------------------------------------------------
            // BIRTH DATE
            // --------------------------------------------------

            const Text(
              'උපන් දිනය',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 8),

            InkWell(
              onTap: selectDate,
              borderRadius: BorderRadius.circular(16),
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 18,
                ),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  children: [
                    const Icon(
                      Icons.calendar_month,
                      color: Color(0xFF6A1B9A),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        selectedDate == null
                            ? 'උපන් දිනය තෝරන්න'
                            : '${selectedDate!.day.toString().padLeft(2, '0')}/'
                                '${selectedDate!.month.toString().padLeft(2, '0')}/'
                                '${selectedDate!.year}',
                        style: TextStyle(
                          fontSize: 15,
                          color: selectedDate == null
                              ? Colors.black45
                              : Colors.black87,
                        ),
                      ),
                    ),
                    const Icon(
                      Icons.chevron_right,
                      color: Colors.black38,
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 22),

            // --------------------------------------------------
            // BIRTH TIME
            // --------------------------------------------------

            const Text(
              'උපන් වේලාව',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 8),

            InkWell(
              onTap: selectTime,
              borderRadius: BorderRadius.circular(16),
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 18,
                ),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  children: [
                    const Icon(
                      Icons.access_time,
                      color: Color(0xFF6A1B9A),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        selectedTime == null
                            ? 'උපන් වේලාව තෝරන්න'
                            : selectedTime!.format(context),
                        style: TextStyle(
                          fontSize: 15,
                          color: selectedTime == null
                              ? Colors.black45
                              : Colors.black87,
                        ),
                      ),
                    ),
                    const Icon(
                      Icons.chevron_right,
                      color: Colors.black38,
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 35),

            // --------------------------------------------------
            // CONTINUE BUTTON
            // --------------------------------------------------

            SizedBox(
              width: double.infinity,
              height: 58,
              child: ElevatedButton(
                onPressed: continueToBirthPlace,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6A1B9A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
                child: const Text(
                  'ඉදිරියට යන්න',
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                  ),
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
