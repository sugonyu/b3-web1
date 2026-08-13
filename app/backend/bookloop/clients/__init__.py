"""BookLoop의 제품 browser client Blueprints.

Outline:
1. jinja_client — Flask/Jinja product client
2. vanilla_client — static Flask Vanilla client boundary
3. __all__ — package public exports
"""

from .flask_vanilla import vanilla_client
from .jinja_product import jinja_client

__all__ = ["jinja_client", "vanilla_client"]
