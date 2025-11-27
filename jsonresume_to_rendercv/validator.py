import requests
import jsonschema
from jsonschema import validate


class SchemaValidator:
    def __init__(self, schema_url, schema_name=None):
        self.schema = self.fetch_schema(schema_url)
        self.schema_name = schema_name or "schema"

    @staticmethod
    def fetch_schema(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def validate_json(self, data):
        try:
            validate(instance=data, schema=self.schema)
        except jsonschema.exceptions.ValidationError as err:
            # Build a readable path to the problematic field
            path_parts = [str(p) for p in err.absolute_path]
            field_path = ".".join(path_parts) if path_parts else "(root)"
            
            # Get the invalid value for display
            invalid_value = repr(err.instance)
            if len(invalid_value) > 100:
                invalid_value = invalid_value[:100] + "..."
            
            # Build a detailed error message
            error_msg = f"[{self.schema_name}] Validation error at field '{field_path}': {err.message}"
            error_msg += f"\n  Invalid value: {invalid_value}"
            
            # Show what was expected if available
            if err.schema:
                constraints = []
                if 'minLength' in err.schema:
                    constraints.append(f"minLength: {err.schema['minLength']}")
                if 'maxLength' in err.schema:
                    constraints.append(f"maxLength: {err.schema['maxLength']}")
                if 'format' in err.schema:
                    constraints.append(f"format: {err.schema['format']}")
                if 'type' in err.schema:
                    constraints.append(f"type: {err.schema['type']}")
                if constraints:
                    error_msg += f"\n  Expected constraints: {', '.join(constraints)}"
            
            print(error_msg)
            raise

    def validate_yaml(self, data):
        self.validate_json(data)
