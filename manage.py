# 调用方法，获取app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from ihome_flask import create_app, db

app = create_app("develop")

# 创建应用程序管理对象
manager = Manager(app)

# 关联app和db
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
