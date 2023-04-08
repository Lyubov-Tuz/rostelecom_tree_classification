from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api_tools import router as api_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# при получении ссылки проверяется возврат кода 200, далее если по ссылке не текст, то отображается фраза "есть файл"
# в остальных случаях возвращается фраза "файла нет"

@app.get("/classifier")
async def classifier(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            content_type = r.headers.get("content-type")
            if "text" not in content_type.lower():
                return {"message": "Тут есть какой-то файл, надо что-то сделать"}
            else:
                return {"message": "Тут файла нет, предоставьте корректную ссылку"}
        else:
            return {"message": "Тут файла нет, предоставьте корректную ссылку"}
    except:
        return {"message": "Тут файла нет, предоставьте корректную ссылку"}
