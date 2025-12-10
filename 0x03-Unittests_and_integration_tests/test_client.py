#!/usr/bin/env python3,,,,,,,,,,
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient  # Adjust import if your file structure is different
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests # type: ignore


# -------------------------
# Unit Tests
# -------------------------
class TestGithubOrgClient(unittest.TestCase):

    # 1. Test org property with parameterized inputs and patch
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"login": org_name})

    # 2. Test _public_repos_url property
    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")

    # 3. Test public_repos method
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "fake_url"
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("fake_url")

    # 4. Test has_license method with parameterized input
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


# -------------------------
# Integration Tests
# -------------------------
@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup patching for requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        # Use side_effect to return different payloads depending on URL
        def side_effect(url, *args, **kwargs):
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data

                def json(self):
                    return self._json_data
            if "orgs" in url:
                return MockResponse(cls.org_payload)
            return MockResponse(cls.repos_payload)
        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    # Test public_repos returns correct repos list
    def test_public_repos(self):
        client = GithubOrgClient("org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    # Test public_repos with license filtering
    def test_public_repos_with_license(self):
        client = GithubOrgClient("org")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
