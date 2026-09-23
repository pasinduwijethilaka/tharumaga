import 'package:flutter/material.dart';

import '../models/yoga_model.dart';

class YogasScreen extends StatelessWidget {
  final List<YogaModel> yogas;

  const YogasScreen({
    super.key,
    required this.yogas,
  });

  IconData _iconForYoga(String id) {
    switch (id) {
      case 'gaja_kesari':
        return Icons.auto_awesome;
      case 'budha_aditya':
        return Icons.lightbulb_outline;
      case 'raja_yoga':
        return Icons.workspace_premium_outlined;
      case 'dhana_yoga':
        return Icons.account_balance_wallet_outlined;
      case 'mahapurusha_mars':
        return Icons.local_fire_department_outlined;
      case 'mahapurusha_mercury':
        return Icons.psychology_outlined;
      case 'mahapurusha_jupiter':
        return Icons.school_outlined;
      case 'mahapurusha_venus':
        return Icons.favorite_border;
      case 'mahapurusha_saturn':
        return Icons.shield_outlined;
      default:
        return Icons.auto_awesome_outlined;
    }
  }

  String _planetNames(List<String> planets) {
    const names = {
      'Sun': 'රවි',
      'Moon': 'චන්ද්‍ර',
      'Mars': 'කුජ',
      'Mercury': 'බුධ',
      'Jupiter': 'ගුරු',
      'Venus': 'ශුක්‍ර',
      'Saturn': 'ශනි',
      'Rahu': 'රාහු',
      'Ketu': 'කේතු',
    };

    return planets.map((p) => names[p] ?? p).join(' + ');
  }

  String _title(String id, String fallback) {
    const titles = {
      'gaja_kesari': 'ගජකේසරී යෝගය',
      'budha_aditya': 'බුධාදිත්‍ය යෝගය',
      'dharma_karmadhipati': 'ධර්ම කර්මාධිපති යෝගය',
      'raja_yoga': 'රාජ යෝගය',
      'dhana_yoga': 'ධන යෝගය',
      'mahapurusha_mars': 'රුචක යෝගය',
      'mahapurusha_mercury': 'භද්‍ර යෝගය',
      'mahapurusha_jupiter': 'හංස යෝගය',
      'mahapurusha_venus': 'මාලව්‍ය යෝගය',
      'mahapurusha_saturn': 'ශශ යෝගය',
    };
    return titles[id] ?? fallback;
  }

  String _category(String id, String fallback) {
    const categories = {
      'gaja_kesari': 'ප්‍රඥාව හා බලපෑම',
      'budha_aditya': 'බුද්ධිය හා සන්නිවේදනය',
      'dharma_karmadhipati': 'අරමුණ හා වෘත්තිය',
      'raja_yoga': 'ජයග්‍රහණ හා වගකීම',
      'dhana_yoga': 'සම්පත් හා සමෘද්ධිය',
      'mahapurusha_mars': 'පංච මහාපුරුෂ',
      'mahapurusha_mercury': 'පංච මහාපුරුෂ',
      'mahapurusha_jupiter': 'පංච මහාපුරුෂ',
      'mahapurusha_venus': 'පංච මහාපුරුෂ',
      'mahapurusha_saturn': 'පංච මහාපුරුෂ',
    };
    return categories[id] ?? fallback;
  }

