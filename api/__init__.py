import pkgutil
import importlib
import sys
from modules.server import app

# 自动导入当前包下的所有模块
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    try:
        module = importlib.import_module(f"api.{modname}")
        # 如果模块有 router 属性，则注册到 app
        if hasattr(module, 'router'):
            app.include_router(module.router)
    except ImportError as e:
        print(f"Failed to import api.{modname}: {e}")