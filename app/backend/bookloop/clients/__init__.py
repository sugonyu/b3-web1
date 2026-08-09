"""BookLoop의 제품 browser client Blueprints."""

from .flask_vanilla import vanilla_client
from .jinja_product import jinja_client

__all__ = ["jinja_client", "vanilla_client"]
