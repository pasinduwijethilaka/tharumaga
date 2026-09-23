import 'package:flutter/material.dart';
import 'birth_details_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F5FC),
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.fromLTRB(
            18,
            18,
            18,
            30,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ==================================================
              // TOP BRAND
              // ==================================================

              Row(
                children: [
                  Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [
                          Color(0xFF6A1B9A),
                          Color(0xFF8E24AA),
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(15),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(
                            0xFF6A1B9A,
                          ).withOpacity(0.20),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: const Icon(
                      Icons.auto_awesome,
                      color: Colors.white,
                      size: 27,
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'තරුමග',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF4A148C),
                          ),
                        ),
                        SizedBox(height: 2),
                        Text(
                          'ඔබේ තරු මඟ කියවමු',
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.black54,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 26),

              // ==================================================
              // HERO CARD
              // ==================================================

              Container(
                width: double.infinity,
                padding: const EdgeInsets.fromLTRB(
                  22,
                  24,
                  22,
                  22,
                ),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [
                      Color(0xFF4A148C),
                      Color(0xFF7B1FA2),
                      Color(0xFF9C27B0),
                    ],
                  ),
                  borderRadius: BorderRadius.circular(26),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(
                        0xFF6A1B9A,
                      ).withOpacity(0.24),
                      blurRadius: 18,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: Stack(
                  children: [
                    // Decorative stars

                    const Positioned(
                      top: 0,
                      right: 4,
                      child: Opacity(
                        opacity: 0.16,
                        child: Icon(
                          Icons.auto_awesome,
                          size: 75,
                          color: Colors.white,
                        ),
                      ),
                    ),

                    const Positioned(
                      right: 48,
                      bottom: 10,
                      child: Opacity(
                        opacity: 0.10,
                        child: Icon(
                          Icons.star,
                          size: 35,
                          color: Colors.white,
                        ),
                      ),
                    ),

                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 11,
                            vertical: 6,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.13),
                            borderRadius: BorderRadius.circular(
                              20,
                            ),
                          ),
                          child: const Text(
                            '✨ ඔබේ තරු ලෝකයට',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),

                        const SizedBox(height: 16),

                        const Text(
                          'ඔබේ ජන්ම පත්‍රය\nසොයාගන්න',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 29,
                            height: 1.12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),

                        const SizedBox(height: 12),

                        const Text(
                          'උපන් දිනය, වේලාව සහ ස්ථානය ඇතුළත් කර ඔබේ ජන්ම පත්‍රය ගණනය කරගන්න.',
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 14,
                            height: 1.5,
                          ),
                        ),

                        const SizedBox(height: 22),

                        // ==================================================
                        // START BUTTON
                        // ==================================================

                        SizedBox(
                          width: double.infinity,
                          height: 54,
                          child: ElevatedButton.icon(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => const BirthDetailsScreen(),
                                ),
                              );
                            },
                            icon: const Icon(
                              Icons.auto_awesome,
                              size: 20,
                            ),
                            label: const Text(
                              'ජන්ම පත්‍රය ආරම්භ කරන්න',
                              style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.white,
                              foregroundColor: const Color(
                                0xFF6A1B9A,
                              ),
                              elevation: 0,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(
                                  17,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              // ==================================================
              // SECTION TITLE
              // ==================================================

              const Text(
                'TharuMaga සමඟ',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF3D2450),
                ),
              ),

              const SizedBox(height: 6),

              Text(
                'ඔබේ ජන්ම පත්‍රය ගණනය කිරීමට භාවිතා කරන ක්‍රම',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey.shade600,
                ),
              ),

              const SizedBox(height: 16),

              // ==================================================
              // FEATURE GRID
              // ==================================================

              const Row(
                children: [
                  Expanded(
                    child: FeatureCard(
                      icon: Icons.public,
                      title: 'Sidereal',
                      subtitle: 'Lahiri Ayanamsa',
                    ),
                  ),
                  SizedBox(width: 12),
                  Expanded(
                    child: FeatureCard(
                      icon: Icons.stars,
                      title: 'Nakshatra',
                      subtitle: '27 Nakshatras',
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              const Row(
                children: [
                  Expanded(
                    child: FeatureCard(
                      icon: Icons.timelapse,
                      title: 'Vimshottari',
                      subtitle: 'Dasha System',
                    ),
                  ),
                  SizedBox(width: 12),
                  Expanded(
                    child: FeatureCard(
                      icon: Icons.grid_view_rounded,
                      title: 'D1 Chart',
                      subtitle: 'Whole Sign',
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 26),

              // ==================================================
              // WHAT YOU GET CARD
              // ==================================================

              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(19),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(21),
                  border: Border.all(
                    color: const Color(
                      0xFF6A1B9A,
                    ).withOpacity(0.08),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.045),
                      blurRadius: 12,
                      offset: const Offset(0, 5),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 42,
                          height: 42,
                          decoration: BoxDecoration(
                            color: const Color(
                              0xFFF1E4F8,
                            ),
                            borderRadius: BorderRadius.circular(
                              13,
                            ),
                          ),
                          child: const Icon(
                            Icons.auto_graph_rounded,
                            color: Color(
                              0xFF6A1B9A,
                            ),
                            size: 23,
                          ),
                        ),
                        const SizedBox(width: 12),
                        const Text(
                          'ඔබට ලැබෙන තොරතුරු',
                          style: TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.bold,
                            color: Color(
                              0xFF4A148C,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 17),
                    const InfoItem(
                      icon: Icons.radio_button_checked,
                      text: 'ලග්නය සහ රාශිය',
                    ),
                    const InfoItem(
                      icon: Icons.radio_button_checked,
                      text: 'ග්‍රහ පිහිටීම් සහ අංශක',
                    ),
                    const InfoItem(
                      icon: Icons.radio_button_checked,
                      text: 'නක්ෂත්‍රය සහ පාදය',
                    ),
                    const InfoItem(
                      icon: Icons.radio_button_checked,
                      text: 'D1 රාශි චක්‍රය',
                    ),
                    const InfoItem(
                      icon: Icons.radio_button_checked,
                      text: 'මහ දශා, අන්තර් දශා සහ ප්‍රත්‍යන්තර දශා',
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 26),

              // ==================================================
              // HOW IT WORKS
              // ==================================================

              const Text(
                'ආරම්භ කරන්නේ මෙහෙමයි',
                style: TextStyle(
                  fontSize: 19,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF3D2450),
                ),
              ),

              const SizedBox(height: 14),

              const Row(
                children: [
                  Expanded(
                    child: StepCard(
                      number: '1',
                      title: 'උපන් තොරතුරු',
                      icon: Icons.calendar_month_rounded,
                    ),
                  ),
                  SizedBox(width: 9),
                  Expanded(
                    child: StepCard(
                      number: '2',
                      title: 'ස්ථානය',
                      icon: Icons.location_on_rounded,
                    ),
                  ),
                  SizedBox(width: 9),
                  Expanded(
                    child: StepCard(
                      number: '3',
                      title: 'ජන්ම පත්‍රය',
                      icon: Icons.auto_awesome,
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 30),

              // ==================================================
              // FINAL CTA
              // ==================================================

              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(
                  horizontal: 18,
                  vertical: 18,
                ),
                decoration: BoxDecoration(
                  color: const Color(0xFFF1E4F8),
                  borderRadius: BorderRadius.circular(18),
                ),
                child: Row(
                  children: [
                    const Icon(
                      Icons.auto_awesome_outlined,
                      color: Color(0xFF6A1B9A),
                      size: 25,
                    ),
                    const SizedBox(width: 12),
                    const Expanded(
                      child: Text(
                        'ඔබේ තරු මඟ සොයා බලමු.',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: Color(
                            0xFF4A148C,
                          ),
                        ),
                      ),
                    ),
                    Icon(
                      Icons.arrow_forward_ios_rounded,
                      size: 15,
                      color: Colors.grey.shade600,
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              // ==================================================
              // FOOTER
              // ==================================================

              Center(
                child: Column(
                  children: [
                    Text(
                      'TharuMaga',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                        color: Colors.grey.shade700,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      'ඔබේ තරු මඟ කියවමු',
                      style: TextStyle(
                        fontSize: 11,
                        color: Colors.grey.shade500,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// ============================================================
// FEATURE CARD
// ============================================================

class FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;

  const FeatureCard({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 142,
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(19),
        border: Border.all(
          color: Colors.black.withOpacity(0.05),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.045),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: const Color(0xFFF1E4F8),
              borderRadius: BorderRadius.circular(15),
            ),
            child: Icon(
              icon,
              size: 27,
              color: const Color(0xFF6A1B9A),
            ),
          ),
          const SizedBox(height: 10),
          Text(
            title,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Color(0xFF333333),
            ),
          ),
          const SizedBox(height: 4),
          Text(
            subtitle,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 10.5,
              color: Colors.black54,
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================
// INFO ITEM
// ============================================================

class InfoItem extends StatelessWidget {
  final IconData icon;
  final String text;

  const InfoItem({
    super.key,
    required this.icon,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 11),
      child: Row(
        children: [
          Icon(
            icon,
            size: 15,
            color: const Color(0xFF8E24AA),
          ),
          const SizedBox(width: 9),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 13,
                color: Colors.black87,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================
// STEP CARD
// ============================================================

class StepCard extends StatelessWidget {
  final String number;
  final String title;
  final IconData icon;

  const StepCard({
    super.key,
    required this.number,
    required this.title,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 118,
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(17),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Stack(
            alignment: Alignment.bottomRight,
            children: [
              Container(
                width: 42,
                height: 42,
                decoration: BoxDecoration(
                  color: const Color(0xFFF1E4F8),
                  borderRadius: BorderRadius.circular(
                    13,
                  ),
                ),
                child: Icon(
                  icon,
                  size: 22,
                  color: const Color(
                    0xFF6A1B9A,
                  ),
                ),
              ),
              Container(
                width: 17,
                height: 17,
                decoration: const BoxDecoration(
                  color: Color(0xFF6A1B9A),
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: Text(
                    number,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 9,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 9),
          Text(
            title,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w600,
              color: Color(0xFF333333),
            ),
          ),
        ],
      ),
    );
  }
}
