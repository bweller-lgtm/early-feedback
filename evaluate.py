#!/usr/bin/env python3
"""CLI entry point for Simulated Innovation evaluator."""

import argparse
import sys
import time
from pathlib import Path
from datetime import date


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a project idea using synthetic user personas and simulated interviews.",
    )
    parser.add_argument("idea", nargs="?", help="The project idea to evaluate (text)")
    parser.add_argument("--file", "-f", help="Read idea from a text file instead")
    parser.add_argument("--personas", "-p", type=int, help="Number of personas to generate (default: 8)")
    parser.add_argument("--output", "-o", help="Output file path (default: outputs/YYYY-MM-DD-name.md)")
    parser.add_argument("--model", "-m", help="Claude model to use")
    args = parser.parse_args()

    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Override model if specified
    if args.model:
        import config
        config.MODEL = args.model

    # Get idea text
    if args.file:
        idea_text = Path(args.file).read_text(encoding="utf-8")
    elif args.idea:
        idea_text = args.idea
    else:
        parser.error("Provide an idea as a positional argument or use --file")

    # Validate API key
    from config import ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not set. Create a .env file or set the environment variable.", file=sys.stderr)
        sys.exit(1)

    # Run pipeline
    from pipeline import run_evaluation

    print(f"\n{'='*60}", file=sys.stderr)
    print("  Simulated Innovation Evaluator", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    t_start = time.time()
    report = run_evaluation(idea_text, args.personas)
    elapsed = time.time() - t_start

    # Write report
    from config import OUTPUT_DIR
    OUTPUT_DIR.mkdir(exist_ok=True)

    if args.output:
        output_path = Path(args.output)
    else:
        # Generate filename from product name
        slug = report.markdown_report.split("\n")[0].strip("# ").strip()[:50]
        slug = "".join(c if c.isalnum() or c in " -" else "" for c in slug).strip().replace(" ", "-").lower()
        slug = slug or "evaluation"
        output_path = OUTPUT_DIR / f"{date.today().isoformat()}-{slug}.md"

    output_path.write_text(report.markdown_report, encoding="utf-8")

    # Print summary to stdout
    print(f"\n{'='*60}")
    print(f"  EVALUATION: {report.verdict}")
    print(f"  SCORE: {report.overall_score}/10")
    print(f"{'='*60}")
    print(f"\n  Problem Validity:      {report.score_breakdown.problem_validity}/10")
    print(f"  Solution Fit:          {report.score_breakdown.solution_fit}/10")
    print(f"  Market Demand:         {report.score_breakdown.market_demand}/10")
    print(f"  Competitive Position:  {report.score_breakdown.competitive_position}/10")
    print(f"  Monetization:          {report.score_breakdown.monetization_potential}/10")
    print()
    if report.executive_summary:
        print(report.executive_summary)
        print()
    if report.top_recommendations:
        print("Top Recommendations:")
        for i, rec in enumerate(report.top_recommendations, 1):
            print(f"  {i}. {rec}")
        print()
    print(f"Full report: {output_path}", file=sys.stderr)
    print(f"Completed in {elapsed:.0f}s\n", file=sys.stderr)


if __name__ == "__main__":
    main()
