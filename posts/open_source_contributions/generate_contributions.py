#!/usr/bin/env python3
"""
Generate a markdown list of GitHub contributions for oameye
Uses the persistent database created by update_database.py
"""

import json
import os
from datetime import datetime
from collections import defaultdict

def load_database():
    """Load the contributions database"""
    db = {
        'prs': [],
        'repos': []
    }
    
    if not os.path.exists('database/prs.json') or not os.path.exists('database/repos.json'):
        print("❌ Database not found! Please run 'python3 update_database.py' first.")
        return None
    
    with open('database/prs.json', 'r') as f:
        db['prs'] = json.load(f)
    
    with open('database/repos.json', 'r') as f:
        db['repos'] = json.load(f)
    
    print(f"📊 Loaded database: {len(db['prs'])} PRs, {len(db['repos'])} repos")
    return db

def categorize_repositories(repos):
    """Categorize repositories by project type"""
    categories = {
        'Julia Packages': [],
        'Research Projects': [],
        'Tools & Utilities': [],
        'Documentation & Tutorials': [],
        'Personal Projects': []
    }
    
    for repo in repos:
        if repo.get('isPrivate', False) or repo.get('isFork', False):
            continue  # Skip private repos and forks
            
        name = repo['name']
        description = repo.get('description', '')
        
        # Categorize based on name and description
        if name.endswith('.jl'):
            categories['Julia Packages'].append(repo)
        elif any(keyword in name.lower() or keyword in description.lower() 
                for keyword in ['tutorial', 'docs', 'documentation', 'guide']):
            categories['Documentation & Tutorials'].append(repo)
        elif any(keyword in name.lower() or keyword in description.lower() 
                for keyword in ['research', 'paper', 'parametron', 'quantum', 'oscillator', 'hopf']):
            categories['Research Projects'].append(repo)
        elif any(keyword in name.lower() or keyword in description.lower() 
                for keyword in ['tool', 'utility', 'engine', 'zotero', 'homebrew']):
            categories['Tools & Utilities'].append(repo)
        elif 'github.io' in name or 'website' in name or 'hugo' in name:
            categories['Personal Projects'].append(repo)
        # Skip other repositories (previously in "Forks & Contributions")
    
    return categories

