# Travel Plan Agent

A modern AI-powered travel planning web app built with FastAPI, LangGraph, and OpenAI. The application takes a natural-language trip request, searches for flights and hotels, generates a structured itinerary, and presents the result in a clean web interface.

This project was designed to demonstrate full-stack AI application development, orchestration of multiple agents, persistent conversation state, and production-ready deployment with Docker.

## Highlights

- Multi-step travel planning workflow driven by LangGraph
- Flight lookup using a custom airport and location resolution tool
- Hotel discovery powered by Tavily search
- Itinerary generation with OpenAI and structured prompt chaining
- Persistent graph state using PostgreSQL checkpointing
- FastAPI web app with server-rendered UI
- Responsive, minimal interface focused on readability
- Dockerfile included for cloud deployment on Render
- LangSmith tracing support for debugging and observability

## Live Workflow

1. The user enters a trip request such as origin, destination, budget, dates, and traveler count.
2. The backend normalizes the request and sends it through a LangGraph pipeline.
3. The flight agent searches for flight options.
4. The hotel agent collects hotel-related results.
5. The itinerary agent creates a detailed travel plan.
6. The final response agent formats the output for display in the UI.
7. The result is stored with a thread ID so the conversation can be resumed or traced.

## Tech Stack

- Python 3.13
- FastAPI
- Jinja2
- LangGraph
- LangChain
- OpenAI GPT-4o mini
- Tavily Search
- PostgreSQL
- Psycopg 3
- Docker
- Uvicorn

## Project Structure

```text
travel-plan-agent/
  app.py               # FastAPI routes and web app entrypoint
  backend.py           # LangGraph workflow and agent orchestration
  tools/
    flight_tool.py      # Flight search and airport resolution logic
    tavily_tool.py      # Hotel and web search helper
  templates/
    index.html          # Main UI template
  static/
    style.css           # Shared site styles
    script.js           # Frontend behavior
  requirements.txt      # Python dependencies
  Dockerfile            # Container config for Render
```

## Features

### Flight and hotel planning
The backend separates planning into dedicated stages so the application can gather flight and hotel context before generating the final itinerary.

### State persistence
The graph uses PostgreSQL checkpointing, which allows the workflow to keep state across requests using a thread ID.

### Observability
LangSmith tracing is enabled through environment variables, making it easier to inspect execution paths and debug prompts, tool calls, and model responses.

### Clean UI
The frontend is intentionally minimal and focuses on the generated itinerary as the primary result, with additional details available on demand.

## Getting Started

### Prerequisites

- Python 3.13 or compatible version
- PostgreSQL database
- OpenAI API key
- Tavily API key
- Optional: LangSmith API key for tracing

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd travel-plan-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv travelenv
travelenv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
DATABASE_URL=your_postgres_connection_string
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=travel_plan_agent
LANGSMITH_TRACING=true
LANGCHAIN_TRACING_V2=true
DEFAULT_ORIGIN_IATA=IXU
```

### 5. Run the app locally

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open the app in your browser:

```text
http://127.0.0.1:8000
```

## Docker

You can run the project in a container using the included Dockerfile.

```bash
docker build -t travel-plan-agent .
docker run -p 8000:8000 --env-file .env travel-plan-agent
```

## Deploying to Render

This repository is ready to be deployed to Render as a Web Service.

### Recommended settings

- **Environment**: Docker
- **Build command**: use the Dockerfile build
- **Start command**: handled by the Dockerfile
- **Port**: Render will assign `PORT` automatically

### Required Render environment variables

- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
- `DATABASE_URL`
- `LANGSMITH_API_KEY` if tracing is enabled
- `LANGSMITH_ENDPOINT`
- `LANGSMITH_PROJECT`

## API Endpoints

### `GET /`
Renders the main travel planning interface.

### `POST /plan`
Accepts form input, runs the travel planning workflow, and returns the rendered results page.

### `GET /health`
Simple health check endpoint for deployment monitoring.

## Why this project stands out

This project is more than a single API call or a static demo. It combines:

- multi-agent orchestration
- search tools for real-world planning inputs
- persistent graph-based workflow state
- server-rendered UI for human-friendly output
- production deployment support through Docker

That makes it a strong portfolio piece for roles involving AI engineering, backend development, or applied LLM systems.

## Future Improvements

- Add true PDF export for itinerary downloads
- Cache repeated flight and hotel lookups
- Add user authentication and saved trip history
- Expose the planner as a REST API as well as a web UI
- Add tests for graph nodes and route behavior

## License

This project is available under the terms of the LICENSE file in this repository.
