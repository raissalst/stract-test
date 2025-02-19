from flask import Blueprint

from app.controllers.general_controller import (
    get_all_platforms,
    get_all_platforms_platform_collapsed,
)

bp_general = Blueprint("geral", __name__, url_prefix="/geral")

bp_general.get("")(get_all_platforms)
bp_general.get("/resumo")(get_all_platforms_platform_collapsed)
