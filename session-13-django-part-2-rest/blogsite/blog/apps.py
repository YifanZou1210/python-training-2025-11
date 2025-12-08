from django.apps import AppConfig
# django配置类，通过 python manage.py startapp blog自动生成

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'    # 默认主键类型
    name = 'blog'    # app名称, 同时说明根路径
# 必须在installed_apps中注册，让django扫描到app内部的models, signals, migrations等才会加载app配置找到内部的models以及加载static folder, 不register的话不知道