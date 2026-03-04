"""Minimal configuration for SimulatedInnovation."""

import os
from pathlib import Path

# API
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Model
MODEL = os.environ.get("SI_MODEL", "claude-sonnet-4-20250514")

# Pipeline defaults
NUM_PERSONAS = int(os.environ.get("SI_NUM_PERSONAS", "8"))
MAX_CONCURRENT = int(os.environ.get("SI_MAX_CONCURRENT", "5"))

# Paths
PROJECT_DIR = Path(__file__).parent
PROMPTS_DIR = PROJECT_DIR / "prompts"
OUTPUT_DIR = PROJECT_DIR / "outputs"
