# GitHub Activity CLI

A simple command-line tool to view a GitHub user's recent activity. This tool fetches and displays the most recent events from a GitHub user's activity feed.


Sample solution for the [github-user-activity](https://roadmap.sh/projects/github-user-activity) challenge from [roadmap.sh](https://roadmap.sh/).

## Features

- View recent GitHub activity for any user
- Colorized output for better readability
- Comprehensive error handling
- No external HTTP libraries required
- Supports various event types (pushes, issues, stars, etc.)

## Requirements

- Python 3.6 or higher
- colorama (for Windows compatibility)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/github-user-activity.git
cd github-user-activity
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python github_activity.py <username>
```

Example:
```bash
python github_activity.py kamranahmedse
```

### Example Output
```
✓ Fetched 5 events for kamranahmedse:
- Pushed 3 commits to kamranahmedse/developer-roadmap
- Opened issue "Update 2024 roadmap" in kamranahmedse/notes
- Starred freeCodeCamp/freeCodeCamp
- Created repository kamranahmedse/todo-cli
- Forked axios/axios to kamranahmedse/axios-fork
```

## Error Handling

The tool handles various error cases:
- Invalid usernames
- API rate limits
- Network errors
- Invalid API responses

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
