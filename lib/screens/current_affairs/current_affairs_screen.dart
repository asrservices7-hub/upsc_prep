import 'package:flutter/material.dart';

class CurrentAffairsScreen extends StatelessWidget {
  const CurrentAffairsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> mockAffairs = [
      {
        'title': 'New Economic Policy Reforms announced',
        'date': 'Aug 05, 2026',
        'summary': 'The government has announced sweeping changes to the current economic framework, focusing on sustainable development and digital infrastructure...',
        'category': 'Economy',
      },
      {
        'title': 'Supreme Court rules on Environmental Protection',
        'date': 'Aug 04, 2026',
        'summary': 'In a landmark judgment, the Supreme Court has mandated strict ecological assessments for all future industrial projects near coastal regions.',
        'category': 'Polity & Environment',
      },
      {
        'title': 'G20 Summit: Key Takeaways for India',
        'date': 'Aug 03, 2026',
        'summary': 'India secured several strategic partnerships in renewable energy and cyber security during the latest G20 summit.',
        'category': 'International Relations',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Daily Current Affairs'),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {},
          )
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: mockAffairs.length,
        itemBuilder: (context, index) {
          final item = mockAffairs[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            child: InkWell(
              borderRadius: BorderRadius.circular(16),
              onTap: () {
                // Open full article
              },
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Chip(
                          label: Text(
                            item['category']!,
                            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                          ),
                          backgroundColor: Theme.of(context).primaryColor.withOpacity(0.1),
                          labelStyle: TextStyle(color: Theme.of(context).primaryColor),
                        ),
                        Text(
                          item['date']!,
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      item['title']!,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(fontSize: 18),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      item['summary']!,
                      style: Theme.of(context).textTheme.bodyMedium,
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Text(
                          'Read more',
                          style: TextStyle(
                            color: Theme.of(context).colorScheme.secondary,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(width: 4),
                        Icon(Icons.arrow_forward, size: 16, color: Theme.of(context).colorScheme.secondary),
                      ],
                    )
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
