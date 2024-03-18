from authlib.integrations.httpx_client import OAuth2Client  # type: ignore

from ..base.schema import AuthToken

TOKEN_ENDPOINT = "https://auth.dev.gcn.nasa.gov/oauth2/token"


class Authentication:
    """
    Class to handle authentication for the ACROSS API. This authenticates using
    client_id and client_secret that are obtained from NASA's General
    Coordinates Network (https://gcn.nasa.gov). Note that these have to have
    the correct scopes to access the ACROSS API.

    Note that the access token is automatically refreshed when it is expired as
    long as the `access_token` property is used to access the token.

    Parameters
    ----------
    client_id : str
        The client ID for the API.
    client_secret : str
        The client secret for the API.

    Attributes
    ----------
    auth_token : AuthToken
        The refresh token for the API.

    Properties
    ----------
    access_token : str
        The refresh token for the API. This will automatically refresh the token if it is expired.

    """

    auth_token: AuthToken

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token = self.get_credential(client_id, client_secret)

    @property
    def access_token(self) -> str:
        """Property to get the refresh token. This will automatically refresh the token if it is expired."""
        if self.auth_token.is_expired:
            self.auth_token = self.get_credential(self.client_id, self.client_secret)
        return self.auth_token.access_token

    @classmethod
    def get_credential(cls, client_id: str, client_secret: str) -> AuthToken:
        """Get the refresh token for the API."""
        session = OAuth2Client(client_id, client_secret, scope={})
        token = session.fetch_token(TOKEN_ENDPOINT)
        return AuthToken(**token)


def get_credential(client_id: str, client_secret: str) -> AuthToken:
    return Authentication.get_credential(client_id, client_secret)
