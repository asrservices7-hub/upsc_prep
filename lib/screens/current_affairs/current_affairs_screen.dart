import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../providers/exam_provider.dart';
import '../../widgets/exam_switcher.dart';
import '../../data/static_data.dart';

class CurrentAffairsScreen extends StatelessWidget {
  const CurrentAffairsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ExamProvider>(
      builder: (context, examProvider, child) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Daily Feed'),
            actions: [
              const ExamSwitcher(),
              IconButton(
                icon: const Icon(Icons.search),
                onPressed: () {},
              )
            ],
          ),
          body: StreamBuilder<DatabaseEvent>(
            stream: FirebaseDatabase.instance
                .ref()
                .child('current_affairs')
                .child(examProvider.selectedExam)
                .orderByChild('timestamp')
                .onValue,
            builder: (context, snapshot) {
          if (snapshot.hasError || snapshot.data?.snapshot.value == null) {
            final mockAffairs = StaticData.currentAffairs;

            return ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: mockAffairs.length,
              itemBuilder: (context, index) {
                final data = mockAffairs[index];
                
                final title = data['title'] as String;
                final category = data['category'] as String;
                final date = data['date'] as String;
                final summary = data['summary'] as String;
                final sourceUrl = data['source_url'] as String;

                return Card(
                  margin: const EdgeInsets.only(bottom: 16),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(16),
                    onTap: () async {
                      if (sourceUrl.isNotEmpty) {
                        final url = Uri.parse(sourceUrl);
                        if (await canLaunchUrl(url)) {
                          await launchUrl(url);
                        } else {
                          if (context.mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Could not launch URL')),
                            );
                          }
                        }
                      }
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
                                  category,
                                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                                ),
                                backgroundColor: Theme.of(context).primaryColor.withOpacity(0.1),
                                labelStyle: TextStyle(color: Theme.of(context).primaryColor),
                              ),
                              Text(
                                date,
                                style: Theme.of(context).textTheme.bodyMedium,
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text(
                            title,
                            style: Theme.of(context).textTheme.titleLarge?.copyWith(fontSize: 18),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            summary,
                            style: Theme.of(context).textTheme.bodyMedium,
                            maxLines: 3,
                            overflow: TextOverflow.ellipsis,
                          ),
                          if (sourceUrl.isNotEmpty) ...[
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                Text(
                                  'Read Full Article',
                                  style: TextStyle(
                                    color: Theme.of(context).colorScheme.secondary,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(width: 4),
                                Icon(Icons.open_in_new, size: 16, color: Theme.of(context).colorScheme.secondary),
                              ],
                            )
                          ],
                        ],
                      ),
                    ),
                  ),
                );
              },
            );
          }

          final Map<dynamic, dynamic> affairsMap = snapshot.data!.snapshot.value as Map<dynamic, dynamic>;
          
          // Convert to list and sort by timestamp descending
          final affairsList = affairsMap.entries.map((e) => {
            'id': e.key,
            ...Map<String, dynamic>.from(e.value as Map)
          }).toList();
          
          affairsList.sort((a, b) {
            final int timeA = a['timestamp'] ?? 0;
            final int timeB = b['timestamp'] ?? 0;
            return timeB.compareTo(timeA); // Descending
          });

          if (affairsList.isEmpty) {
            return const Center(child: Text('No current affairs found.'));
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: affairsList.length,
            itemBuilder: (context, index) {
              final data = affairsList[index];
              
              final title = data['title'] ?? 'No Title';
              final category = data['category'] ?? 'Uncategorized';
              final date = data['date'] ?? '';
              final summary = data['summary'] ?? '';
              final sourceUrl = data['source_url'] ?? '';

              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                child: InkWell(
                  borderRadius: BorderRadius.circular(16),
                  onTap: () async {
                    if (sourceUrl.isNotEmpty) {
                      final url = Uri.parse(sourceUrl);
                      if (await canLaunchUrl(url)) {
                        await launchUrl(url);
                      } else {
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Could not launch URL')),
                          );
                        }
                      }
                    }
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
                                category,
                                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                              ),
                              backgroundColor: Theme.of(context).primaryColor.withOpacity(0.1),
                              labelStyle: TextStyle(color: Theme.of(context).primaryColor),
                            ),
                            Text(
                              date,
                              style: Theme.of(context).textTheme.bodyMedium,
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(
                          title,
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(fontSize: 18),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          summary,
                          style: Theme.of(context).textTheme.bodyMedium,
                          maxLines: 3,
                          overflow: TextOverflow.ellipsis,
                        ),
                        if (sourceUrl.isNotEmpty) ...[
                          const SizedBox(height: 12),
                          Row(
                            children: [
                              Text(
                                'Read Full Article',
                                style: TextStyle(
                                  color: Theme.of(context).colorScheme.secondary,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(width: 4),
                              Icon(Icons.open_in_new, size: 16, color: Theme.of(context).colorScheme.secondary),
                            ],
                          )
                        ],
                      ],
                    ),
                  ),
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
