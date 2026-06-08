# Smart Travel Planner — Flask Backend

AI-powered travel planning system converted from FastAPI to **Flask**.

## Project Structure

```
travel-planner-flask/
├── app.py                  ← Flask entry point (run this)
├── requirements.txt        ← Python dependencies
├── .env                    ← API keys & config
├── routes/
│   ├── travel.py           ← /api/travel/* — destinations & recommendations
│   ├── weather.py          ← /api/weather/* — current weather & forecast
│   ├── predict.py          ← /api/predict/* — ML cost prediction
│   └── itinerary.py        ← /api/itinerary/* — AI itinerary (IBM watsonx)
├── services/
│   ├── destination_service.py
│   ├── weather_service.py
│   ├── predict_service.py
│   └── itinerary_service.py
├── ml/
│   ├── train.py            ← Run once to train the model
│   └── predict.py          ← ML inference logic
├── rag/
│   └── knowledge_base.py   ← ChromaDB RAG setup
├── data/
│   ├── dataset.csv
│   └── chroma_db/          ← Vector DB (auto-created)
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

## Quick Start

### 1. Create & activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Edit `.env` (already present) and fill in your keys:

```env
IBM_API_KEY=your_ibm_api_key_here
PROJECT_ID=your_watsonx_project_id
IBM_REGION=au-syd          # or us-south, eu-de, jp-tok
OPENWEATHER_API_KEY=your_openweather_key

API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5500
ENVIRONMENT=development
```

### 4. Train the ML model (one-time)

```bash
python ml/train.py
```

### 5. Run the Flask server

```bash
python app.py
```

The server starts at **http://localhost:8000**

---

## API Endpoints

### Health
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |

### Travel — `/api/travel`
| Method | URL | Params |
|--------|-----|--------|
| GET | `/api/travel/destinations` | — |
| GET | `/api/travel/destination/<name>` | name e.g. `Goa` |
| GET | `/api/travel/recommend` | `budget`, `days`, `travelers`, `interests` |

### Weather — `/api/weather`
| Method | URL | Params |
|--------|-----|--------|
| GET | `/api/weather/current` | `city` |
| GET | `/api/weather/forecast` | `city`, `days` (1-7) |

### Cost Prediction — `/api/predict`
| Method | URL | Body (JSON) |
|--------|-----|-------------|
| POST | `/api/predict/cost` | `destination`, `days`, `travelers`, `transport_type`, `hotel_type` |
| GET | `/api/predict/destinations` | — |

**Example request:**
```bash
curl -X POST http://localhost:8000/api/predict/cost \
  -H "Content-Type: application/json" \
  -d '{"destination":"Goa","days":5,"travelers":2,"transport_type":"flight","hotel_type":"standard"}'
```

### Itinerary — `/api/itinerary`
| Method | URL | Body (JSON) |
|--------|-----|-------------|
| POST | `/api/itinerary/generate` | `source`, `destination`, `budget`, `days`, `travelers`, `interests[]`, `transport_type`, `hotel_type` |

**Example request:**
```bash
curl -X POST http://localhost:8000/api/itinerary/generate \
  -H "Content-Type: application/json" \
  -d '{"source":"Mumbai","destination":"Goa","budget":25000,"days":5,"travelers":2,"interests":["beaches","food"],"transport_type":"flight","hotel_type":"standard"}'
```

---

## Key Changes from FastAPI → Flask

| Feature | FastAPI (original) | Flask (this version) |
|---|---|---|
| Framework | `FastAPI` | `Flask` |
| CORS | `fastapi.middleware.cors` | `flask-cors` |
| Routers | `APIRouter` | `Blueprint` |
| Request params | Pydantic models / Query() | `request.args` / `request.get_json()` |
| Responses | Auto-serialized | `jsonify()` |
| Async routes | Native `async def` | `asyncio.run()` wrapper |
| Validation | Pydantic + FastAPI | Manual checks |
| Auto docs | `/docs` (Swagger) | Not included (use Postman) |

---

## Frontend

Open `frontend/index.html` with a local server (e.g. VS Code Live Server on port 5500).
The frontend calls `http://localhost:8000` by default.
# Smart-Travel-Planner-Agent
