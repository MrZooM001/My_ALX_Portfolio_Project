#!/usr/bin/python3
from api.v1.main import create_app
from api.v1.config import DevConfig


if __name__ == "__main__":
    app = create_app(DevConfig)
    app.run()
