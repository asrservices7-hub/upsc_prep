import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_database/firebase_database.dart';
import '../../providers/exam_provider.dart';
import '../../services/auth_service.dart';
import '../../widgets/exam_switcher.dart';
import 'broadcast_screen.dart';
import 'audience_screen.dart';
import 'manage_live_requests_screen.dart';

class LiveListScreen extends StatelessWidget {
  const LiveListScreen({super.key});

  Future<void> _requestToGoLive(BuildContext context, String exam, String email) async {
    final titleController = TextEditingController();
    
    final result = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Request to Go Live'),
        content: TextField(
          controller: titleController,
          decoration: const InputDecoration(labelText: 'Session Title', border: OutlineInputBorder()),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
          ElevatedButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Submit Request')),
        ],
      ),
    );

    if (result == true && titleController.text.isNotEmpty) {
      try {
        await FirebaseDatabase.instance.ref().child('live_requests').push().set({
          'title': titleController.text.trim(),
          'exam': exam,
          'userEmail': email,
          'status': 'pending', // pending, approved, rejected
          'timestamp': ServerValue.timestamp,
        });
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Live request submitted! Wait for admin approval.')),
          );
        }
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Failed to request: $e')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();
    final isAdmin = authService.isAdmin;
    final currentUserEmail = authService.user?.email ?? '';

    return Consumer<ExamProvider>(
      builder: (context, examProvider, child) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Live Classes'),
            actions: const [ExamSwitcher()],
          ),
          body: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (isAdmin) ...[
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => BroadcastScreen(
                                  channelName: examProvider.selectedExam.replaceAll(' ', ''),
                                ),
                              ),
                            );
                          },
                          icon: const Icon(Icons.videocam),
                          label: const Text('Instant Live'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            backgroundColor: Colors.redAccent,
                            foregroundColor: Colors.white,
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const ManageLiveRequestsScreen(),
                              ),
                            );
                          },
                          icon: const Icon(Icons.admin_panel_settings),
                          label: const Text('Manage Requests'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                ] else ...[
                  ElevatedButton.icon(
                    onPressed: () => _requestToGoLive(context, examProvider.selectedExam, currentUserEmail),
                    icon: const Icon(Icons.waving_hand),
                    label: const Text('Request to Go Live'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      backgroundColor: Colors.blueAccent,
                      foregroundColor: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 24),
                ],

                Text(
                  'Active Live Streams',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 8),
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.live_tv, color: Colors.redAccent),
                    title: Text('${examProvider.selectedExam} Live Session'),
                    subtitle: const Text('Tap to join the ongoing class'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => AudienceScreen(
                            channelName: examProvider.selectedExam.replaceAll(' ', ''),
                          ),
                        ),
                      );
                    },
                  ),
                ),
                const SizedBox(height: 24),

                if (!isAdmin) ...[
                  Text(
                    'My Approved Broadcasts',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  Expanded(
                    child: StreamBuilder<DatabaseEvent>(
                      stream: FirebaseDatabase.instance
                          .ref()
                          .child('live_requests')
                          .orderByChild('userEmail')
                          .equalTo(currentUserEmail)
                          .onValue,
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return const Center(child: CircularProgressIndicator());
                        }

                        if (snapshot.data?.snapshot.value == null) {
                          return const Center(child: Text('You have no requests.'));
                        }

                        final Map<dynamic, dynamic> reqMap = snapshot.data!.snapshot.value as Map<dynamic, dynamic>;
                        final myRequests = reqMap.entries.map((e) => {
                          'id': e.key,
                          ...Map<String, dynamic>.from(e.value as Map)
                        }).where((r) => r['exam'] == examProvider.selectedExam).toList();

                        if (myRequests.isEmpty) {
                          return const Center(child: Text('No requests for this exam.'));
                        }

                        return ListView.builder(
                          itemCount: myRequests.length,
                          itemBuilder: (context, index) {
                            final req = myRequests[index];
                            final isApproved = req['status'] == 'approved';
                            return Card(
                              child: ListTile(
                                title: Text(req['title'] ?? 'Untitled'),
                                subtitle: Text('Status: ${req['status']}'),
                                trailing: isApproved
                                    ? ElevatedButton(
                                        onPressed: () {
                                          Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                              builder: (_) => BroadcastScreen(
                                                channelName: req['id'], // use request ID as unique channel
                                              ),
                                            ),
                                          );
                                        },
                                        style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
                                        child: const Text('Start Broadcast'),
                                      )
                                    : null,
                              ),
                            );
                          },
                        );
                      },
                    ),
                  ),
                ]
              ],
            ),
          ),
        );
      },
    );
  }
}
