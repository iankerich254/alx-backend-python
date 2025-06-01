#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org"""
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"payload": True})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test/repos")

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        mock_repos_url.return_value = "https://api.github.com/orgs/test/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            MockResponse(cls.org_payload),
            MockResponse(cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos integration"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


class MockResponse:
    """Mock response for requests.get().json()"""

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload
