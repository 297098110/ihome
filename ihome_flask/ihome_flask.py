# 创建蓝图
from flask import Blueprint, current_app
from flask_wtf.csrf import generate_csrf

html = Blueprint("ihome_flask", __name__)


# 使用蓝图装饰视图函数
@html.route("/<re(r'.*'):file_name>")
def get_html_page(file_name):
    # 判断是否访问的根路径
    if not file_name:
        file_name = "index.html"

    # 判断不是favicon.ico才进行拼接：
    if file_name != "favicon.ico":
        file_name = "html/" + file_name

    response = current_app.send_static_file(file_name)

    # 给cookie中设置csrf_token
    token = generate_csrf()
    response.set_cookie("csrf_token", token)

    return response
