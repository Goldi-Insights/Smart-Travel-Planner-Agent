"""
Smart Travel Planner — Trip Cost Predictor (ML Module)
Loads trained Random Forest model and returns cost estimate.
This file lives in ml/ and is imported by services/predict_service.py.
"""

import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
ENCODERS_PATH = os.path.join(BASE_DIR, "encoders.pkl")

VALID_DESTINATIONS = ["Goa", "Jaipur", "Kerala", "Shimla", "Andaman", "Ladakh"]
VALID_TRANSPORT    = ["flight", "train", "bus"]
VALID_HOTEL        = ["budget", "standard", "luxury"]


def load_artifacts():
    """Load model and encoders from disk."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run: python ml/train.py"
        )
    if not os.path.exists(ENCODERS_PATH):
        raise FileNotFoundError(
            f"Encoders not found at {ENCODERS_PATH}. Run: python ml/train.py"
        )
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(ENCODERS_PATH, "rb") as f:
        encoders = pickle.load(f)
    return model, encoders


def predict_cost(
    destination: str,
    days: int,
    travelers: int,
    transport_type: str,
    hotel_type: str,
) -> dict:
    """
    Predict the estimated trip cost.

    Returns a dict with:
        - estimated_cost (int)
        - per_person_cost (int)
        - confidence_range (dict): low / high bounds
        - breakdown (dict): approximate cost breakdown
    """
    destination    = destination.strip().title()
    transport_type = transport_type.strip().lower()
    hotel_type     = hotel_type.strip().lower()

    if destination not in VALID_DESTINATIONS:
        raise ValueError(f"Unknown destination '{destination}'. Choose from: {VALID_DESTINATIONS}")
    if transport_type not in VALID_TRANSPORT:
        raise ValueError(f"Unknown transport '{transport_type}'. Choose from: {VALID_TRANSPORT}")
    if hotel_type not in VALID_HOTEL:
        raise ValueError(f"Unknown hotel type '{hotel_type}'. Choose from: {VALID_HOTEL}")
    if days < 1 or days > 30:
        raise ValueError("days must be between 1 and 30")
    if travelers < 1 or travelers > 20:
        raise ValueError("travelers must be between 1 and 20")

    model, encoders = load_artifacts()

    dest_enc  = encoders["destination"].transform([destination])[0]
    trans_enc = encoders["transport_type"].transform([transport_type])[0]
    hotel_enc = encoders["hotel_type"].transform([hotel_type])[0]

    features = np.array([[dest_enc, days, travelers, trans_enc, hotel_enc]])

    estimated_cost   = int(model.predict(features)[0])
    tree_predictions = [tree.predict(features)[0] for tree in model.estimators_]
    low  = int(np.percentile(tree_predictions, 10))
    high = int(np.percentile(tree_predictions, 90))
    per_person = estimated_cost // travelers

    breakdown_pct = {
        "budget":   {"transport": 0.35, "hotel": 0.25, "food": 0.20, "activities": 0.20},
        "standard": {"transport": 0.30, "hotel": 0.32, "food": 0.22, "activities": 0.16},
        "luxury":   {"transport": 0.25, "hotel": 0.42, "food": 0.18, "activities": 0.15},
    }
    pct       = breakdown_pct[hotel_type]
    breakdown = {k: int(estimated_cost * v) for k, v in pct.items()}

    return {
        "estimated_cost":    estimated_cost,
        "per_person_cost":   per_person,
        "confidence_range":  {"low": low, "high": high},
        "breakdown":         breakdown,
        "inputs": {
            "destination":    destination,
            "days":           days,
            "travelers":      travelers,
            "transport_type": transport_type,
            "hotel_type":     hotel_type,
        },
    }
