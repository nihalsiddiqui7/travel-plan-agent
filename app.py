from pathlib import Path

from fastapi import FastAPI, Request, Form
import uvicorn
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel



BASE_DIR =Path(__file__).resolve().parent

app = FastAPI(title="Travel Plan Agent",
            description="A travel plan agent that can help you plan your trips.",
            version="1.0.0")

app.mount("/static", 
        StaticFiles(directory=str(BASE_DIR / "static")),
        name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
        return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                        "result": None,
                },
        )


@app.post("/plan", response_class=HTMLResponse)
def plan_trip(
        request: Request,
        origin: str = Form(""),
        destination: str = Form(""),
        trip_type: str = Form(""),
        budget: str = Form(""),
        dates: str = Form(""),
        travelers: int = Form(1),
        user_query: str = Form(""),
):
        pieces = [user_query.strip()]

        if origin.strip() or destination.strip():
                pieces.append(f"Origin: {origin.strip() or 'Not specified'}")
                pieces.append(f"Destination: {destination.strip() or 'Not specified'}")

        if trip_type.strip():
                pieces.append(f"Trip style: {trip_type.strip()}")

        if budget.strip():
                pieces.append(f"Budget: {budget.strip()}")

        if dates.strip():
                pieces.append(f"Dates: {dates.strip()}")

        pieces.append(f"Travelers: {travelers}")

        query = "\n".join(piece for piece in pieces if piece)
        result = run_travel_plan_agent(query)

        return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                        "result": result,
                },
        )


@app.get("/health", response_class=JSONResponse)
async def health_check():
        return JSONResponse(content={"status": "ok"})