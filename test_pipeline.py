#!/usr/bin/env python3
"""
Simple test script to run the master pipeline
"""

from master_pipeline import MasterPipeline

def main():
    # Run pipeline in test mode with 2 recipes
    pipeline = MasterPipeline(test_mode=True, test_recipes=2)
    success = pipeline.run_complete_pipeline()
    
    if success:
        print("\n🎉 Pipeline completed successfully!")
        print("🔨 You can now run './build_latex.sh' to compile the PDF")
    else:
        print("\n❌ Pipeline failed")

if __name__ == "__main__":
    main() 