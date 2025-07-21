#!/usr/bin/env python3
"""
API Testing Script for AI Services
Tests OpenAI GPT-4o-mini, Google Gemini 2.5, Perplexity Sonar Pro, and OpenAI DALL-E 3

Requirements:
- Create a .env file with your API keys (see env_template.txt)
- Install required packages: pip install openai google-generativeai perplexipy python-dotenv requests
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import time

# Import AI libraries
try:
    import openai
    import google.generativeai as genai
    from perplexipy import PerplexityClient
    import requests
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install required packages:")
    print("pip install openai google-generativeai perplexipy python-dotenv requests")
    sys.exit(1)

# Load environment variables
load_dotenv()

class APITester:
    def __init__(self):
        self.results = {}
        self.test_prompt = "What is the capital of France? Answer in one sentence."
        self.image_prompt = "A beautifully plated traditional Tunisian couscous dish with colorful vegetables, photographed in professional food photography style, top-down view, natural lighting"
        
    def print_header(self, service_name):
        print(f"\n{'='*60}")
        print(f"🧪 Testing {service_name}")
        print(f"{'='*60}")
        
    def print_result(self, success, response_text="", error_msg="", response_time=None):
        if success:
            print(f"✅ Status: SUCCESS")
            if response_time:
                print(f"⏱️  Response Time: {response_time:.2f} seconds")
            print(f"💬 Response: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
        else:
            print(f"❌ Status: FAILED")
            print(f"🚨 Error: {error_msg}")
            
    def test_openai_gpt4o_mini(self):
        """Test OpenAI GPT-4o-mini API"""
        self.print_header("OpenAI GPT-4o-mini")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            self.print_result(False, error_msg="OPENAI_API_KEY not found or not set in .env file")
            return False
            
        try:
            client = openai.OpenAI(api_key=api_key)
            
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": self.test_prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            end_time = time.time()
            
            response_text = response.choices[0].message.content
            self.print_result(True, response_text, response_time=end_time-start_time)
            return True
            
        except Exception as e:
            self.print_result(False, error_msg=str(e))
            return False
            
    def test_google_gemini_25(self):
        """Test Google Gemini 2.5 Flash API"""
        self.print_header("Google Gemini 2.5 Flash")
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'your_google_api_key_here':
            self.print_result(False, error_msg="GOOGLE_API_KEY not found or not set in .env file")
            return False
            
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            start_time = time.time()
            response = model.generate_content(self.test_prompt)
            end_time = time.time()
            
            response_text = response.text
            self.print_result(True, response_text, response_time=end_time-start_time)
            return True
            
        except Exception as e:
            self.print_result(False, error_msg=str(e))
            return False
            
    def test_perplexity_sonar_pro(self):
        """Test Perplexity Sonar Pro API"""
        self.print_header("Perplexity Sonar Pro")
        
        api_key = os.getenv('PERPLEXITY_API_KEY')
        if not api_key or api_key == 'your_perplexity_api_key_here':
            self.print_result(False, error_msg="PERPLEXITY_API_KEY not found or not set in .env file")
            return False
            
        try:
            client = PerplexityClient(key=api_key)
            
            start_time = time.time()
            # Test with a search-enabled query
            search_prompt = "What is the current weather in Paris, France today?"
            response = client.query(search_prompt)
            end_time = time.time()
            
            self.print_result(True, response, response_time=end_time-start_time)
            return True
            
        except Exception as e:
            self.print_result(False, error_msg=str(e))
            return False

    def test_openai_image_generation(self):
        """Test OpenAI DALL-E Image Generation"""
        self.print_header("OpenAI DALL-E Image Generation")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            self.print_result(False, error_msg="OPENAI_API_KEY not found or not set in .env file")
            return False
            
        try:
            client = openai.OpenAI(api_key=api_key)
            
            start_time = time.time()
            response = client.images.generate(
                model="dall-e-3",
                prompt=self.image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            end_time = time.time()
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Download and save the image to verify it worked
            import requests
            import urllib.parse
            
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                # Save the image
                filename = f"test_generated_image_{int(time.time())}.png"
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                
                success_msg = f"Image generated and saved as '{filename}'. URL: {image_url[:60]}..."
                self.print_result(True, success_msg, response_time=end_time-start_time)
                return True
            else:
                self.print_result(False, error_msg=f"Failed to download generated image. Status: {img_response.status_code}")
                return False
                
        except Exception as e:
            self.print_result(False, error_msg=str(e))
            return False
            
    def run_all_tests(self):
        """Run all API tests"""
        print(f"🚀 Starting API Key Tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📝 Test Prompt: '{self.test_prompt}'")
        
        # Test each service
        results = {
            'OpenAI GPT-4o-mini': self.test_openai_gpt4o_mini(),
            'Google Gemini 2.5': self.test_google_gemini_25(),
            'Perplexity Sonar Pro': self.test_perplexity_sonar_pro(),
            'OpenAI DALL-E 3': self.test_openai_image_generation()
        }
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 TEST SUMMARY")
        print(f"{'='*60}")
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for service, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{service:<25} {status}")
            
        print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All API keys are working correctly!")
        else:
            print("⚠️  Some API keys need attention. Check the errors above.")
            print("\n💡 Troubleshooting Tips:")
            print("1. Verify your API keys are correct in the .env file")
            print("2. Check that you have sufficient credits/quota")
            print("3. Ensure your API keys have the necessary permissions")
            print("4. For Perplexity, make sure you have a paid subscription")
            print("5. For DALL-E, ensure you have image generation credits/access")
            print("6. Generated images are saved locally for verification")
            
        return passed_tests == total_tests

def main():
    """Main function"""
    print("🤖 AI API Key Testing Script")
    print("Testing OpenAI (Chat + Image), Google Gemini, and Perplexity APIs")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n❌ .env file not found!")
        print("Please create a .env file using the template in env_template.txt")
        print("Then add your actual API keys to the .env file")
        sys.exit(1)
    
    # Run tests
    tester = APITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 