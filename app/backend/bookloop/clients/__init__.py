"""BookLoop browser-facing Flask client Blueprints."""

from .client_jinja import jinja_client
from .client_test import client_test
from .client_vanilla import vanilla_client

__all__ = ["jinja_client", "client_test", "vanilla_client"]
