#!/usr/bin/env python3

"""unittest for client.githuborgclient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient

class TestGithunOrgClient(unittest.TestCase):
    """test for ithuborgclient.org property"""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])

    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """test that githuborgclient.org returns expected value"""
        mock_payload = {"org": org_name}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org 

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, mock_payload)