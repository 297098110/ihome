# 转换器
from functools import wraps
from flask import g, session, jsonify
from werkzeug.routing import BaseConverter

from ihome_flask.utils.response_code import RET


class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex


# 登录装饰器
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        g.user_id = session.get("user_id")

        if g.user_id:
            return view_func(*args, **kwargs)
        else:
            return jsonify(errno=RET.USERERR, errmsg="用户尚未登录")
    return wrapper