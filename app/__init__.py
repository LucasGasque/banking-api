from datetime import datetime
from app.serializers.root import AppInfo
from app.configs.settings import settings


__version__ = "1.0.0"

app_info = AppInfo(
    application=settings.APP_NAME, version=__version__, started_at=datetime.now()
)
