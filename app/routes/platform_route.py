from flask import Blueprint
from app.controllers.platform_controller import get_a_platform, get_a_platform_user_collapsed

bp_platform = Blueprint("plataforma", __name__)

bp_platform.get("/<string:platform>")(get_a_platform)
bp_platform.get("/<string:platform>/resumo")(get_a_platform_user_collapsed)