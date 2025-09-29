import requests
import json

def get_user_repos_with_commits(user_id):
  
    # Input validation - fix the validation logic
    if not user_id or not isinstance(user_id, str) or user_id.strip() == "":
        raise ValueError("User ID must be a non-empty string")
    
    # Strip whitespace from user_id
    user_id = user_id.strip()
    
    try:
        # Get user repositories
        repos_url = f"https://api.github.com/users/{user_id}/repos"
        repos_response = requests.get(repos_url)
        
        # Check for HTTP errors
        if repos_response.status_code == 404:
            raise requests.exceptions.RequestException(f"User '{user_id}' not found: 404 Client Error")
        elif repos_response.status_code == 403:
            raise requests.exceptions.RequestException(f"API rate limit exceeded: 403 Forbidden")
        
        repos_response.raise_for_status()
        
        try:
            repositories = repos_response.json()
        except ValueError as e:
            raise requests.exceptions.RequestException(f"Invalid JSON response: {str(e)}")
        
        result = []
        total_commits = 0
        
        for repo in repositories:
            repo_name = repo['name']
            
            # Get commit count for each repository
            commits_url = f"https://api.github.com/repos/{user_id}/{repo_name}/commits"
            try:
                commits_response = requests.get(commits_url)
                
                if commits_response.status_code == 200:
                    commits = commits_response.json()
                    commit_count = len(commits)
                else:
                    # Handle cases where commits are not accessible (private repos, etc.)
                    commit_count = 0
                    
            except requests.exceptions.RequestException:
                # If commits API fails, default to 0
                commit_count = 0
            
            result.append({
                'repo_name': repo_name,
                'commit_count': commit_count
            })
            
            total_commits += commit_count

            # Display output as required
            print(f"Repo: {repo_name} | Number of commits: {commit_count}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"    Total repositories: {len(result)}")
        print(f"    Total commits: {total_commits}")
        print(f"    Successfully analyzed all repositories")
        return result
        
    except requests.exceptions.RequestException as e:
        # Re-raise with more specific message if not already formatted
        if "GitHub API request failed" not in str(e):
            raise requests.exceptions.RequestException(f"Failed to fetch repositories for user {user_id}: {str(e)}")
        else:
            raise e

if __name__ == "__main__":
    # Example usage
    try:
        user = "vanshajtyagi"
        user_repos = get_user_repos_with_commits(user)
        print(f'Fetched Repositories from Github for user: {user}')
        print(f"Successfully retrieved {len(user_repos)} repositories")
    except Exception as e:
        print(f"Error: {str(e)}")
