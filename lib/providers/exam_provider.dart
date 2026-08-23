import 'package:flutter/material.dart';

class ExamProvider with ChangeNotifier {
  static const List<String> availableExams = [
    'UPSC',
    'State PCS',
    'RO / ARO',
    'High Court',
    'PO'
  ];

  String _selectedExam = availableExams.first;

  String get selectedExam => _selectedExam;

  void setExam(String exam) {
    if (_selectedExam != exam && availableExams.contains(exam)) {
      _selectedExam = exam;
      notifyListeners();
    }
  }
}
