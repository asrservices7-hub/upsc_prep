import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';

class ManageLiveRequestsScreen extends StatelessWidget {
  const ManageLiveRequestsScreen({super.key});

  Future<void> _updateRequestStatus(BuildContext context, String requestId, String status) async {
    try {
      await FirebaseDatabase.instance.ref().child('live_requests').child(requestId).update({
        'status': status,
      });
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Request marked as $status')),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error updating request: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Manage Live Requests'),
      ),
      body: StreamBuilder<DatabaseEvent>(
        stream: FirebaseDatabase.instance
            .ref()
            .child('live_requests')
            .orderByChild('status')
            .equalTo('pending')
            .onValue,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.data?.snapshot.value == null) {
            return const Center(child: Text('No pending live requests.'));
          }

          final Map<dynamic, dynamic> requestsMap = snapshot.data!.snapshot.value as Map<dynamic, dynamic>;
          final requestsList = requestsMap.entries.map((e) => {
            'id': e.key,
            ...Map<String, dynamic>.from(e.value as Map)
          }).toList();

          return ListView.builder(
            itemCount: requestsList.length,
            padding: const EdgeInsets.all(16),
            itemBuilder: (context, index) {
              final request = requestsList[index];
              return Card(
                child: ListTile(
                  title: Text(request['title'] ?? 'Untitled Session'),
                  subtitle: Text('Exam: ${request['exam']}\nRequested by: ${request['userEmail']}'),
                  isThreeLine: true,
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.check, color: Colors.green),
                        onPressed: () => _updateRequestStatus(context, request['id'], 'approved'),
                        tooltip: 'Approve',
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.red),
                        onPressed: () => _updateRequestStatus(context, request['id'], 'rejected'),
                        tooltip: 'Reject',
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
