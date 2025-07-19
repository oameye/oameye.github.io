#!/usr/bin/env python3
"""
Update the contributions database with new GitHub data
This script maintains a persistent database of all contributions to avoid GitHub's 1000 limit
"""

import json
import subprocess
import os
from datetime import datetime, timedelta
from collections import defaultdict

def run_gh_command(cmd):
    """Run a GitHub CLI command and return parsed JSON output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"Error: {result.stderr}")
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from command: {cmd}")
        return []

def load_database():
    """Load existing database files"""
    db = {
        'prs': [],
        'repos': [],
        'last_update': None
    }
    
    if os.path.exists('database/prs.json'):
        with open('database/prs.json', 'r') as f:
            db['prs'] = json.load(f)
    
    if os.path.exists('database/repos.json'):
        with open('database/repos.json', 'r') as f:
            db['repos'] = json.load(f)
    
    if os.path.exists('database/metadata.json'):
        with open('database/metadata.json', 'r') as f:
            metadata = json.load(f)
            db['last_update'] = metadata.get('last_update')
    
    return db

def save_database(db):
    """Save database to files"""
    os.makedirs('database', exist_ok=True)
    
    with open('database/prs.json', 'w') as f:
        json.dump(db['prs'], f, indent=2)
    
    with open('database/repos.json', 'w') as f:
        json.dump(db['repos'], f, indent=2)
    
    metadata = {
        'last_update': datetime.now().isoformat(),
        'total_prs': len(db['prs']),
        'total_repos': len(db['repos'])
    }
    with open('database/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

def merge_prs(existing_prs, new_prs):
    """Merge new PRs with existing ones, avoiding duplicates"""
    # Create a set of existing PR URLs for quick lookup
    existing_urls = {pr.get('url') for pr in existing_prs}
    
    # Add new PRs that don't already exist
    for pr in new_prs:
        if pr.get('url') not in existing_urls:
            existing_prs.append(pr)
            print(f"Added new PR: {pr.get('title', 'Unknown')} to {pr.get('repository', {}).get('nameWithOwner', 'Unknown')}")
    
    return existing_prs

def merge_repos(existing_repos, new_repos):
    """Merge new repos with existing ones, updating existing entries"""
    # Create a dict of existing repos by name for quick lookup and updates
    existing_dict = {repo.get('name'): repo for repo in existing_repos}
    
    for repo in new_repos:
        repo_name = repo.get('name')
        if repo_name in existing_dict:
            # Update existing repo (stars might have changed, etc.)
            existing_dict[repo_name].update(repo)
        else:
            # Add new repo
            existing_repos.append(repo)
            print(f"Added new repo: {repo_name}")
    
    return existing_repos

def fetch_new_data(last_update=None):
    """Fetch new data from GitHub, optionally since last update"""
    print("Fetching data from GitHub...")
    
    # Fetch all PRs (we'll filter client-side for efficiency)
    closed_prs = run_gh_command("gh search prs --author=oameye --state=closed --limit=1000 --json title,url,repository,createdAt,state,closedAt")
    open_prs = run_gh_command("gh search prs --author=oameye --state=open --limit=1000 --json title,url,repository,createdAt,state")
    
    # Combine all PRs
    all_prs = closed_prs + open_prs
    
    # If we have a last update date, we could filter here, but GitHub search doesn't support date ranges well
    # So we'll fetch all and let merge_prs handle duplicates
    
    # Fetch all repositories
    repos = run_gh_command("gh repo list oameye --limit=1000 --json name,description,url,isPrivate,createdAt,stargazerCount,isFork")
    
    return all_prs, repos

def update_database():
    """Main function to update the database"""
    print("Loading existing database...")
    db = load_database()
    
    print(f"Current database stats:")
    print(f"  PRs: {len(db['prs'])}")
    print(f"  Repos: {len(db['repos'])}")
    print(f"  Last update: {db['last_update'] or 'Never'}")
    
    # Fetch new data
    new_prs, new_repos = fetch_new_data(db['last_update'])
    
    print(f"Fetched from GitHub:")
    print(f"  PRs: {len(new_prs)}")
    print(f"  Repos: {len(new_repos)}")
    
    # Merge data
    print("Merging data...")
    db['prs'] = merge_prs(db['prs'], new_prs)
    db['repos'] = merge_repos(db['repos'], new_repos)
    
    # Save updated database
    print("Saving database...")
    save_database(db)
    
    print("✅ Database updated successfully!")
    print(f"Final stats:")
    print(f"  Total PRs: {len(db['prs'])}")
    print(f"  Total Repos: {len(db['repos'])}")
    
    return db

if __name__ == "__main__":
    update_database()
