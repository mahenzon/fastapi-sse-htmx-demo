from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse

from misc.templating import templates
from orders.views import router

app = FastAPI(
    title="Orders API: SSE + HTMX Demo",
)
app.include_router(router)


@app.get("/", include_in_schema=False)
def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
