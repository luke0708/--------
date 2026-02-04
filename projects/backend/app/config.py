from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


@dataclass
class DeepSeekConfig:
    base_url: str
    api_key: str
    model: str


@dataclass
class AppConfig:
    secret_key: str
    access_token_expire_minutes: int
    admin_username: Optional[str]
    admin_password: Optional[str]
    database_url: str
    deepseek: DeepSeekConfig


def _get_nested(data: Dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if isinstance(data, dict) and key in data:
            return data[key]
    return None


def _pick_latest_model(config: Dict[str, Any]) -> Optional[str]:
    if not isinstance(config, dict):
        return None
    if isinstance(config.get("model_latest"), str):
        return config["model_latest"]
    if isinstance(config.get("model"), str):
        return config["model"]
    models = config.get("models")
    if isinstance(models, list) and models:
        last = models[-1]
        if isinstance(last, str):
            return last
        if isinstance(last, dict) and isinstance(last.get("name"), str):
            return last["name"]
    return None


def _load_toml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    load_dotenv(Path(".env"))

    config_path = config_path or Path("./config.toml")
    data = _load_toml(config_path)

    api_section = data.get("api", {}) if isinstance(data, dict) else {}
    deepseek_section = data.get("deepseek", {}) if isinstance(data, dict) else {}

    base_url = (
        os.getenv("DEEPSEEK_BASE_URL")
        or _get_nested(deepseek_section, "base_url", "baseUrl")
        or _get_nested(api_section, "base_url", "baseUrl")
        or "https://api.deepseek.com"
    )
    api_key = (
        os.getenv("DEEPSEEK_API_KEY")
        or _get_nested(deepseek_section, "key", "api_key", "apiKey")
        or _get_nested(api_section, "key", "api_key", "apiKey")
        or ""
    )

    model = (
        os.getenv("DEEPSEEK_MODEL")
        or _pick_latest_model(deepseek_section)
        or _pick_latest_model(api_section)
        or "deepseek-chat"
    )

    secret_key = os.getenv("SECRET_KEY") or data.get("secret_key") or "dev-secret"
    access_token_expire_minutes = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        or data.get("access_token_expire_minutes")
        or 60
    )

    admin_username = os.getenv("ADMIN_USERNAME") or data.get("admin_username")
    admin_password = os.getenv("ADMIN_PASSWORD") or data.get("admin_password")

    database_url = (
        os.getenv("DATABASE_URL")
        or data.get("database_url")
        or "sqlite:///./backend/data/app.db"
    )

    deepseek = DeepSeekConfig(base_url=base_url, api_key=api_key, model=model)

    return AppConfig(
        secret_key=secret_key,
        access_token_expire_minutes=access_token_expire_minutes,
        admin_username=admin_username,
        admin_password=admin_password,
        database_url=database_url,
        deepseek=deepseek,
    )


settings = load_config()
