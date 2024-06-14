from connectors.secret_manager_connection import SecretManagerConnector
from connectors.open_ai_connector import OpenaiConnector
from connectors.big_query_connector import BigQueryConnector

from connectors.credentials import SERVICE_ACCOUNT_JSON
from connectors.credentials import OPEN_AI_MODEL
from connectors.credentials import PROJECT_ID


class ConnectionManager:

    def __init__(self, service_account_json=SERVICE_ACCOUNT_JSON, model: str = OPEN_AI_MODEL, project_id = PROJECT_ID):
        self.secret_manager_connector = SecretManagerConnector(json_key=service_account_json, project_id=project_id)
        self.bigquery_connection = BigQueryConnector(json_key=service_account_json, project_id=project_id)
        self.openai_key = self.secret_manager_connector.get_secret('openai_api_key')
        self.open_ai_connection = OpenaiConnector(api_key=self.openai_key, model=model)
