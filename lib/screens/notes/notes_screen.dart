import 'package:flutter/material.dart';
import '../../widgets/exam_switcher.dart';
import 'notes_list_screen.dart';

class NotesScreen extends StatelessWidget {
  const NotesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> noteCategories = [
      {'title': 'Indian Polity', 'icon': Icons.account_balance, 'count': 45},
      {'title': 'Modern History', 'icon': Icons.history_edu, 'count': 32},
      {'title': 'Geography', 'icon': Icons.public, 'count': 28},
      {'title': 'Economy', 'icon': Icons.trending_up, 'count': 50},
      {'title': 'Environment', 'icon': Icons.eco, 'count': 15},
      {'title': 'Science & Tech', 'icon': Icons.science, 'count': 20},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Handwritten Notes'),
        actions: const [ExamSwitcher()],
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: 1.1,
        ),
        itemCount: noteCategories.length,
        itemBuilder: (context, index) {
          final category = noteCategories[index];
          return Card(
            elevation: 4,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: InkWell(
              borderRadius: BorderRadius.circular(16),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => NotesListScreen(category: category['title']),
                  ),
                );
              },
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Theme.of(context).primaryColor.withOpacity(0.1),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      category['icon'],
                      size: 40,
                      color: Theme.of(context).primaryColor,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    category['title'],
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${category['count']} PDFs',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
