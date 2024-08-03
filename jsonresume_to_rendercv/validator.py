import requests
import jsonschema
from jsonschema import validate


class SchemaValidator:
    def __init__(self, schema_url):
        self.schema = self.fetch_schema(schema_url)

    @staticmethod
    def fetch_schema(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def validate_json(self, data):
        try:
            validate(instance=data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as err:
            print(f"Validation error: {err.message}")
            raise

    def validate_yaml(self, data):
        self.validate_json(data)
