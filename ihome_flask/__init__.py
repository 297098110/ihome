import logging
from logging.handlers import RotatingFileHandler
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config_dict
from ihome_flask.utils.commons import RegexConverter

# 创建数据库对象
db = SQLAlchemy()

# 创建redis_store对象
redis_store = None


# 工厂方法，根据配置信息，返回对应的app对象
def create_app(config_name):
    # 创建应用程序对象
    app = Flask(__name__)
    # 通过配置名，获取配置类
    config = config_dict.get(config_name)
    # 将配置信息加载到app中
    app.config.from_object(config)
    # 创建日志记录文件
    log_file(config.DEBUG_LEVEL)
    # 初始化session
    Session(app)
    # 初始化数据库，绑定数据库和应用程序app
    db.init_app(app)
    # csrf配置
    CSRFProtect(app)
    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    # 添加自定义的转换器到转换器列表中
    app.url_map.converters['re'] = RegexConverter
    # 注册蓝图
    from ihome_flask.api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")
    # 注册静态文件蓝图
    from ihome_flask.ihome_flask import html
    app.register_blueprint(html)
    print(app.url_map)
    return app


def log_file(debug_level):
    # 设置日志记录等级
    logging.basicConfig(level=debug_level)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式
    formatter = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask_app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
