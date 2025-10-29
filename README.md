# FUTURE_CS_03

# Secure File Sharing System
A secure, production-ready file sharing system built with Python Flask that provides comprehensive security measures for safe file uploads and storage.

🚀 Features

· 🔒 Secure File Upload - Whitelist-based file type validation
· 🛡️ Malware Protection - Blocks executable and script files
· 📏 Size Limits - 16MB maximum file size enforcement
· 🔍 File Integrity - MD5 hash verification for uploaded files
· 🚫 Path Traversal Prevention - Secure filename handling
· ✅ Comprehensive Testing - 100% security test pass rate

📋 Security Test Results

✅ All Security Tests Passing

Test Category Result Details
File Type Validation ✅ PASS 15+ file extensions tested
Malicious File Blocking ✅ PASS 100% effectiveness
File Integrity ✅ PASS No corruption detected
Size Limits ✅ PASS 16MB limit enforced
Path Traversal ✅ PASS All attempts blocked

🧪 Test Coverage

· Normal files (.txt, .pdf, .jpg, .png) → Correctly allowed
· Executable files (.exe, .bat) → Correctly blocked
· Script files (.php, .html) → Correctly blocked
· Path traversal attempts → Correctly blocked
· Double extensions → Correctly blocked

Prerequisites

· Python 3.8 or higher
· pip package manager
A Flask-based web application for secure file uploads and downloads with encryption.


## Installation
1. Clone this repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python app.py`

## Usage
- Visit `http://localhost:5000`
- Upload files using the form
