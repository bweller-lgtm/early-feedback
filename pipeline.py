"""Pipeline orchestrator: wires the 5 steps together."""

import asyncio
import sys
import time

from models import ProductContext, SyntheticPersona, InterviewTranscript, FeedbackAnalysis, EvaluationReport
from steps.parse_context import parse_context
from steps.generate_personas import generate_personas
from steps.simulate_interviews import simulate_interviews
from steps.analyze_feedback import analyze_feedback
from steps.generate_report import generate_report


def _log(msg: str):
    print(msg, file=sys.stderr, flush=True)


def run_evaluation(idea_text: str, num_personas: int | None = None) -> EvaluationReport:
    """Run the full evaluation pipeline on an idea."""

    # Step 1: Parse context
    _log("Step 1/5: Parsing product context...")
    t0 = time.time()
    context = parse_context(idea_text)
    _log(f"  → {context.product_name} ({time.time() - t0:.1f}s)")

    # Step 2: Generate personas
    _log(f"Step 2/5: Generating personas...")
    t0 = time.time()
    personas = generate_personas(context, num_personas)
    _log(f"  → {len(personas)} personas ({time.time() - t0:.1f}s)")

    # Step 3: Simulate interviews (async)
    _log(f"Step 3/5: Simulating interviews...")
    t0 = time.time()
    transcripts = asyncio.run(simulate_interviews(personas, context))
    _log(f"  → {len(transcripts)} interviews ({time.time() - t0:.1f}s)")

    # Step 4: Analyze feedback
    _log("Step 4/5: Analyzing feedback...")
    t0 = time.time()
    analysis = analyze_feedback(transcripts, context)
    _log(f"  → {len(analysis.themes)} themes identified ({time.time() - t0:.1f}s)")

    # Step 5: Generate report
    _log("Step 5/5: Generating report...")
    t0 = time.time()
    report = generate_report(context, transcripts, analysis)
    _log(f"  → Score: {report.overall_score}/10 ({time.time() - t0:.1f}s)")

    return report
