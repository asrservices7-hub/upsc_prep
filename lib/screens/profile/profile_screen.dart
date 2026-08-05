import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              // TODO: implement logout
            },
          )
        ],
      ),
      body: Center(
        child: Text(
          'User Profile & Progress',
          style: Theme.of(context).textTheme.titleLarge,
        ),
      ),
    );
  }
}
