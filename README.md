# Task 4 - Environment & Configuration Manager

## Objective

Centralize application configurations, API keys, and environment settings in one safe place.

## What This Task Does

This task creates a common configuration manager for a backend project. Instead of writing settings directly inside different code files, all values are loaded from environment variables or a `.env` file.

Examples of managed values:

- Application name
- Environment mode, such as development or production
- Host and port
- Admin username and password
- Database path
- Log file path
- Evidence folder path
- API keys

## Files Included

- `config_manager.py` - Main environment and configuration manager
- `.env.example` - Sample environment file
- `demo_usage.py` - Small demo showing how to use the manager
- `README.md` - Explanation and workflow

## How It Works

Workflow:

```text
.env file
   -> config_manager.py loads values
   -> values are validated
   -> settings object is created
   -> backend files use settings
```

Example usage:

```python
from config_manager import settings

print(settings.database_path)
print(settings.admin_username)
```

## Missing Key Handling

In development, safe default values are allowed.

In production, important values must be provided:

```env
APP_ENV=production
APP_ADMIN_USERNAME=admin
APP_ADMIN_PASSWORD=strong-password
```

If these are missing, the system raises a clear error.

## Secure Secrets Handling

The real password and API key are available internally to the application, but they are masked when displayed publicly.

Example safe output:

```text
admin_password: ********
api_key: ********
```

## How To Run

1. Copy `.env.example` to `.env`.
2. Edit `.env` with your values.
3. Run:

```powershell
python demo_usage.py
```

## Explanation For Captain

Task 4 is used to manage all backend configuration from one central place. I created a configuration manager that loads values from a `.env` file, validates required settings, handles missing keys, and protects secrets by masking passwords and API keys. This makes the project easier to maintain, safer, and ready for deployment because settings can be changed without editing source code.
