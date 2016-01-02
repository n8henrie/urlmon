from urlmon.urlmon import Pushover
import keyring


def test_pushover():
    """Test pushover credentials"""

    api_token = keyring.get_password('pushover', 'api_token')
    pushover_user = keyring.get_password('pushover', 'user')
    pushover = Pushover(api_token, pushover_user)

    response = pushover.validate()
    assert response.status_code == 200
    assert response.json().get("status") == 1
