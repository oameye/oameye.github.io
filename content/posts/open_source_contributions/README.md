# GitHub Contributions Tracker

This project automatically tracks and generates a comprehensive list of GitHub contributions, solving the GitHub CLI 1000-result limit by maintaining a persistent database.

## 🚀 Quick Start

To update your contributions and generate the markdown file:

```bash
python3 update_contributions.py
```

This single command will:
1. Update the local database with new GitHub data
2. Generate the `contributions.md` file with all your contributions

## � Project Structure

- `update_contributions.py` - Main script that runs the full workflow
- `update_database.py` - Updates the persistent database with new GitHub data
- `generate_contributions.py` - Generates markdown from the database
- `database/` - Persistent storage for all contribution data
  - `prs.json` - All pull requests
  - `repos.json` - All repositories
  - `metadata.json` - Database metadata and statistics
- `contributions.md` - Generated markdown file with all contributions

## 🔧 Individual Commands

### Update Database Only
```bash
python3 update_database.py
```

### Generate Markdown Only (from existing database)
```bash
python3 generate_contributions.py
```

## 🎯 Features

- **No Data Loss**: Maintains complete history of contributions beyond GitHub's 1000 limit
- **Incremental Updates**: Only fetches new data, preserving historical records
- **Smart Categorization**: Automatically categorizes your repositories
- **Filtered Views**: Shows only meaningful external contributions
- **Automatic Summarization**: Summarizes major projects you maintain
- **Professional Formatting**: Clean, readable markdown output

## 📊 What Gets Tracked

- ✅ All merged pull requests to external repositories
- ✅ Your open source projects (categorized by type)
- ✅ Repository statistics (stars, creation dates)
- ❌ Forks (excluded for cleaner presentation)
- ❌ PRs to your own repositories (excluded)
- ❌ Unmerged PRs (excluded for professional presentation)

## � Regular Usage

Run the main script periodically to keep your contributions up to date:

```bash
# Daily/weekly update
python3 update_contributions.py
```

The system intelligently merges new data with existing records, ensuring no contributions are lost.

---

*This represents a complete system for tracking and showcasing your open source contributions.*
