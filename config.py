import redis
import logging


class BaseConfig(object):
    """启动配置类"""
    SECRET_KEY = "xiaoya21"

    # 数据库配置
    SQLALCHEMY_DATABASE_URL = "mysql://root:mysql@localhost:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = "redis"  # 指定session的保存位置
    SESSION_USE_SIGNER = True  # 设置session存储签名
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 24 * 3600 * 2  # session的有效时间（s）


class Develop(BaseConfig):
    """开发模式"""
    DEBUG = True
    DEBUG_LEVEL = logging.DEBUG


class Production(BaseConfig):
    """生产环境"""
    DEBUG_LEVEL = logging.ERROR
    pass


# 提供外界获取配置信息的方式
config_dict = {
    "develop": Develop,
    "product": Production
}
