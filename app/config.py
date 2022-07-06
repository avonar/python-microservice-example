from pyaml_env import parse_config
from pydantic import BaseSettings, SecretStr, Extra
from tap import Tap
import logging


class CollectorConfig(BaseSettings):
    # All variables MUST have possibility to be overwritten by environment variables
    # example of usage hashicorp vault:
    # from pydantic_vault import vault_config_settings_source
    # DATABASE_URL: str = SecretStr(
    #     ...,
    #     vault_secret_path="secret/data/path/to/secret",
    #     vault_secret_key="DATABASE_URL",
    # )

    DATABASE_URL: SecretStr = SecretStr('')
    CI_COMMIT_SHA: str = "local"
    ENV: str = "local"
    DEBUG: bool = False
    PORT: int = 8000
    LOG_LEVEL: str = "info"

    class Config:
        case_sensitive = True
        extra = Extra.ignore


class ArgumentParser(Tap):
    local_config: bool = False  # use config from local-config.yaml


args = ArgumentParser().parse_args()

yaml_config = parse_config('.app-ci/local-config.yaml') if args.local_config else {}

config = CollectorConfig().parse_obj(yaml_config)

LOG_LEVEL = logging.getLevelName('DEBUG' if config.DEBUG else config.LOG_LEVEL.upper())
