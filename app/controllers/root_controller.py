from http import HTTPStatus
import json
from flask import Response

def get_main_user():
    user_data = {
        'name': 'Raissa Laubenbacher Sampaio de Toledo',
        'email': 'raissalst@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/raissalstoledo/'
    }
    return Response(
        json.dumps(user_data, ensure_ascii=False), 
        status=HTTPStatus.OK, 
        content_type="application/json; charset=utf-8"
    )
