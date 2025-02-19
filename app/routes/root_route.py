from flask import Blueprint
from app.controllers.root_controller import get_main_user

bp_root = Blueprint("root", __name__, url_prefix="/")

bp_root.get("")(get_main_user)