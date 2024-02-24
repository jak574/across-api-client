from authlib.integrations.httpx_client import OAuth2Client  # type: ignore

from ..base.schema import AuthToken


TOKEN_ENDPOINT = "https://auth.gcn.nasa.gov/oauth2/token"


def get_credential(client_id: str, client_secret: str) -> AuthToken:
    session = OAuth2Client(client_id, client_secret, scope={})
    token = session.fetch_token(TOKEN_ENDPOINT)
    return AuthToken(**token)