  String _summary(String id, String fallback) {
    const summaries = {
      'gaja_kesari':
          'චන්ද්‍රයා සහ ගුරු අතර ඇති සම්ප්‍රදායික සංයෝගයකි. මෙම යෝගය ව්‍යුහාත්මකව පවතින විට, ඉගෙනීම, විනිශ්චය කිරීමේ හැකියාව, ආත්මවිශ්වාසය සහ සමාජ බලපෑම සමඟ සම්බන්ධ කර සලකනු ලැබේ.',
      'budha_aditya':
          'රවි සහ බුධ එකට පිහිටීමෙන් ඇතිවන සම්ප්‍රදායික සංයෝගයකි. බුද්ධිය, සන්නිවේදනය, විශ්ලේෂණාත්මක සිතීම සහ අදහස් පැහැදිලිව ප්‍රකාශ කිරීම සමඟ සම්බන්ධ කර සලකනු ලැබේ.',
      'dharma_karmadhipati':
          '9 වන සහ 10 වන භාව අධිපතීන් අතර ඇති සම්බන්ධතාවයකි. ධර්මය, මඟපෙන්වීම සහ අරමුණ වැනි කරුණු වෘත්තිය, වගකීම සහ ක්‍රියාකාරීත්වය සමඟ සම්බන්ධ කරයි.',
      'raja_yoga':
          'කේන්ද්‍ර සහ ත්‍රිකෝණ භාව අධිපතීන් අතර සුදුසු සම්බන්ධතාවයක් ඇති විට හඳුනාගන්නා යෝගයකි. ක්‍රියාකාරීත්වය, ස්ථාවරත්වය, අරමුණ සහ අවස්ථා වැනි කරුණු සමඟ සම්බන්ධ වේ.',
      'dhana_yoga':
          '2, 5, 9 සහ 11 වන භාව අධිපතීන් අතර සුදුසු සම්බන්ධතාවයක් ඇති විට හඳුනාගන්නා යෝගයකි. සම්පත්, ධනය, අවස්ථා සහ ලාභ වැනි කරුණු සමඟ සම්බන්ධ කර සලකනු ලැබේ.',
      'mahapurusha_mars':
          'කුජ මත පදනම් වූ පංච මහාපුරුෂ යෝගයකි. ධෛර්යය, ආරම්භක ශක්තිය, බලය සහ තීරණාත්මක ක්‍රියාකාරීත්වය සමඟ සම්ප්‍රදායිකව සම්බන්ධ වේ.',
      'mahapurusha_mercury':
          'බුධ මත පදනම් වූ පංච මහාපුරුෂ යෝගයකි. බුද්ධිය, සන්නිවේදනය, තර්කනය සහ කුසලතා සමඟ සම්ප්‍රදායිකව සම්බන්ධ වේ.',
      'mahapurusha_jupiter':
          'ගුරු මත පදනම් වූ පංච මහාපුරුෂ යෝගයකි. ප්‍රඥාව, ඉගෙනීම, ආචාරධර්ම සහ මඟපෙන්වීම සමඟ සම්ප්‍රදායිකව සම්බන්ධ වේ.',
      'mahapurusha_venus':
          'ශුක්‍ර මත පදනම් වූ පංච මහාපුරුෂ යෝගයකි. රසවත්භාවය, නිර්මාණශීලීත්වය, සබඳතා සහ සුවපහසුව සමඟ සම්ප්‍රදායිකව සම්බන්ධ වේ.',
      'mahapurusha_saturn':
          'ශනි මත පදනම් වූ පංච මහාපුරුෂ යෝගයකි. විනය, ඉවසීම, සංවිධානය සහ වගකීම සමඟ සම්ප්‍රදායිකව සම්බන්ධ වේ.',
    };
    return summaries[id] ?? fallback;
  }

  List<String> _themes(String id, List<String> fallback) {
    const themes = {
      'gaja_kesari': [
        'ඉගෙනීම හා දැනුම',
        'විනිශ්චය හා තීරණ ගැනීම',
        'ආත්මවිශ්වාසය',
        'සමාජ පිළිගැනීම'
      ],
      'budha_aditya': [
        'බුද්ධිමය ක්‍රියාකාරකම්',
        'සන්නිවේදනය',
        'විශ්ලේෂණය',
        'ඉගෙනීම',
        'ස්වයං ප්‍රකාශනය'
      ],
      'dharma_karmadhipati': [
        'ජීවිත අරමුණ',
        'වෘත්තීය දිශාව',
        'වගකීම',
        'මඟපෙන්වීම',
        'ක්‍රියාවෙන් ජයග්‍රහණය'
      ],
      'raja_yoga': [
        'ජයග්‍රහණ',
        'වගකීම',
        'නායකත්වය',
        'අවස්ථා',
        'ඵලදායී ක්‍රියාකාරීත්වය'
      ],
      'dhana_yoga': [
        'සම්පත්',
        'මූල්‍ය අවස්ථා',
        'සමුච්චය',
        'ලාභ',
        'ප්‍රායෝගික වටිනාකම'
      ],
      'mahapurusha_mars': [
        'ධෛර්යය',
        'ආරම්භක ශක්තිය',
        'උද්යෝගය',
        'තීරණාත්මක බව'
      ],
      'mahapurusha_mercury': ['තර්කනය', 'සන්නිවේදනය', 'විශ්ලේෂණය', 'කුසලතා'],
      'mahapurusha_jupiter': ['ප්‍රඥාව', 'ඉගෙනීම', 'ආචාරධර්ම', 'මඟපෙන්වීම'],
      'mahapurusha_venus': [
        'රසවත්භාවය',
        'නිර්මාණශීලීත්වය',
        'සබඳතා',
        'සුවපහසුව'
      ],
      'mahapurusha_saturn': ['විනය', 'ඉවසීම', 'සංවිධානය', 'වගකීම'],
    };
    return themes[id] ?? fallback;
  }

