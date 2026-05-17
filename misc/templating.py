from fastapi.templating import Jinja2Templates

from config import BASE_DIR

TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(
    directory=TEMPLATES_DIR,
)
