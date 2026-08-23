import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:typed_data';

class UploadNotesScreen extends StatefulWidget {
  const UploadNotesScreen({super.key});

  @override
  State<UploadNotesScreen> createState() => _UploadNotesScreenState();
}

class _UploadNotesScreenState extends State<UploadNotesScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  
  String _selectedExam = 'UPSC';
  final List<String> _exams = [
    'UPSC',
    'State PCS',
    'RO / ARO',
    'High Court',
    'PO'
  ];

  String _selectedCategory = 'Indian Polity';
  final List<String> _categories = [
    'Indian Polity',
    'Modern History',
    'Geography',
    'Economy',
    'Environment',
    'Science & Tech',
  ];

  PlatformFile? _selectedFile;
  Uint8List? _fileBytes;
  bool _isUploading = false;
  double _uploadProgress = 0.0;

  Future<void> _pickFile() async {
    final result = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
      withData: true,
    );

    if (result != null) {
      setState(() {
        _selectedFile = result.files.first;
        _fileBytes = result.files.first.bytes;
      });
    }
  }

  Future<void> _uploadData() async {
    if (!_formKey.currentState!.validate()) return;
    if (_selectedFile == null || _fileBytes == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a PDF file first')),
      );
      return;
    }
    
    setState(() {
      _isUploading = true;
      _uploadProgress = 0.1;
    });
    
    try {
      // 1. Upload file to Firebase Storage
      final fileName = '${DateTime.now().millisecondsSinceEpoch}_${_selectedFile!.name}';
      final storageRef = FirebaseStorage.instance.ref().child('notes/$fileName');
      
      final uploadTask = storageRef.putData(
        _fileBytes!,
        SettableMetadata(contentType: 'application/pdf'),
      );
      
      uploadTask.snapshotEvents.listen((event) {
        setState(() {
          _uploadProgress = event.bytesTransferred / event.totalBytes;
        });
      });
      
      await uploadTask;
      final downloadUrl = await storageRef.getDownloadURL();
      
      // 2. Save metadata to Realtime Database
      await FirebaseDatabase.instance.ref().child('notes').child(_selectedExam).push().set({
        'title': _titleController.text.trim(),
        'category': _selectedCategory,
        'pdfUrl': downloadUrl,
        'fileName': _selectedFile!.name,
        'timestamp': ServerValue.timestamp,
      });
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Successfully uploaded notes!')),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to upload: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isUploading = false;
          _uploadProgress = 0.0;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Upload Notes'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(
                  labelText: 'Title',
                  border: OutlineInputBorder(),
                ),
                validator: (val) => val == null || val.isEmpty ? 'Required' : null,
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: _selectedExam,
                decoration: const InputDecoration(
                  labelText: 'Exam / Paper',
                  border: OutlineInputBorder(),
                ),
                items: _exams.map((exam) {
                  return DropdownMenuItem(value: exam, child: Text(exam));
                }).toList(),
                onChanged: (val) {
                  if (val != null) setState(() => _selectedExam = val);
                },
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: _selectedCategory,
                decoration: const InputDecoration(
                  labelText: 'Category',
                  border: OutlineInputBorder(),
                ),
                items: _categories.map((cat) {
                  return DropdownMenuItem(value: cat, child: Text(cat));
                }).toList(),
                onChanged: (val) {
                  if (val != null) setState(() => _selectedCategory = val);
                },
              ),
              const SizedBox(height: 24),
              OutlinedButton.icon(
                onPressed: _pickFile,
                icon: const Icon(Icons.picture_as_pdf),
                label: Text(_selectedFile != null ? 'Change File: ${_selectedFile!.name}' : 'Select PDF File'),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.all(16),
                  side: BorderSide(color: _selectedFile != null ? Colors.green : Colors.grey),
                ),
              ),
              if (_selectedFile != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: Text(
                    'Selected: ${_selectedFile!.name} (${(_selectedFile!.size / 1024 / 1024).toStringAsFixed(2)} MB)',
                    style: const TextStyle(color: Colors.green, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                  ),
                ),
              const SizedBox(height: 32),
              if (_isUploading) ...[
                LinearProgressIndicator(value: _uploadProgress),
                const SizedBox(height: 8),
                Text('${(_uploadProgress * 100).toStringAsFixed(0)}% uploaded', textAlign: TextAlign.center),
              ] else ...[
                ElevatedButton.icon(
                  onPressed: _uploadData,
                  icon: const Icon(Icons.cloud_upload),
                  label: const Text('Upload Notes to App'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ]
            ],
          ),
        ),
      ),
    );
  }
  
  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }
}