  String _lifeAreas(String id, List<String> fallback) {
    const areas = {
      'gaja_kesari':
          'අධ්‍යාපනය • සන්නිවේදනය • ගුරුවරුන් හා මඟපෙන්වන්නන් සමඟ සබඳතා • සමාජ ජීවිතය',
      'budha_aditya':
          'අධ්‍යාපනය • ලිවීම හා කථනය • ව්‍යාපාර හෝ විශ්ලේෂණාත්මක කටයුතු • සැලසුම් හා ගැටලු විසඳීම',
      'dharma_karmadhipati':
          'වෘත්තිය • වෘත්තීය වගකීම් • නායකත්වය • උසස් අධ්‍යාපනය හා මඟපෙන්වීම',
      'raja_yoga': 'වෘත්තිය • නායකත්වය • සමාජ වගකීම් • ප්‍රධාන ජීවන අරමුණු',
      'dhana_yoga':
          'ආදායම් හා සම්පත් • මූල්‍ය සැලසුම් • කුසලතා මඟින් ලැබෙන ලාභ • දිගුකාලීන භෞතික අරමුණු',
      'mahapurusha_mars': 'නායකත්වය • තරගකාරී ක්ෂේත්‍ර • ක්‍රියාකාරී වැඩ',
      'mahapurusha_mercury': 'අධ්‍යාපනය • ව්‍යාපාර • ලිවීම • තාක්ෂණික කටයුතු',
      'mahapurusha_jupiter': 'අධ්‍යාපනය • ඉගැන්වීම • මඟපෙන්වීම • උපදේශනය',
      'mahapurusha_venus': 'කලා • සබඳතා • නිර්මාණකරණය • ජීවන රටාව',
      'mahapurusha_saturn':
          'කළමනාකරණය • දිගුකාලීන වැඩ • පරිපාලනය • ව්‍යුහගත කටයුතු',
    };
    return areas[id] ?? fallback.join(' • ');
  }

  String _caution(String id, String fallback) {
    const cautions = {
      'gaja_kesari':
          'මෙම සංයෝගය පමණක් තිබීමෙන් එහි බලපෑම කොපමණ ප්‍රබලදැයි තීරණය කළ නොහැක. ග්‍රහ බලය, තත්ත්වය සහ සමස්ත කේන්දරය වෙන වෙනම සලකා බැලිය යුතුය.',
      'budha_aditya':
          'රවි-බුධ සංයෝගය පමණක් තිබීමෙන් අධ්‍යාපනික හෝ වෘත්තීය සාර්ථකත්වයක් සහතික නොවේ. ග්‍රහ බලය සහ තත්ත්වය වෙන වෙනම සලකා බැලිය යුතුය.',
      'dharma_karmadhipati':
          'මෙය කේන්දරයේ ව්‍යුහාත්මක සම්බන්ධතාවයක් පෙන්වන යෝගයකි. එය නිශ්චිත වෘත්තීය ප්‍රතිඵලයක් ලෙස නොසැලකිය යුතුය.',
      'raja_yoga':
          'රාජ යෝගයක් හඳුනාගැනීම ව්‍යුහාත්මක සලකුණක් පමණි. තත්ත්වය, බලය සහ දශා වැනි කරුණු සමඟ සමස්ත කේන්දරය සලකා බැලිය යුතුය.',
      'dhana_yoga':
          'ධන යෝගයක් තිබීමෙන් නිශ්චිත මුදල් ප්‍රමාණයක් ලැබෙන බව සහතික නොවේ. සමස්ත කේන්දරය, කාලය සහ සැබෑ ජීවන තත්ත්වයන් ද බලපායි.',
      'mahapurusha_mars':
          'මෙය ව්‍යුහාත්මක සලකුණකි. එහි ප්‍රකාශනය කුජගේ බලය සහ සමස්ත කේන්දරයේ තත්ත්වය මත වෙනස් විය හැක.',
      'mahapurusha_mercury':
          'මෙය ව්‍යුහාත්මක සලකුණකි. එහි ප්‍රකාශනය බුධගේ බලය සහ සමස්ත කේන්දරයේ තත්ත්වය මත වෙනස් විය හැක.',
      'mahapurusha_jupiter':
          'මෙය ව්‍යුහාත්මක සලකුණකි. එහි ප්‍රකාශනය ගුරුගේ බලය සහ සමස්ත කේන්දරයේ තත්ත්වය මත වෙනස් විය හැක.',
      'mahapurusha_venus':
          'මෙය ව්‍යුහාත්මක සලකුණකි. එහි ප්‍රකාශනය ශුක්‍රගේ බලය සහ සමස්ත කේන්දරයේ තත්ත්වය මත වෙනස් විය හැක.',
      'mahapurusha_saturn':
          'මෙය ව්‍යුහාත්මක සලකුණකි. එහි ප්‍රකාශනය ශනිගේ බලය සහ සමස්ත කේන්දරයේ තත්ත්වය මත වෙනස් විය හැක.',
    };
    return cautions[id] ?? fallback;
  }

