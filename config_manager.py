"""
Task 4 - Environment & Configuration Manager

This module centralizes application settings, loads values from a .env file,
validates required keys, and masks secrets when settings are displayed.
It is dependency-free and can be copied into any Python backend project.
"""

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_FILE = BASE_DIR / ".env"
MASKED_SECRET = "********"


class ConfigurationError(RuntimeError):
    """Raised when configuration is missing or invalid."""


def load_env_file(path: Path = DEFAULT_ENV_FILE) -> None:
    """
    Load KEY=VALUE pairs from a .env file into os.environ.

    Existing environment variables are not overwritten. This allows real server
    secrets to take priority over local development values.
    """
    if not path.exists():
        return

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[len("export ") :].strip()

        if "=" not in line:
            raise ConfigurationError(f"Invalid .env line {line_number}: missing '='.")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")

        if not key:
            raise ConfigurationError(f"Invalid .env line {line_number}: empty key.")

        os.environ.setdefault(key, value)


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def get_bool_env(name: str, default: bool) -> bool:
    value = get_env(name)
    if value is None:
        return default

    normalized = value.lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False

    raise ConfigurationError(f"{name} must be true or false.")


def get_int_env(name: str, default: int, minimum: int | None = None) -> int:
    value = get_env(name)

    try:
        parsed = default if value is None else int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a number.") from exc

    if minimum is not None and parsed < minimum:
        raise ConfigurationError(f"{name} must be at least {minimum}.")

    return parsed


def get_path_env(name: str, default: str) -> Path:
    value = get_env(name, default)
    path = Path(value)
    return path if path.is_absolute() else BASE_DIR / path


@dataclass(frozen=True)
class AppConfig:
    app_name: str
    environment: str
    debug: bool
    host: str
    port: int
    admin_username: str
    admin_password: str
    database_path: Path
    log_file: Path
    evidence_dir: Path
    api_key: str | None

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    def validate(self) -> None:
        missing = []

        if self.is_production:
            required_keys = {
                "APP_ADMIN_USERNAME": self.admin_username,
                "APP_ADMIN_PASSWORD": self.admin_password,
            }
            missing = [key for key, value in required_keys.items() if not value]

        if missing:
            raise ConfigurationError(f"Missing required environment variables: {', '.join(missing)}.")

        if self.is_production and self.admin_password == "change-me":
            raise ConfigurationError("APP_ADMIN_PASSWORD must be changed in production.")

    def public_dict(self) -> dict:
        """
        Return settings that are safe to show in logs, dashboards, or APIs.
        Secret values are masked.
        """
        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "debug": self.debug,
            "host": self.host,
            "port": self.port,
            "database_path": str(self.database_path),
            "log_file": str(self.log_file),
            "evidence_dir": str(self.evidence_dir),
            "admin_username": self.admin_username,
            "admin_password": MASKED_SECRET,
            "api_key": MASKED_SECRET if self.api_key else None,
        }


def load_config(env_file: Path = DEFAULT_ENV_FILE) -> AppConfig:
    load_env_file(env_file)

    config = AppConfig(
        app_name=get_env("APP_NAME", "AI Proctoring System"),
        environment=get_env("APP_ENV", "development"),
        debug=get_bool_env("APP_DEBUG", False),
        host=get_env("APP_HOST", "127.0.0.1"),
        port=get_int_env("APP_PORT", 8000, minimum=1),
        admin_username=get_env("APP_ADMIN_USERNAME", "admin"),
        admin_password=get_env("APP_ADMIN_PASSWORD", "change-me"),
        database_path=get_path_env("APP_DATABASE_PATH", "data/app.db"),
        log_file=get_path_env("APP_LOG_FILE", "logs/app.log"),
        evidence_dir=get_path_env("APP_EVIDENCE_DIR", "evidence"),
        api_key=get_env("APP_API_KEY"),
    )
    config.validate()
    return config


settings = load_config()


if __name__ == "__main__":
    print(settings.public_dict())
