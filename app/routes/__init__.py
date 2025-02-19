from flask import Flask

from app.routes.general_route import bp_general
from app.routes.platform_route import bp_platform
from app.routes.root_route import bp_root


def init_app(app: Flask):
    app.register_blueprint(bp_general)
    app.register_blueprint(bp_platform)
    app.register_blueprint(bp_root)