def generate_markdown():
    """Generate the complete markdown document"""
    
    print("Loading data from database...")
    
    # Load data from database
    db = load_database()
    if db is None:
        return None
    
    # Use database data
    all_prs = db['prs']
    repos = db['repos']
    
    # Filter out forks
    repos = [repo for repo in repos if not repo.get('isFork', False)]
    
    # Filter out PRs to oameye repositories and only keep merged PRs
    external_closed_prs = [pr for pr in all_prs if not pr.get('repository', {}).get('nameWithOwner', '').startswith('oameye/') and pr.get('state') == 'merged']
    
    # Sort PRs by creation date (most recent first)
    external_closed_prs.sort(key=lambda x: x.get('createdAt', ''), reverse=True)

    # Start building markdown
    md = []
    md.append("# Open Source Contributions")
    md.append("")
    md.append("> **Note**: This document is automatically generated using the GitHub CLI and updated regularly to reflect the latest contributions.")
    md.append("")
    md.append(f"*Generated on {datetime.now().strftime('%B %d, %Y')}*")
    md.append("")
    
    # Recent merged contributions (external repositories only)
    md.append("## 🔥 Recent Merged Contributions (External Repositories)")
    md.append("")
    
    # Use already filtered external merged PRs
    external_merged_prs = external_closed_prs[:10]  # Take top 10 recent
    
    for pr in external_merged_prs:
        repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
        title = pr.get('title', 'No title')
        url = pr.get('url', '#')
        created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
        
        md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
    
    md.append("")
    
    # My repositories by category
    md.append("## 🚀 My Open Source Projects")
    md.append("")
    
    categorized_repos = categorize_repositories(repos)
    
    for category, category_repos in categorized_repos.items():
        if not category_repos:
            continue
            
        md.append(f"### {category}")
        md.append("")
        
        # Sort by stars, then by creation date
        category_repos.sort(key=lambda x: (x.get('stargazerCount', 0), x.get('createdAt', '')), reverse=True)
        
        for repo in category_repos:
            name = repo['name']
            description = repo.get('description', 'No description')
            url = repo['url']
            stars = repo.get('stargazerCount', 0)
            created_date = datetime.fromisoformat(repo.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
            
            star_badge = f"⭐ {stars}" if stars > 0 else ""
            
            md.append(f"- **[{name}]({url})** {star_badge}")
            if description and description != "":
                md.append(f"  - {description}")
            md.append(f"  - *Created: {created_date}*")
            md.append("")
            md.append("#")
            md.append("")
    
    # All merged pull requests by organization (excluding own repositories)
    md.append("## 📝 All Merged Pull Requests by Organization (External Repositories)")
    md.append("")
    
    # Group PRs by organization (excluding oameye, only merged PRs)
    org_prs = defaultdict(list)
    all_external_prs = external_closed_prs  # Only merged PRs now
    
    for pr in all_external_prs:
        repo_full_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
        org_name = repo_full_name.split('/')[0] if '/' in repo_full_name else 'Unknown'
        if org_name != 'oameye':  # Extra safety check
            org_prs[org_name].append(pr)
    
    # Sort organizations by number of PRs
    for org, prs in sorted(org_prs.items(), key=lambda x: len(x[1]), reverse=True):
        md.append(f"### {org} ({len(prs)} PRs)")
        md.append("")
        
        if org == "QuantumEngineeredSystems":
            # Summarize QuantumEngineeredSystems contributions instead of listing all
            merged_count = len(prs)  # All are merged by definition now
            
            # Group by repository
            repo_counts = defaultdict(int)
            for pr in prs:
                repo_name = pr.get('repository', {}).get('name', 'Unknown')
                repo_counts[repo_name] += 1
            
            md.append(f"*As main maintainer of QuantumEngineeredSystems packages:*")
            md.append(f"- **{merged_count}** merged PRs")
            md.append(f"- Active development across **{len(repo_counts)}** repositories:")
            
            # Show repository breakdown
            for repo, count in sorted(repo_counts.items(), key=lambda x: x[1], reverse=True):
                md.append(f"  - **{repo}**: {count} PRs")
            
            md.append("")
            md.append("*Recent contributions (last 5):*")
            
            # Show only the 5 most recent PRs
            recent_prs = sorted(prs, key=lambda x: x.get('createdAt', ''), reverse=True)[:5]
            for pr in recent_prs:
                repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
                title = pr.get('title', 'No title')
                url = pr.get('url', '#')
                created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
                
                md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
        elif org == "JuliaDynamics":
            # Only summarize CriticalTransitions.jl, show other repos individually
            merged_count = len(prs)
            
            # Group by repository
            repo_counts = defaultdict(int)
            critical_transitions_prs = []
            other_prs = []
            
            for pr in prs:
                repo_name = pr.get('repository', {}).get('name', 'Unknown')
                repo_counts[repo_name] += 1
                if repo_name == 'CriticalTransitions.jl':
                    critical_transitions_prs.append(pr)
                else:
                    other_prs.append(pr)
            
            # Summarize CriticalTransitions.jl
            if critical_transitions_prs:
                md.append(f"**CriticalTransitions.jl** ({len(critical_transitions_prs)} PRs) - *Co-creator and main contributor*")
                md.append("")
                md.append("*Recent CriticalTransitions.jl contributions (last 3):*")
                
                recent_ct_prs = sorted(critical_transitions_prs, key=lambda x: x.get('createdAt', ''), reverse=True)[:3]
                for pr in recent_ct_prs:
                    repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
                    title = pr.get('title', 'No title')
                    url = pr.get('url', '#')
                    created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
                md.append("")
            
            # Show other repositories individually
            if other_prs:
                md.append("**Other JuliaDynamics contributions:**")
                md.append("")
                
                # Sort other PRs by creation date (most recent first)
                other_prs.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
                
                for pr in other_prs:
                    repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
                    title = pr.get('title', 'No title')
                    url = pr.get('url', '#')
                    created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    
                    md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
        elif org == "qojulia":
            # Only summarize SecondQuantizedAlgebra.jl, show other repos individually
            merged_count = len(prs)
            
            # Group by repository
            repo_counts = defaultdict(int)
            second_quantized_prs = []
            other_prs = []
            
            for pr in prs:
                repo_name = pr.get('repository', {}).get('name', 'Unknown')
                repo_counts[repo_name] += 1
                if repo_name == 'SecondQuantizedAlgebra.jl':
                    second_quantized_prs.append(pr)
                else:
                    other_prs.append(pr)
            
            # Summarize SecondQuantizedAlgebra.jl
            if second_quantized_prs:
                md.append(f"**SecondQuantizedAlgebra.jl** ({len(second_quantized_prs)} PRs) - *Major contributor and maintainer*")
                md.append("")
                md.append("*Recent SecondQuantizedAlgebra.jl contributions (last 3):*")
                
                recent_sq_prs = sorted(second_quantized_prs, key=lambda x: x.get('createdAt', ''), reverse=True)[:3]
                for pr in recent_sq_prs:
                    repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
                    title = pr.get('title', 'No title')
                    url = pr.get('url', '#')
                    created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
                md.append("")
            
            # Show other repositories individually
            if other_prs:
                md.append("**Other qojulia contributions:**")
                md.append("")
                
                # Sort other PRs by creation date (most recent first)
                other_prs.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
                
                for pr in other_prs:
                    repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
                    title = pr.get('title', 'No title')
                    url = pr.get('url', '#')
                    created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    
                    md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
        else:
            # Sort PRs by creation date (most recent first)
            prs.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
            
            for pr in prs:
                repo_name = pr.get('repository', {}).get('nameWithOwner', 'Unknown')
                title = pr.get('title', 'No title')
                url = pr.get('url', '#')
                created_date = datetime.fromisoformat(pr.get('createdAt', '').replace('Z', '+00:00')).strftime('%Y-%m-%d')
                
                md.append(f"- **[{repo_name}]({url})** - {title} *(merged {created_date})*")
        
        md.append("")
    
    # Footer
    md.append("---")
    md.append("")
    md.append("*This document was automatically generated using the GitHub CLI.*")
    
    return '\n'.join(md)

if __name__ == "__main__":
    markdown_content = generate_markdown()
    
    if markdown_content is None:
        print("❌ Failed to generate markdown. Please update the database first.")
        exit(1)
    
    # Write to file
    with open('contributions.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("✅ Generated contributions.md successfully!")
    print(f"📄 File size: {len(markdown_content)} characters")