  String _formation(String value) {
    if (value == 'Structural relationship identified.') {
      return 'ව්‍යුහාත්මක සම්බන්ධතාවය හඳුනාගෙන ඇත.';
    }

    const labels = {
      'same planetary lord': 'එකම භාව අධිපති',
      'conjunction in the same house': 'එකම භාවයේ සංයෝගය',
      'mutual planetary aspect': 'අන්‍යෝන්‍ය ග්‍රහ දෘෂ්ටිය',
      'sign exchange': 'රාශි මාරුව',
    };

    return value.split(', ').map((item) => labels[item] ?? item).join(', ');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('යෝග විස්තර'),
      ),
      body: yogas.isEmpty
          ? const Center(
              child: Text(
                'හඳුනාගත් ව්‍යුහාත්මක යෝග නොමැත.',
                style: TextStyle(fontSize: 16),
              ),
            )
          : ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: yogas.length,
              separatorBuilder: (_, __) => const SizedBox(height: 14),
              itemBuilder: (context, index) {
                final yoga = yogas[index];

                return Card(
                  elevation: 2,
                  clipBehavior: Clip.antiAlias,
                  child: Padding(
                    padding: const EdgeInsets.all(18),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            CircleAvatar(
                              radius: 24,
                              child: Icon(_iconForYoga(yoga.id)),
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    _title(yoga.id, yoga.title),
                                    style: Theme.of(context)
                                        .textTheme
                                        .titleLarge
                                        ?.copyWith(
                                          fontWeight: FontWeight.bold,
                                        ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    _category(yoga.id, yoga.category),
                                    style: Theme.of(context)
                                        .textTheme
                                        .bodyMedium
                                        ?.copyWith(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .primary,
                                          fontWeight: FontWeight.w600,
                                        ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          _summary(yoga.id, yoga.summary),
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 14),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            Chip(
                              avatar: const Icon(Icons.public, size: 18),
                              label: Text(_planetNames(yoga.planets)),
                            ),
                            if (yoga.houses.isNotEmpty)
                              Chip(
                                avatar: const Icon(
                                  Icons.home_outlined,
                                  size: 18,
                                ),
                                label: Text(
                                  'භාව ${yoga.houses.join(', ')}',
                                ),
                              ),
                          ],
                        ),
                        if (yoga.relationshipSummary.isNotEmpty) ...[
                          const SizedBox(height: 10),
                          Text(
                            'යෝගය සෑදෙන ආකාරය',
                            style: Theme.of(context)
                                .textTheme
                                .titleSmall
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          Text(_formation(yoga.relationshipSummary)),
                        ],
                        if (yoga.themes.isNotEmpty) ...[
                          const SizedBox(height: 12),
                          Text(
                            'ප්‍රධාන කරුණු',
                            style: Theme.of(context)
                                .textTheme
                                .titleSmall
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 6),
                          Wrap(
                            spacing: 6,
                            runSpacing: 6,
                            children: _themes(yoga.id, yoga.themes)
                                .map(
                                  (theme) => Chip(
                                    label: Text(theme),
                                    visualDensity: VisualDensity.compact,
                                  ),
                                )
                                .toList(),
                          ),
                        ],
                        if (yoga.lifeAreas.isNotEmpty) ...[
                          const SizedBox(height: 12),
                          Text(
                            'බලපාන ජීවන ක්ෂේත්‍ර',
                            style: Theme.of(context)
                                .textTheme
                                .titleSmall
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          Text(_lifeAreas(yoga.id, yoga.lifeAreas)),
                        ],
                        if (yoga.caution.isNotEmpty) ...[
                          const SizedBox(height: 14),
                          Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color:
                                  Theme.of(context).colorScheme.surfaceVariant,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              'සටහන: ${_caution(yoga.id, yoga.caution)}',
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
