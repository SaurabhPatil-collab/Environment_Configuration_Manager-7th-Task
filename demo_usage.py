from config_manager import ConfigurationError, settings


def main():
    try:
        print("Application:", settings.app_name)
        print("Environment:", settings.environment)
        print("Server:", f"{settings.host}:{settings.port}")
        print("Database:", settings.database_path)
        print("Safe config output:", settings.public_dict())
    except ConfigurationError as exc:
        print("Configuration error:", exc)


if __name__ == "__main__":
    main()
