from authlib.integrations.httpx_client import OAuth2Client  # type: ignore

from ..base.schema import AuthToken

TOKEN_ENDPOINT = "https://auth.dev.gcn.nasa.gov/oauth2/token"


class Authentication:
    auth_token: AuthToken

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token = self.get_credential(client_id, client_secret)

    @property
    def access_token(self) -> str:
        if self.auth_token.is_expired:
            self.auth_token = self.get_credential(self.client_id, self.client_secret)
        return self.auth_token.access_token

    @classmethod
    def get_credential(cls, client_id: str, client_secret: str) -> AuthToken:
        session = OAuth2Client(client_id, client_secret, scope={})
        token = session.fetch_token(TOKEN_ENDPOINT)
        return AuthToken(**token)


def get_credential(client_id: str, client_secret: str) -> AuthToken:
    return Authentication.get_credential(client_id, client_secret)
