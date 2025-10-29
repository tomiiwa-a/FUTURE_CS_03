import os
import requests
import hashlib

class SecurityTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.upload_dir = "static/files"
        
    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of file for integrity checking"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def test_file_integrity(self):
        """Test that uploaded files maintain integrity"""
        print("🧪 TESTING FILE INTEGRITY...")
        
        # Create test file
        test_content = b"This is a test file for integrity checking"
        test_filename = "integrity_test.txt"
        
        with open(test_filename, 'wb') as f:
            f.write(test_content)
        
        try:
            # Upload file via API (no CSRF needed)
            with open(test_filename, 'rb') as f:
                files = {'file': (test_filename, f)}
                response = requests.post(f"{self.base_url}/api/upload", files=files)
            
            result = response.json()
            
            if result.get('success'):
                # Check if file exists in upload directory
                uploaded_path = os.path.join(self.upload_dir, test_filename)
                if os.path.exists(uploaded_path):
                    # Verify content
                    with open(uploaded_path, 'rb') as f:
                        uploaded_content = f.read()
                    
                    if uploaded_content == test_content:
                        print("✅ PASS: File integrity maintained")
                    else:
                        print("❌ FAIL: File integrity compromised")
                else:
                    print("❌ FAIL: File not found after upload")
            else:
                print(f"❌ FAIL: File upload failed - {result.get('error')}")
        
        except Exception as e:
            print(f"❌ ERROR during integrity test: {e}")
        
        # Cleanup
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    def test_security_measures(self):
        """Test various security vulnerabilities"""
        print("\n🔒 TESTING SECURITY MEASURES...")
        
        test_cases = [
            ("normal.txt", b"safe content", True, "Normal text file"),
            ("test.exe", b"malicious exe", False, "Executable file"),
            ("script.php", b"<?php echo 'test' ?>", False, "PHP file"),
            ("../../../etc/passwd", b"path traversal content", False, "Path traversal attempt"),
            ("file.html", b"<script>alert('xss')</script>", False, "HTML with scripts"),
            ("file.exe.jpg", b"fake image content", False, "Double extension"),
            ("normal.jpg", b"fake image content", True, "Allowed image file"),
        ]
        
        for test_case in test_cases:
            filename, content, should_work, description = test_case
            print(f"Testing: {description}")
            
            try:
                # Upload via API
                files = {'file': (filename, content)}
                response = requests.post(f"{self.base_url}/api/upload", files=files)
                result = response.json()
                
                success = result.get('success', False)
                
                if should_work and success:
                    print("  ✅ PASS: Correctly allowed")
                elif not should_work and not success:
                    print("  ✅ PASS: Correctly blocked")
                elif should_work and not success:
                    print(f"  ❌ FAIL: Should have been allowed but was blocked - {result.get('error')}")
                else:
                    print(f"  ❌ FAIL: Should have been blocked but was allowed")
                    
            except Exception as e:
                print(f"  ❌ ERROR: {e}")
    
    def test_large_file(self):
        """Test file size limits"""
        print("\n📏 TESTING FILE SIZE LIMITS...")
        
        # Create a large file (17MB - over the 16MB limit)
        large_filename = "large_file.bin"
        try:
            with open(large_filename, 'wb') as f:
                f.write(b'x' * (17 * 1024 * 1024))  # 17MB
            
            with open(large_filename, 'rb') as f:
                files = {'file': (large_filename, f)}
                response = requests.post(f"{self.base_url}/api/upload", files=files)
            
            # Large files should be blocked by Flask
            if response.status_code == 413 or "413" in str(response.status_code):
                print("✅ PASS: Large file correctly blocked (413 error)")
            else:
                result = response.json()
                if not result.get('success'):
                    print("✅ PASS: Large file correctly blocked")
                else:
                    print("❌ FAIL: Large file was not blocked")
                
        except Exception as e:
            print(f"✅ PASS: Large file caused error (as expected)")
        finally:
            if os.path.exists(large_filename):
                os.remove(large_filename)
    
    def test_csrf_protection(self):
        """Test CSRF protection on main form"""
        print("\n🛡️ TESTING CSRF PROTECTION...")
        
        # Try to submit to main form without CSRF token
        files = {'file': ('test.txt', b'test content')}
        response = requests.post(f"{self.base_url}/", files=files)
        
        if "CSRF" in response.text or response.status_code != 200:
            print("✅ PASS: CSRF protection is working on main form")
        else:
            print("❌ WARNING: CSRF protection may be weak")
    
    def test_allowed_extensions(self):
        """Test all allowed file extensions"""
        print("\n📄 TESTING ALLOWED EXTENSIONS...")
        
        allowed_files = [
            ("test.txt", b"text content", "Text file"),
            ("document.pdf", b"pdf content", "PDF file"), 
            ("image.png", b"png content", "PNG image"),
            ("photo.jpg", b"jpg content", "JPG image"),
            ("picture.jpeg", b"jpeg content", "JPEG image"),
            ("animation.gif", b"gif content", "GIF image"),
            ("doc.doc", b"doc content", "DOC document"),
            ("document.docx", b"docx content", "DOCX document"),
        ]
        
        for test_case in allowed_files:
            filename, content, description = test_case
            print(f"Testing: {description}")
            
            try:
                files = {'file': (filename, content)}
                response = requests.post(f"{self.base_url}/api/upload", files=files)
                result = response.json()
                
                if result.get('success'):
                    print("  ✅ PASS: Correctly allowed")
                else:
                    print(f"  ❌ FAIL: Should have been allowed - {result.get('error')}")
                    
            except Exception as e:
                print(f"  ❌ ERROR: {e}")
    
    def run_all_tests(self):
        """Run all security and integrity tests"""
        print("🚀 STARTING COMPREHENSIVE SECURITY TEST SUITE")
        print("=" * 50)
        
        self.test_file_integrity()
        self.test_security_measures() 
        self.test_large_file()
        self.test_csrf_protection()
        self.test_allowed_extensions()
        
        print("\n" + "=" * 50)
        print("🎯 SECURITY TESTING COMPLETE")

if __name__ == "__main__":
    # Check if server is running first
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ Flask server is running. Starting tests...")
        tester = SecurityTester()
        tester.run_all_tests()
    except requests.ConnectionError:
        print("❌ ERROR: Flask server is not running!")
        print("Please start your Flask app first:")
        print("1. Open terminal and navigate to project folder")
        print("2. Activate virtual environment: .venv\\Scripts\\activate") 
        print("3. Run: python app.py")
        print("4. Then run this test in a NEW terminal window")
    except Exception as e:
        print(f"❌ ERROR: {e}")