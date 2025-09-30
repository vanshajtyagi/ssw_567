import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from github_api import get_user_repos_with_commits

class TestGitHubAPIMocked:
    """Comprehensive test class using mocked GitHub API calls"""

    @patch('github_api.requests.get')
    def test_valid_user_with_multiple_repos_mocked(self, mock_get):
        """Test successful API call with mocked responses for multiple repositories"""
        # Mock repositories response
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {'name': 'Airline-Passenger-Satisfaction-Analysis'},
            {'name': 'AWS-tutorials'},
            {'name': 'Data-Structures-and-Algorithms'}
        ]
        mock_repos_response.raise_for_status.return_value = None
        
        # Mock commits responses with different commit counts
        mock_commits_response1 = Mock()
        mock_commits_response1.status_code = 200
        mock_commits_response1.json.return_value = [
            {'sha': f'commit{i}', 'message': f'Commit {i}'} for i in range(15)
        ]
        
        mock_commits_response2 = Mock()
        mock_commits_response2.status_code = 200
        mock_commits_response2.json.return_value = [
            {'sha': f'commit{i}', 'message': f'Commit {i}'} for i in range(8)
        ]
        
        mock_commits_response3 = Mock()
        mock_commits_response3.status_code = 200
        mock_commits_response3.json.return_value = [
            {'sha': f'commit{i}', 'message': f'Commit {i}'} for i in range(23)
        ]
        
        # Configure mock to return different responses for each call
        mock_get.side_effect = [
            mock_repos_response,
            mock_commits_response1,
            mock_commits_response2,
            mock_commits_response3
        ]
        
        # Execute the function
        result = get_user_repos_with_commits("vanshajtyagi")
        
        # Verify results
        assert len(result) == 3
        assert result[0]['repo_name'] == 'Airline-Passenger-Satisfaction-Analysis'
        assert result[0]['commit_count'] == 15
        assert result[1]['repo_name'] == 'AWS-tutorials'
        assert result[1]['commit_count'] == 8
        assert result[2]['repo_name'] == 'Data-Structures-and-Algorithms'
        assert result[2]['commit_count'] == 23
        
        # Verify API was called correctly
        assert mock_get.call_count == 4
        assert mock_get.call_args_list[0][0][0] == "https://api.github.com/users/vanshajtyagi/repos"

    @patch('github_api.requests.get')
    def test_valid_user_single_repo_mocked(self, mock_get):
        """Test user with single repository using mocked responses"""
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [{'name': 'single-project'}]
        mock_repos_response.raise_for_status.return_value = None
        
        mock_commits_response = Mock()
        mock_commits_response.status_code = 200
        mock_commits_response.json.return_value = [
            {'sha': f'commit{i}'} for i in range(12)
        ]
        
        mock_get.side_effect = [mock_repos_response, mock_commits_response]
        
        result = get_user_repos_with_commits("testuser")
        
        assert len(result) == 1
        assert result[0]['repo_name'] == 'single-project'
        assert result[0]['commit_count'] == 12

    @patch('github_api.requests.get')
    def test_user_with_no_repos_mocked(self, mock_get):
        """Test user with no repositories using mocked responses"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_user_repos_with_commits("emptyuser")
        
        assert result == []
        assert len(result) == 0

    @patch('github_api.requests.get')
    def test_repos_with_zero_commits_mocked(self, mock_get):
        """Test repositories with zero commits using mocked responses"""
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {'name': 'empty-repo1'},
            {'name': 'empty-repo2'}
        ]
        mock_repos_response.raise_for_status.return_value = None
        
        mock_commits_response = Mock()
        mock_commits_response.status_code = 200
        mock_commits_response.json.return_value = []  # No commits
        
        mock_get.side_effect = [
            mock_repos_response,
            mock_commits_response,
            mock_commits_response
        ]
        
        result = get_user_repos_with_commits("emptycommitsuser")
        
        assert len(result) == 2
        assert result[0]['commit_count'] == 0
        assert result[1]['commit_count'] == 0

    def test_invalid_input_empty_string_mocked(self):
        """Test error handling for empty string input - no mocking needed"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits("")
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_invalid_input_none_mocked(self):
        """Test error handling for None input - no mocking needed"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits(None)
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_invalid_input_integer_mocked(self):
        """Test error handling for integer input - no mocking needed"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits(123)
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_invalid_input_whitespace_only_mocked(self):
        """Test error handling for whitespace-only input - no mocking needed"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits("   ")
        assert "User ID must be a non-empty string" in str(excinfo.value)

    @patch('github_api.requests.get')
    def test_user_not_found_404_mocked(self, mock_get):
        """Test handling of non-existent user using mocked 404 response"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            get_user_repos_with_commits("nonexistentuser")
        assert "User 'nonexistentuser' not found: 404 Client Error" in str(excinfo.value)

    @patch('github_api.requests.get')
    def test_api_rate_limit_403_mocked(self, mock_get):
        """Test handling of API rate limit using mocked 403 response"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            get_user_repos_with_commits("testuser")
        assert "API rate limit exceeded: 403 Forbidden" in str(excinfo.value)

    @patch('github_api.requests.get')
    def test_network_connection_error_mocked(self, mock_get):
        """Test handling of network connection errors using mocked exception"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Mocked network error")
        
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            get_user_repos_with_commits("testuser")
        assert "Failed to fetch repositories for user testuser" in str(excinfo.value)

    @patch('github_api.requests.get')
    def test_network_timeout_error_mocked(self, mock_get):
        """Test handling of network timeout errors using mocked exception"""
        mock_get.side_effect = requests.exceptions.Timeout("Mocked timeout")
        
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            get_user_repos_with_commits("testuser")
        assert "Failed to fetch repositories for user testuser" in str(excinfo.value)

    @patch('github_api.requests.get')
    def test_commits_api_failure_mocked(self, mock_get):
        """Test handling when commits API fails but repos API succeeds"""
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {'name': 'accessible-repo'},
            {'name': 'private-repo'}
        ]
        mock_repos_response.raise_for_status.return_value = None
        
        # First commits call succeeds, second fails (private repo)
        mock_commits_success = Mock()
        mock_commits_success.status_code = 200
        mock_commits_success.json.return_value = [{'sha': 'commit1'}]
        
        mock_commits_fail = Mock()
        mock_commits_fail.status_code = 403  # Forbidden
        
        mock_get.side_effect = [
            mock_repos_response,
            mock_commits_success,
            mock_commits_fail
        ]
        
        result = get_user_repos_with_commits("mixedaccessuser")
        
        assert len(result) == 2
        assert result[0]['commit_count'] == 1  # Accessible repo
        assert result[1]['commit_count'] == 0  # Private repo defaults to 0

    @patch('github_api.requests.get')
    def test_malformed_json_response_mocked(self, mock_get):
        """Test handling of malformed JSON responses using mocked exception"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Mocked JSON decode error")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            get_user_repos_with_commits("testuser")
        assert "Invalid JSON response" in str(excinfo.value)

    @patch('github_api.requests.get')
    def test_large_repository_count_mocked(self, mock_get):
        """Test user with many repositories using mocked responses"""
        # Mock 5 repositories
        repos_data = [{'name': f'project-{i}'} for i in range(1, 6)]
        
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = repos_data
        mock_repos_response.raise_for_status.return_value = None
        
        # Mock commits responses - each repo has different commit counts
        mock_commits_responses = []
        expected_counts = [5, 10, 15, 20, 25]
        
        for count in expected_counts:
            mock_commits = Mock()
            mock_commits.status_code = 200
            mock_commits.json.return_value = [{'sha': f'commit{i}'} for i in range(count)]
            mock_commits_responses.append(mock_commits)
        
        mock_get.side_effect = [mock_repos_response] + mock_commits_responses
        
        result = get_user_repos_with_commits("prolificuser")
        
        assert len(result) == 5
        for i, repo in enumerate(result):
            assert repo['repo_name'] == f'project-{i+1}'
            assert repo['commit_count'] == expected_counts[i]

    @patch('github_api.requests.get')
    def test_special_character_repo_names_mocked(self, mock_get):
        """Test repositories with special characters using mocked responses"""
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {'name': 'repo-with-dashes'},
            {'name': 'repo_with_underscores'},
            {'name': 'repo.with.dots'},
            {'name': 'UPPERCASE-REPO'}
        ]
        mock_repos_response.raise_for_status.return_value = None
        
        mock_commits_response = Mock()
        mock_commits_response.status_code = 200
        mock_commits_response.json.return_value = [{'sha': 'commit1'}, {'sha': 'commit2'}]
        
        mock_get.side_effect = [mock_repos_response] + [mock_commits_response] * 4
        
        result = get_user_repos_with_commits("specialuser")
        
        assert len(result) == 4
        expected_names = ['repo-with-dashes', 'repo_with_underscores', 'repo.with.dots', 'UPPERCASE-REPO']
        for i, repo in enumerate(result):
            assert repo['repo_name'] == expected_names[i]
            assert repo['commit_count'] == 2

    @patch('github_api.requests.get')
    def test_realistic_github_api_response_structure_mocked(self, mock_get):
        """Test with realistic GitHub API response structure using your actual data"""
        # Based on your actual GitHub response from vanshajtyagi
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {
                'id': 901118501,
                'name': 'Airline-Passenger-Satisfaction-Analysis',
                'full_name': 'vanshajtyagi/Airline-Passenger-Satisfaction-Analysis',
                'private': False,
                'owner': {
                    'login': 'vanshajtyagi',
                    'id': 45164555,
                    'type': 'User'
                },
                'description': 'Analysis of airline passenger satisfaction data',
                'created_at': '2024-12-18T10:30:45Z',
                'updated_at': '2024-12-20T15:22:30Z'
            },
            {
                'id': 322821259,
                'name': 'AWS-tutorials',
                'full_name': 'vanshajtyagi/AWS-tutorials',
                'private': False,
                'owner': {
                    'login': 'vanshajtyagi',
                    'id': 45164555,
                    'type': 'User'
                }
            }
        ]
        mock_repos_response.raise_for_status.return_value = None
        
        # Mock realistic commit responses
        mock_commits_response1 = Mock()
        mock_commits_response1.status_code = 200
        mock_commits_response1.json.return_value = [
            {
                'sha': 'abc123def456',
                'commit': {
                    'author': {'name': 'vanshajtyagi', 'email': 'vanshaj@example.com'},
                    'message': 'Initial analysis implementation'
                }
            }
        ] * 15  # 15 commits
        
        mock_commits_response2 = Mock()
        mock_commits_response2.status_code = 200
        mock_commits_response2.json.return_value = [
            {
                'sha': 'def456ghi789',
                'commit': {
                    'author': {'name': 'vanshajtyagi', 'email': 'vanshaj@example.com'},
                    'message': 'AWS tutorial updates'
                }
            }
        ] * 8  # 8 commits
        
        mock_get.side_effect = [
            mock_repos_response,
            mock_commits_response1,
            mock_commits_response2
        ]
        
        result = get_user_repos_with_commits("vanshajtyagi")
        
        assert len(result) == 2
        assert result[0]['repo_name'] == 'Airline-Passenger-Satisfaction-Analysis'
        assert result[0]['commit_count'] == 15
        assert result[1]['repo_name'] == 'AWS-tutorials'
        assert result[1]['commit_count'] == 8

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
