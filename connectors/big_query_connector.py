import os
import json

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd


class BigQueryConnector:
    """
    A class for connecting to and interacting with Google BigQuery.
    """

    def __init__(self, json_key: str = None, project_id: str = None) -> None:
        """
        Initializes the BigQueryConnector.

        Args:
            json_key (str): JSON key as a string containing credentials.
            local_env (bool): Flag indicating whether to use local environment variables for credentials.
        """
        if json_key is not None:
            credentials = json.loads(json_key, strict=False)
            self.credentials = service_account.Credentials.from_service_account_info(credentials)
        else:
            self.credentials = None
        self.client = bigquery.Client(project=project_id, credentials=self.credentials)

    def run_big_query_to_df(self, query: str) -> pd.DataFrame:
        """
        Runs a BigQuery query and returns the result as a Pandas DataFrame.

        Args:
            query (str): BigQuery SQL query.

        Returns:
            pd.DataFrame: Result of the query as a DataFrame.
        """
        return self.client.query(query).to_dataframe()

    def stream_to_big_query(self, table: str, values_dict: dict) -> None:
        """
        Streams data to a BigQuery table.

        Args:
            table: BigQuery table reference.
            values_dict: Dictionary containing values to be inserted.

        Returns:
            None
        """
        errors = self.client.insert_rows_json(table=table, json_rows=[values_dict])
        if errors:
            print("Encountered errors while inserting rows: {}".format(errors))
