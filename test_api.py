"""
Simple test script for AutoGrader API
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
import os
from pathlib import Path

# Base URL of your API
BASE_URL = "http://127.0.0.1:8000"

def test_upload_exam():
    """Test uploading an exam"""
    print("🧪 Testing: Upload Exam...")
    
    # Use existing exam files if they exist
    exam_dir = Path("uploads/exams/exam3")
    
    if not exam_dir.exists():
        print("❌ Error: Exam files not found. Please create uploads/exams/exam3/ with questions.pdf, correction.pdf, bareme.pdf")
        return False
    
    url = f"{BASE_URL}/api/upload_exam"
    
    files = {
        'questions': open(exam_dir / 'questions.pdf', 'rb'),
        'correction': open(exam_dir / 'correction.pdf', 'rb'),
        'bareme': open(exam_dir / 'bareme.pdf', 'rb')
    }
    
    data = {
        'exam_name': 'test_exam_python'
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        files['questions'].close()
        files['correction'].close()
        files['bareme'].close()
        
        if response.status_code == 200:
            print("✅ Exam uploaded successfully!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_grade_student():
    """Test grading a student's work"""
    print("\n🧪 Testing: Grade Student...")
    
    student_file = Path("data/students/exam3/zinebelmrabet.pdf")
    
    if not student_file.exists():
        print("❌ Error: Student file not found. Please check data/students/exam3/")
        return False
    
    url = f"{BASE_URL}/api/grade_student"
    
    files = {
        'copy': open(student_file, 'rb')
    }
    
    data = {
        'exam_name': 'test_exam_python',
        'student_name': 'test_student_python'
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        files['copy'].close()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Student graded successfully!")
            print(f"   Student: {result.get('student')}")
            print(f"   Grade: {result.get('grade')}/20")
            print(f"   Similarity: {result.get('similarity_score', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_grades():
    """Test getting all grades for an exam"""
    print("\n🧪 Testing: Get All Grades...")
    
    url = f"{BASE_URL}/grade/test_exam_python"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Grades retrieved successfully!")
            print(f"   Exam: {result.get('exam')}")
            print(f"   Grades: {result.get('grades')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("=" * 50)
    print("AutoGrader API Test Script")
    print("=" * 50)
    print("\n⚠️  Make sure the server is running!")
    print("   Run: uvicorn app.main:app --reload\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print("❌ Server is not running! Please start it first.")
            return
    except:
        print("❌ Cannot connect to server! Please start it first.")
        print("   Run: uvicorn app.main:app --reload")
        return
    
    print("✅ Server is running!\n")
    
    # Run tests
    test1 = test_upload_exam()
    test2 = test_grade_student() if test1 else False
    test3 = test_get_grades() if test2 else False
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"  Upload Exam: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  Grade Student: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"  Get Grades: {'✅ PASS' if test3 else '❌ FAIL'}")
    print("=" * 50)


if __name__ == "__main__":
    main()


