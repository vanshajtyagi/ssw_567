"""
Comprehensive test suite for GitHub API Repository Analyzer.

This module contains unit tests for the github_api module using mocking
to ensure tests are independent of external GitHub API calls.
"""
import pytest
import requests
from unittest.mock import Mock, patch
from github_api import get_user_repos_with_commits

class TestGitHubAPI:
    """Test class for GitHub API functionality"""

    def test_valid_user_with_multiple_repos(self):
        """Test successful API call with valid user having multiple repositories"""
        with patch('requests.get') as mock_get:
            # Mock repositories response
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = [
                {'name': 'repo1'},
                {'name': 'repo2'},
                {'name': 'repo3'}
            ]
            mock_repos_response.raise_for_status.return_value = None
            
            # Mock commits responses - different commit counts for each repo
            mock_commits_response1 = Mock()
            mock_commits_response1.status_code = 200
            mock_commits_response1.json.return_value = [
                {'sha': 'commit1'}, {'sha': 'commit2'}, {'sha': 'commit3'}
            ]
            
            mock_commits_response2 = Mock()
            mock_commits_response2.status_code = 200
            mock_commits_response2.json.return_value = [
                {'sha': 'commit1'}, {'sha': 'commit2'}
            ]
            
            mock_commits_response3 = Mock()
            mock_commits_response3.status_code = 200
            mock_commits_response3.json.return_value = [
                {'sha': 'commit1'}
            ]
            
            mock_get.side_effect = [
                mock_repos_response, 
                mock_commits_response1, 
                mock_commits_response2, 
                mock_commits_response3
            ]
            
            result = get_user_repos_with_commits("testuser")
            
            assert len(result) == 3
            assert result[0]['repo_name'] == 'repo1'
            assert result[0]['commit_count'] == 3
            assert result[1]['repo_name'] == 'repo2'
            assert result[1]['commit_count'] == 2
            assert result[2]['repo_name'] == 'repo3'
            assert result[2]['commit_count'] == 1

    def test_valid_user_single_repo(self):
        """Test successful API call with valid user having single repository"""
        with patch('requests.get') as mock_get:
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = [{'name': 'single-repo'}]
            mock_repos_response.raise_for_status.return_value = None
            
            mock_commits_response = Mock()
            mock_commits_response.status_code = 200
            mock_commits_response.json.return_value = [
                {'sha': 'commit1'}, {'sha': 'commit2'}, {'sha': 'commit3'}, 
                {'sha': 'commit4'}, {'sha': 'commit5'}
            ]
            
            mock_get.side_effect = [mock_repos_response, mock_commits_response]
            
            result = get_user_repos_with_commits("singlerepouser")
            
            assert len(result) == 1
            assert result[0]['repo_name'] == 'single-repo'
            assert result[0]['commit_count'] == 5

    def test_valid_user_no_repos(self):
        """Test user with no repositories"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = get_user_repos_with_commits("emptyuser")
            
            assert result == []
            assert len(result) == 0

    def test_valid_user_repos_with_zero_commits(self):
        """Test repositories with zero commits"""
        with patch('requests.get') as mock_get:
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = [
                {'name': 'empty-repo1'},
                {'name': 'empty-repo2'}
            ]
            mock_repos_response.raise_for_status.return_value = None
            
            # Mock empty commits responses
            mock_commits_response = Mock()
            mock_commits_response.status_code = 200
            mock_commits_response.json.return_value = []
            
            mock_get.side_effect = [
                mock_repos_response, 
                mock_commits_response, 
                mock_commits_response
            ]
            
            result = get_user_repos_with_commits("emptycommitsuser")
            
            assert len(result) == 2
            assert result[0]['commit_count'] == 0
            assert result[1]['commit_count'] == 0

    # Fixed input validation tests
    def test_invalid_input_empty_string(self):
        """Test error handling for empty string input"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits("")
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_invalid_input_none(self):
        """Test error handling for None input"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits(None)
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_invalid_input_integer(self):
        """Test error handling for integer input"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits(123)
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_invalid_input_whitespace_only(self):
        """Test error handling for whitespace-only input"""
        with pytest.raises(ValueError) as excinfo:
            get_user_repos_with_commits("   ")
        assert "User ID must be a non-empty string" in str(excinfo.value)

    def test_user_not_found_404(self):
        """Test handling of non-existent user (404 error)"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            with pytest.raises(requests.exceptions.RequestException) as excinfo:
                get_user_repos_with_commits("nonexistentuser")
            assert "User 'nonexistentuser' not found: 404 Client Error" in str(excinfo.value)

    def test_api_rate_limit_403(self):
        """Test handling of API rate limit (403 error)"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 403
            mock_get.return_value = mock_response
            
            with pytest.raises(requests.exceptions.RequestException) as excinfo:
                get_user_repos_with_commits("testuser")
            assert "API rate limit exceeded: 403 Forbidden" in str(excinfo.value)

    def test_network_connection_error(self):
        """Test handling of network connection errors"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network connection failed")
            
            with pytest.raises(requests.exceptions.RequestException) as excinfo:
                get_user_repos_with_commits("testuser")
            assert "Failed to fetch repositories for user testuser" in str(excinfo.value)

    def test_network_timeout_error(self):
        """Test handling of network timeout errors"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
            
            with pytest.raises(requests.exceptions.RequestException) as excinfo:
                get_user_repos_with_commits("testuser")
            assert "Failed to fetch repositories for user testuser" in str(excinfo.value)

    def test_commits_api_failure(self):
        """Test handling when commits API fails but repos API succeeds"""
        with patch('requests.get') as mock_get:
            # Mock successful repos response
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = [
                {'name': 'repo1'},
                {'name': 'repo2'}
            ]
            mock_repos_response.raise_for_status.return_value = None
            
            # Mock failed commits responses
            mock_commits_response = Mock()
            mock_commits_response.status_code = 403  # Forbidden - could be private repo
            
            mock_get.side_effect = [
                mock_repos_response,
                mock_commits_response,
                mock_commits_response
            ]
            
            result = get_user_repos_with_commits("mixedaccessuser")
            
            assert len(result) == 2
            assert result[0]['commit_count'] == 0  # Should default to 0 for inaccessible repos
            assert result[1]['commit_count'] == 0

    def test_malformed_json_response(self):
        """Test handling of malformed JSON responses"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            with pytest.raises(requests.exceptions.RequestException) as excinfo:
                get_user_repos_with_commits("testuser")
            assert "Invalid JSON response" in str(excinfo.value)

    def test_large_repository_count(self):
        """Test user with many repositories"""
        with patch('requests.get') as mock_get:
            # Create mock data for 10 repositories
            repos_data = [{'name': f'repo{i}'} for i in range(10)]
            
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = repos_data
            mock_repos_response.raise_for_status.return_value = None
            
            # Mock commits responses for each repo
            mock_commits_response = Mock()
            mock_commits_response.status_code = 200
            mock_commits_response.json.return_value = [{'sha': 'commit1'}, {'sha': 'commit2'}]
            
            mock_get.side_effect = [mock_repos_response] + [mock_commits_response] * 10
            
            result = get_user_repos_with_commits("prolificuser")
            
            assert len(result) == 10
            for i, repo in enumerate(result):
                assert repo['repo_name'] == f'repo{i}'
                assert repo['commit_count'] == 2

    def test_repo_names_with_special_characters(self):
        """Test repositories with special characters in names"""
        with patch('requests.get') as mock_get:
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = [
                {'name': 'repo-with-dashes'},
                {'name': 'repo_with_underscores'},
                {'name': 'repo.with.dots'},
                {'name': 'REPO-WITH-CAPS'}
            ]
            mock_repos_response.raise_for_status.return_value = None
            
            mock_commits_response = Mock()
            mock_commits_response.status_code = 200
            mock_commits_response.json.return_value = [{'sha': 'commit1'}]
            
            mock_get.side_effect = [mock_repos_response] + [mock_commits_response] * 4
            
            result = get_user_repos_with_commits("specialcharsuser")
            
            assert len(result) == 4
            assert result[0]['repo_name'] == 'repo-with-dashes'
            assert result[1]['repo_name'] == 'repo_with_underscores'
            assert result[2]['repo_name'] == 'repo.with.dots'
            assert result[3]['repo_name'] == 'REPO-WITH-CAPS'

    def test_real_user_structure(self):
        """Test with real GitHub user data structure"""
        with patch('requests.get') as mock_get:
            # Use structure similar to your attached JSON
            mock_repos_response = Mock()
            mock_repos_response.status_code = 200
            mock_repos_response.json.return_value = [
                {
                    'name': 'Airline-Passenger-Satisfaction-Analysis',
                    'id': 901118501,
                    'full_name': 'vanshajtyagi/Airline-Passenger-Satisfaction-Analysis',
                    'private': False
                },
                {
                    'name': 'AWS-tutorials',
                    'id': 322821259,
                    'full_name': 'vanshajtyagi/AWS-tutorials',
                    'private': False
                }
            ]
            mock_repos_response.raise_for_status.return_value = None
            
            # Mock commits responses
            mock_commits_response1 = Mock()
            mock_commits_response1.status_code = 200
            mock_commits_response1.json.return_value = [{'sha': f'commit{i}'} for i in range(5)]
            
            mock_commits_response2 = Mock()
            mock_commits_response2.status_code = 200
            mock_commits_response2.json.return_value = [{'sha': f'commit{i}'} for i in range(3)]
            
            mock_get.side_effect = [
                mock_repos_response,
                mock_commits_response1,
                mock_commits_response2
            ]
            
            result = get_user_repos_with_commits("vanshajtyagi")
            
            assert len(result) == 2
            assert result[0]['repo_name'] == 'Airline-Passenger-Satisfaction-Analysis'
            assert result[0]['commit_count'] == 5
            assert result[1]['repo_name'] == 'AWS-tutorials'
            assert result[1]['commit_count'] == 3
    
    @patch('github_api.requests.get')
    def test_commits_api_non_200_response(self, mock_get):
        """Cover the else branch in commits status check"""
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [{'name': 'test-repo'}]
        mock_repos_response.raise_for_status.return_value = None
        
        mock_commits_response = Mock()
        mock_commits_response.status_code = 404  # Not 200
        
        mock_get.side_effect = [mock_repos_response, mock_commits_response]
        
        result = get_user_repos_with_commits("testuser")
        assert result[0]['commit_count'] == 0

    @patch('github_api.requests.get')
    def test_commits_request_fails(self, mock_get):
        """Cover the except RequestException block in commits"""
        mock_repos_response = Mock()
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [{'name': 'test-repo'}]
        mock_repos_response.raise_for_status.return_value = None
        
        # Second call (commits) raises exception
        mock_get.side_effect = [
            mock_repos_response,
            requests.exceptions.RequestException("Request failed")
        ]
        
        result = get_user_repos_with_commits("testuser")
        assert result[0]['commit_count'] == 0

    @patch('github_api.requests.get')
    def test_exception_already_contains_github_api_message(self, mock_get):
        """Test the else branch in final exception handling"""
        exception_with_message = requests.exceptions.RequestException("GitHub API request failed: test error")
        mock_get.side_effect = exception_with_message
        
        with pytest.raises(requests.exceptions.RequestException) as excinfo:
            get_user_repos_with_commits("testuser")
        
        # Should re-raise the same exception
        assert str(excinfo.value) == "GitHub API request failed: test error"

    def test_main_function_success(self):
        """Test the main function with successful execution"""
        with patch('github_api.get_user_repos_with_commits') as mock_func:
            mock_func.return_value = [{'repo_name': 'test', 'commit_count': 1}]
            
            with patch('builtins.print') as mock_print:
                from github_api import main
                main()
                
                mock_func.assert_called_once_with("vanshajtyagi")
                mock_print.assert_any_call("Successfully retrieved 1 repositories")

    def test_main_function_error(self):
        """Test the main function with error handling"""
        with patch('github_api.get_user_repos_with_commits') as mock_func:
            mock_func.side_effect = ValueError("Test error")
            
            with patch('builtins.print') as mock_print:
                from github_api import main
                main()
                
                mock_print.assert_called_with("Error: Test error")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
