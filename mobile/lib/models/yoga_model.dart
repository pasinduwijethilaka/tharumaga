class YogaModel {
  final String id;
  final String title;
  final String category;
  final String summary;
  final List<String> planets;
  final List<int> houses;
  final String rule;
  final List<String> relationships;
  final String relationshipSummary;
  final List<String> themes;
  final List<String> lifeAreas;
  final String caution;

  const YogaModel({
    required this.id,
    required this.title,
    required this.category,
    required this.summary,
    required this.planets,
    required this.houses,
    required this.rule,
    required this.relationships,
    required this.relationshipSummary,
    required this.themes,
    required this.lifeAreas,
    required this.caution,
  });

  factory YogaModel.fromJson(Map<String, dynamic> json) {
    return YogaModel(
      id: json['id']?.toString() ?? '',
      title: json['title']?.toString() ?? json['name']?.toString() ?? 'Yoga',
      category: json['category']?.toString() ?? 'Yoga',
      summary: json['summary']?.toString() ?? '',
      planets: (json['planets'] as List? ?? [])
          .map((item) => item.toString())
          .toList(),
      houses: (json['houses'] as List? ?? [])
          .map((item) => int.tryParse(item.toString()) ?? 0)
          .where((item) => item > 0)
          .toList(),
      rule: json['rule']?.toString() ?? '',
      relationships: (json['relationships'] as List? ?? [])
          .map((item) => item.toString())
          .toList(),
      relationshipSummary: json['relationship_summary']?.toString() ?? '',
      themes: (json['themes'] as List? ?? [])
          .map((item) => item.toString())
          .toList(),
      lifeAreas: (json['life_areas'] as List? ?? [])
          .map((item) => item.toString())
          .toList(),
      caution: json['caution']?.toString() ?? '',
    );
  }
}
