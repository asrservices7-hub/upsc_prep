import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:provider/provider.dart';
import '../../providers/exam_provider.dart';
import '../../widgets/exam_switcher.dart';

class NotesListScreen extends StatelessWidget {
  final String category;

  const NotesListScreen({super.key, required this.category});

  @override
  Widget build(BuildContext context) {
    return Consumer<ExamProvider>(
      builder: (context, examProvider, child) {
        return Scaffold(
          appBar: AppBar(
            title: Text('$category Notes'),
            actions: const [ExamSwitcher()],
          ),
          body: StreamBuilder<DatabaseEvent>(
            stream: FirebaseDatabase.instance
                .ref()
                .child('notes')
                .child(examProvider.selectedExam)
                .orderByChild('category')
                .equalTo(category)
                .onValue,
            builder: (context, snapshot) {
              if (snapshot.hasError || snapshot.data?.snapshot.value == null) {
                // FALLBACK MOCK DATA IF FIREBASE IS EMPTY
                final mockNotes = [
                  {
                    'title': 'Indian Polity — Fundamental Rights',
                    'summary': 'Part III (Art 12-35). Covers Right to Equality, Freedom, etc. Art 32 is Heart & Soul of Constitution (Ambedkar).',
                    'timestamp': DateTime.now().millisecondsSinceEpoch,
                    'pdfUrl': ''
                  },
                  {
                    'title': 'Indian Polity by M. Laxmikant',
                    'summary': 'The Bible of UPSC Polity. Covers Constitution, Parliament, Judiciary, Local Govt, and all Constitutional/Non-Constitutional bodies.',
                    'timestamp': DateTime.now().millisecondsSinceEpoch - 1000,
                    'pdfUrl': ''
                  },
                  {
                    'title': 'Modern History — Revolt of 1857',
                    'summary': 'Started on 10 May 1857 at Meerut. Causes include Doctrine of Lapse, economic drain, military discrimination.',
                    'timestamp': DateTime.now().millisecondsSinceEpoch - 2000,
                    'pdfUrl': ''
                  },
                  {
                    'title': 'Economy — Banking & Monetary Policy',
                    'summary': 'RBI established 1935. MPC has 6 members, sets repo rate. Target CPI inflation 4% (±2%).',
                    'timestamp': DateTime.now().millisecondsSinceEpoch - 3000,
                    'pdfUrl': ''
                  }
                ];

                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: mockNotes.length,
                  itemBuilder: (context, index) {
                    final data = mockNotes[index];
                    final title = data['title'] as String;
                    final summary = data['summary'] as String;
                    
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ExpansionTile(
                        leading: Icon(
                          Icons.menu_book,
                          color: Theme.of(context).primaryColor,
                          size: 32,
                        ),
                        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                        subtitle: Text(
                          summary,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Text(
                              summary,
                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(height: 1.6),
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                );
              }

              final Map<dynamic, dynamic> notesMap =
                  snapshot.data!.snapshot.value as Map<dynamic, dynamic>;

              final notesList = notesMap.entries.map((e) => {
                'id': e.key,
                ...Map<String, dynamic>.from(e.value as Map)
              }).toList();

              notesList.sort((a, b) {
                final int timeA = a['timestamp'] ?? 0;
                final int timeB = b['timestamp'] ?? 0;
                return timeB.compareTo(timeA);
              });

              if (notesList.isEmpty) {
                return const Center(child: Text('No notes available in this category yet.'));
              }

              return ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: notesList.length,
                itemBuilder: (context, index) {
                  final data = notesList[index];
                  final title = data['title'] ?? 'Untitled Note';
                  final summary = data['summary'] ?? '';
                  final pdfUrl = data['pdfUrl'] ?? '';
                  final hasPdf = pdfUrl.isNotEmpty;

                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ExpansionTile(
                      leading: Icon(
                        hasPdf ? Icons.picture_as_pdf : Icons.menu_book,
                        color: hasPdf ? Colors.redAccent : Theme.of(context).primaryColor,
                        size: 32,
                      ),
                      title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: summary.isNotEmpty
                          ? Text(
                              summary,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: Theme.of(context).textTheme.bodySmall,
                            )
                          : null,
                      children: [
                        if (summary.isNotEmpty)
                          Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Text(
                              summary,
                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(height: 1.6),
                            ),
                          ),
                      ],
                    ),
                  );
                },
              );
            },
          ),
        );
      },
    );
  }
}
