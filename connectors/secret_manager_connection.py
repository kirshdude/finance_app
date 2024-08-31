import json
from google.cloud import secretmanager
from google.oauth2 import service_account


class SecretManagerConnector:

    def __init__(self, json_key: str = None, project_id : str = None) -> None:
        if json_key is not None:
            credentials = json.loads(json_key, strict=False)
            self.credentials = service_account.Credentials.from_service_account_info(credentials)
        else:
            self.credentials = None
        self.client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        self.project_id = project_id

    def get_secret(self, secret_key_name: str):
        secret_name = f"projects/{self.project_id}/secrets/{secret_key_name}/versions/latest"
        response = self.client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode("UTF-8")
