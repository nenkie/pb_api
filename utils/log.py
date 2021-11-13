LOGGING = """
        {
          "version": 1,
          "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
          },
          "handlers": {
            "console": {
              "class": "logging.StreamHandler",
              "level": "DEBUG",
              "formatter": "default",
              "stream": "ext://sys.stdout"
            }
          },
          "root": {
            "level": "DEBUG",
            "handlers": ["console"]
          }
        }
"""
