import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/exam_provider.dart';

class ExamSwitcher extends StatelessWidget {
  const ExamSwitcher({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ExamProvider>(
      builder: (context, examProvider, child) {
        return Container(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          padding: const EdgeInsets.symmetric(horizontal: 12),
          decoration: BoxDecoration(
            color: Theme.of(context).primaryColor.withOpacity(0.1),
            borderRadius: BorderRadius.circular(20),
          ),
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: examProvider.selectedExam,
              icon: Icon(Icons.arrow_drop_down, color: Theme.of(context).primaryColor),
              style: TextStyle(
                color: Theme.of(context).primaryColor,
                fontWeight: FontWeight.bold,
              ),
              onChanged: (String? newValue) {
                if (newValue != null) {
                  examProvider.setExam(newValue);
                }
              },
              items: ExamProvider.availableExams
                  .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
          ),
        );
      },
    );
  }
}
