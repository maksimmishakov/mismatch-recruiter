from app.routes import matching_v2
from app.routes import analytics
app.include_router(matching_v2.router)
app.include_router(analytics.router)
