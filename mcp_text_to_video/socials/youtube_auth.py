from apiclient.discovery import build
from oauth2client.file import Storage

import httplib2
import base64
import os

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

OAUTH2_FILE = "oauth2.json"


def get_authenticated_service():
    with open(OAUTH2_FILE, "w") as f:
        f.write(base64.b64decode(os.getenv("OAUTH2_BASE64")).decode("utf-8"))

    try:
        storage = Storage(OAUTH2_FILE)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            raise Exception(
                "Invalid OAuth2 credentials in OAUTH2_BASE64. Please re-authenticate with youtube_auth."
            )

        return build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()),
        )
    except Exception as e:
        raise e
    finally:
        # Delete files
        os.remove(OAUTH2_FILE)
