from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from ihome_flask import db


class BaseModel(object):
    """模型基类"""
    # 记录创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 记录更新时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "ih_user_profile"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11), unique=True, nullable=False)
    real_name = db.Column(db.String(32))
    id_card = db.Column(db.Integer(20))
    # 用户头像路径
    avatar_url = db.Column(db.String(128))
    # 用户发布的房屋
    houses = db.relationship("House", backref="user")
    # 用户下的订单
    orders = db.relationship("Order", backref="user")

    @property
    def password(self):
        raise AttributeError("不能读取")

    # 将密码加密处理
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    # 在登录的时候比对密码
    def check_password(self, value):
        # 传入密码，明文，返回True表示正确，Flase表示错误
        return check_password_hash(self.password_hash, value)

    # 获取user的基本展示信息
    def user_to_dict(self):
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "real_name": self.real_name,
            "id_card": self.id_card,
            # "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else ""
        }
        return user_dict


