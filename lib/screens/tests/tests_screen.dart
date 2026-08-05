import 'package:flutter/material.dart';

class TestsScreen extends StatelessWidget {
  const TestsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> testSeries = [
      {
        'title': 'Prelims Full Mock Test 1',
        'questions': 100,
        'duration': '120 mins',
        'isPremium': false,
      },
      {
        'title': 'CSAT Practice Test (Math)',
        'questions': 80,
        'duration': '120 mins',
        'isPremium': true,
      },
      {
        'title': 'Polity Sectional Test',
        'questions': 50,
        'duration': '60 mins',
        'isPremium': true,
      },
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Test Series')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: testSeries.length,
        itemBuilder: (context, index) {
          final test = testSeries[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16),
              leading: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: test['isPremium'] 
                      ? Theme.of(context).colorScheme.secondary.withOpacity(0.1)
                      : Theme.of(context).primaryColor.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  test['isPremium'] ? Icons.workspace_premium : Icons.quiz,
                  color: test['isPremium'] 
                      ? Theme.of(context).colorScheme.secondary 
                      : Theme.of(context).primaryColor,
                ),
              ),
              title: Text(
                test['title'],
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Row(
                  children: [
                    const Icon(Icons.timer_outlined, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Text('${test['duration']}'),
                    const SizedBox(width: 16),
                    const Icon(Icons.format_list_bulleted, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Text('${test['questions']} Qs'),
                  ],
                ),
              ),
              trailing: ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  backgroundColor: test['isPremium'] 
                      ? Theme.of(context).colorScheme.secondary 
                      : Theme.of(context).primaryColor,
                ),
                child: Text(test['isPremium'] ? 'Unlock' : 'Start'),
              ),
            ),
          );
        },
      ),
    );
  }
}
