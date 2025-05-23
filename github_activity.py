#!/usr/bin/env python3

import sys
import json
import http.client
import urllib.parse
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()

class GitHubActivity:
    def __init__(self):
        self.api_base = "api.github.com"
        self.user_agent = "GitHub-Activity-CLI/1.0"
        self.default_limit = 10

    def fetch_user_events(self, username, limit=None):
        """Fetch user events from GitHub API."""
        if limit is None:
            limit = self.default_limit

        conn = http.client.HTTPSConnection(self.api_base)
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            path = f"/users/{urllib.parse.quote(username)}/events"
            conn.request("GET", path, headers=headers)
            response = conn.getresponse()
            
            if response.status == 404:
                print(f"{Fore.RED}Error: User '{username}' not found{Style.RESET_ALL}")
                sys.exit(1)
            elif response.status == 403:
                print(f"{Fore.RED}Error: API rate limit exceeded{Style.RESET_ALL}")
                sys.exit(1)
            elif response.status == 429:
                print(f"{Fore.RED}Error: Too many requests. Please try again later{Style.RESET_ALL}")
                sys.exit(1)
            elif response.status != 200:
                print(f"{Fore.RED}Error: Unexpected API response (Status {response.status}){Style.RESET_ALL}")
                sys.exit(1)

            data = json.loads(response.read().decode())
            return data[:limit]

        except http.client.HTTPException as e:
            print(f"{Fore.RED}Error: HTTP request failed - {str(e)}{Style.RESET_ALL}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Invalid JSON response from API{Style.RESET_ALL}")
            sys.exit(1)
        finally:
            conn.close()

    def format_event(self, event):
        """Format a single event into a human-readable message."""
        event_type = event.get("type")
        repo = event.get("repo", {}).get("name", "unknown")
        
        if event_type == "PushEvent":
            commits = len(event.get("payload", {}).get("commits", []))
            return f"Pushed {commits} commits to {repo}"
        
        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type", "repository")
            return f"Created {ref_type} in {repo}"
        
        elif event_type == "IssueEvent":
            action = event.get("payload", {}).get("action", "opened")
            title = event.get("payload", {}).get("issue", {}).get("title", "untitled")
            return f"{action.capitalize()} issue '{title}' in {repo}"
        
        elif event_type == "WatchEvent":
            return f"Starred {repo}"
        
        elif event_type == "ForkEvent":
            return f"Forked {repo}"
        
        else:
            return f"Performed {event_type} in {repo}"

    def display_activity(self, username, limit=None):
        """Display user's GitHub activity."""
        events = self.fetch_user_events(username, limit)
        
        if not events:
            print(f"{Fore.YELLOW}No recent activity found for {username}{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}✓ Fetched {len(events)} events for {username}:{Style.RESET_ALL}")
        for event in events:
            print(f"- {self.format_event(event)}")

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Error: Please provide a GitHub username{Style.RESET_ALL}")
        print("Usage: python github_activity.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    github = GitHubActivity()
    github.display_activity(username)

if __name__ == "__main__":
    main() 