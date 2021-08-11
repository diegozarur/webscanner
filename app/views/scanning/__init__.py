from flask import Blueprint

blueprint = Blueprint(
    'scanning_blueprint',
    __name__,
    url_prefix='/api/scanning',
)
