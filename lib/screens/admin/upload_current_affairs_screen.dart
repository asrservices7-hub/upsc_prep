import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:intl/intl.dart';
import 'package:image_picker/image_picker.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import '../../config/gemini_config.dart';

class UploadCurrentAffairsScreen extends StatefulWidget {
  const UploadCurrentAffairsScreen({super.key});

  @override
  State<UploadCurrentAffairsScreen> createState() => _UploadCurrentAffairsScreenState();
}

class _UploadCurrentAffairsScreenState extends State<UploadCurrentAffairsScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _summaryController = TextEditingController();
  final _sourceUrlController = TextEditingController();
  
  String _selectedExam = 'UPSC';
  final List<String> _exams = [
    'UPSC',
    'State PCS',
    'RO / ARO',
    'High Court',
    'PO'
  ];

  String _selectedCategory = 'Economy';
  final List<String> _categories = [
    'Economy',
    'Polity',
    'Environment',
    'International Relations',
    'Science & Tech',
    'History & Culture',
    'Geography'
  ];

  bool _isUploading = false;
  bool _isExtractingText = false;

  Future<void> _extractTextFromImage() async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(source: ImageSource.gallery);
      
      if (image == null) return;

      setState(() => _isExtractingText = true);

      final bytes = await image.readAsBytes();
      
      final model = GenerativeModel(
        model: 'gemini-1.5-flash',
        apiKey: GeminiConfig.apiKey,
      );

      final prompt = TextPart('Extract the text from this image and format it cleanly as a summary. Remove any unwanted characters.');
      final imagePart = DataPart('image/jpeg', bytes);

      final response = await model.generateContent([
        Content.multi([prompt, imagePart])
      ]);

      if (response.text != null) {
        setState(() {
          _summaryController.text = response.text!;
        });
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Text extracted successfully!')),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to extract text: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isExtractingText = false);
      }
    }
  }

  Future<void> _uploadData() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() => _isUploading = true);
    
    try {
      final String dateString = DateFormat('MMM dd, yyyy').format(DateTime.now());
      
      await FirebaseDatabase.instance.ref().child('current_affairs').child(_selectedExam).push().set({
        'title': _titleController.text.trim(),
        'summary': _summaryController.text.trim(),
        'source_url': _sourceUrlController.text.trim(),
        'category': _selectedCategory,
        'date': dateString,
        'timestamp': ServerValue.timestamp,
      });
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Successfully uploaded current affairs!')),
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
        setState(() => _isUploading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Upload Current Affairs'),
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
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Content', style: TextStyle(fontWeight: FontWeight.bold)),
                  _isExtractingText 
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    : TextButton.icon(
                        onPressed: _extractTextFromImage,
                        icon: const Icon(Icons.document_scanner),
                        label: const Text('Scan Image to Text'),
                      ),
                ],
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _summaryController,
                maxLines: 5,
                decoration: const InputDecoration(
                  labelText: 'Summary / Content',
                  border: OutlineInputBorder(),
                  alignLabelWithHint: true,
                ),
                validator: (val) => val == null || val.isEmpty ? 'Required' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _sourceUrlController,
                decoration: const InputDecoration(
                  labelText: 'Source URL (Optional)',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.url,
              ),
              const SizedBox(height: 32),
              _isUploading
                  ? const Center(child: CircularProgressIndicator())
                  : ElevatedButton.icon(
                      onPressed: _uploadData,
                      icon: const Icon(Icons.cloud_upload),
                      label: const Text('Upload to App'),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                    ),
            ],
          ),
        ),
      ),
    );
  }
  
  @override
  void dispose() {
    _titleController.dispose();
    _summaryController.dispose();
    _sourceUrlController.dispose();
    super.dispose();
  }
}
