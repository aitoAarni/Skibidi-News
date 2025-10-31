from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import httplib2
import base64
import sys
import os

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

CLIENT_SECRETS_FILE = "client_secrets.json"
OAUTH2_FILE = "oauth2.json"


def create_auth():
    with open(CLIENT_SECRETS_FILE, "w") as f:
        f.write(base64.b64decode(os.getenv("CLIENT_SECRETS_BASE64")).decode("utf-8"))

    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message="WARNING: Please configure OAuth 2.0 in client_secrets.json",
    )

    storage = Storage(OAUTH2_FILE)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)


if __name__ == "__main__":
    create_auth()
    with open(OAUTH2_FILE, "r") as f:
        oauth2 = f.read()

    # base64 encode the oauth2 and client_secrets
    encoded_oauth2 = base64.b64encode(oauth2.encode("utf-8")).decode("utf-8")
    print("\n")
    print(f'OAUTH2_BASE64="{encoded_oauth2}"')

    # Delete files
    os.remove(CLIENT_SECRETS_FILE)
    os.remove(OAUTH2_FILE)
