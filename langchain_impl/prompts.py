import yaml
from typing import Any


class YAMLExtractionError(Exception):
    """Custom exception for YAML loading and parsing errors."""
    pass

class YAMLData:
    """Recursive data structure converter for nested YAML content."""
    def __init__(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, YAMLData(value))
            else:
                setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)

class YAMLExtractor:
    """Secure YAML data extractor with Pythonic attribute access."""
    
    def __init__(self, file_path: str):
        """
        Initialize YAML extractor with file path.
        
        Args:
            file_path: Path to YAML file
            
        Raises:
            YAMLExtractionError: For file/YAML syntax issues
        """
        try:
            with open(file_path, 'r') as f:
                raw_data = yaml.safe_load(f)
                self._data = YAMLData(raw_data)
        except FileNotFoundError as e:
            raise YAMLExtractionError(f"File not found: {file_path}") from e
        except yaml.YAMLError as e:
            raise YAMLExtractionError(f"YAML syntax error: {e}") from e

    @property
    def data(self) -> YAMLData:
        """Main access point for parsed YAML data structure"""
        return self._data

    def get_nested(self, dot_path: str, default: Any = None) -> Any:
        """
        Safe nested attribute access using dot notation
        
        Args:
            dot_path: Nested path (e.g. 'vulnscan_agent.system_prompt')
            default: Return value if path not found
            
        Returns:
            Value at path or default
        """
        current = self._data
        print(current)
        for key in dot_path.split('.'):
            current = getattr(current, key, None)
            if current is None:
                return default
        return current or default
    
class Prompts():

    def __init__(self):
        self.yaml_extractor = YAMLExtractor(file_path='config/prompts.yaml')

    @property
    def get(self):
        return self.yaml_extractor.data

if __name__ == '__main__':
    prompts = Prompts()
    print_prompt = prompts.get.vulnscan_agent
    print(print_prompt)