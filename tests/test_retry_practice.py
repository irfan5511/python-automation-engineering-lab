from unittest.mock import patch, call
from retry_practice import get_with_retry
import requests
import pytest


def test_successful_request_returns_immediately():
    with patch("retry_practice.requests.get") as mock_get:
        mock_response = mock_get.return_value

        result = get_with_retry("http://example.com")


        assert result is mock_response


        mock_get.assert_called_once_with(
            "http://example.com",
            headers= None,
            params = None,
            timeout= 10
        )

def test_timeout_then_success():
    with patch("retry_practice.requests.get") as mock_get:
        with patch("retry_practice.time.sleep") as mock_sleep:
            mock_response = mock_get.return_value
            mock_get.side_effect = [requests.Timeout, mock_response]

            result = get_with_retry("http://example.com")

            assert result is mock_response

            assert mock_get.call_count == 2

            mock_sleep.assert_called_once_with(1)


def test_two_timeouts_then_success():
    with patch("retry_practice.requests.get") as mock_get:
        with patch("retry_practice.time.sleep") as mock_sleep:
            mock_response = mock_get.return_value

            mock_get.side_effect = [
                requests.Timeout,
                requests.Timeout,
                mock_response
            ]

            result = get_with_retry("http://example.com")

            assert result is mock_response

            assert mock_get.call_count == 3

            mock_sleep.assert_has_calls(
                [call(1), call(2)]
            )

            assert mock_sleep.call_count == 2


def test_all_attempts_timeout():
    with patch("retry_practice.requests.get") as mock_get:
        with patch("retry_practice.time.sleep") as mock_sleep:
            mock_get.side_effect = requests.Timeout

            with pytest.raises(requests.Timeout):
                get_with_retry("http://example.com")

            assert mock_get.call_count == 3

            mock_sleep.assert_has_calls(
                [call(1), call(2)]
            )

            assert mock_sleep.call_count == 2


def test_http_404_does_not_retry():
    with patch("retry_practice.requests.get") as mock_get:
        with patch("retry_practice.time.sleep") as mock_sleep:
            mock_response = mock_get.return_value
            mock_response.status_code = 404

            http_error = requests.HTTPError(response = mock_response)

            mock_response.raise_for_status.side_effect = http_error

            with pytest.raises(requests.HTTPError):
                get_with_retry("http://example.com")

            assert mock_get.call_count == 1

            mock_sleep.assert_not_called()
            

