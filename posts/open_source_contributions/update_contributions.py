#!/usr/bin/env python3
"""
Main script to update contributions and generate markdown
This script handles the full workflow: update database -> generate markdown
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"🔄 {description}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error running {script_name}:")
        print(result.stderr)
        return False
    
    # Print the script's output
    if result.stdout:
        print(result.stdout)
    
    return True

def main():
    """Main workflow"""
    print("🚀 Starting contributions update workflow...")
    print()
    
    # Step 1: Update database
    if not run_script("update_database.py", "Updating contributions database"):
        print("❌ Failed to update database. Exiting.")
        return 1
    
    print()
    
    # Step 2: Generate markdown
    if not run_script("generate_contributions.py", "Generating contributions.md"):
        print("❌ Failed to generate markdown. Exiting.")
        return 1
    
    print()
    print("✅ Workflow completed successfully!")
    print("📄 Your contributions.md file has been updated with the latest data.")
    
    # Show some stats
    if os.path.exists("database/metadata.json"):
        import json
        with open("database/metadata.json", "r") as f:
            metadata = json.load(f)
        print(f"📊 Database stats: {metadata.get('total_prs', 0)} PRs, {metadata.get('total_repos', 0)} repos")
        print(f"🕒 Last updated: {metadata.get('last_update', 'Unknown')}")
    
    return 0

if __name__ == "__main__":
    exit(main())
