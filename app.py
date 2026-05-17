from fastapi import FastAPI

from orders.views import router

app = FastAPI(
    title="Orders API: SSE + HTMX Demo",
)
app.include_router(router)
