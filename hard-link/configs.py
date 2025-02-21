"""Configuration management for microscope control system"""
from collections import OrderedDict 
import os
from typing import Any, Dict

# Initialize configuration dictionary
config: OrderedDict = OrderedDict()

def abspath(path: str) -> str:
    """
    Convert relative path to absolute path
    
    Args:
        path (str): Input path to convert
        
    Returns:
        str: Absolute path
    """
    return os.path.abspath(path)

def read_env_value(name: str, default: str) -> str:
    """
    Read value from environment variable with fallback to default
    
    Args:
        name (str): Environment variable name
        default (str): Default value if environment variable is not set
        
    Returns:
        str: Value from environment or default
    """
    value = os.environ.get(name, default)
    print(f"Using {name}: {value}")
    return value

# Configuration definitions
MM_DIR: Dict[str, str] = {
    "name": "MM_DIR",
    "default": r"C:\Program Files\Micro-Manager-2.0gamma"
}

MM_CONFIG: Dict[str, str] = {
    "name": "MM_CONFIG",
    "default": "./mmconfigs/Bright_Star.cfg"
}

# Server configuration (referenced in start_server.py)
MM_SERVER: Dict[str, Any] = {
    "port": 18861,
    "hostname": "localhost"
}

# Build configuration dictionary
config["mm_dir"] = abspath(read_env_value(**MM_DIR))
config["mm_config"] = abspath(read_env_value(**MM_CONFIG))
config["mm_server"] = MM_SERVER
