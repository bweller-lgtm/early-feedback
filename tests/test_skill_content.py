"""Tests that the evaluate.md skill file contains all required methodology.

These tests ensure that any edits to the skill preserve the complete
evaluation framework -- scoring, persona diversity, interview coverage,
report structure, and output instructions.
"""

import pytest
from conftest import SKILL_PATH


class TestSkillFileExists:
    def test_skill_file_exists(self):
        assert SKILL_PATH.exists(), f"Skill file missing: {SKILL_PATH}"

    def test_skill_file_not_empty(self, skill_content):
        assert len(skill_content.strip()) > 500, "Skill file appears too short"

    def test_arguments_placeholder(self, skill_content):
        assert "$ARGUMENTS" in skill_content, "Must reference $ARGUMENTS for user input"


class TestStep1ParseContext:
    """Verify context parsing instructions are complete."""

    def test_product_name_field(self, skill_content):
        assert "product name" in skill_content.lower()

    def test_value_proposition_field(self, skill_content):
        assert "value proposition" in skill_content.lower()

    def test_target_users_field(self, skill_content):
        assert "target users" in skill_content.lower()

    def test_core_features_field(self, skill_content):
        assert "core features" in skill_content.lower()

    def test_competitors_field(self, skill_content):
        assert "competitors" in skill_content.lower()

    def test_differentiation_field(self, skill_content):
        assert "differentiation" in skill_content.lower()

    def test_assumptions_field(self, skill_content):
        assert "assumptions" in skill_content.lower()

    def test_product_stage_field(self, skill_content):
        assert "product stage" in skill_content.lower()

    def test_product_type_field(self, skill_content):
        assert "product type" in skill_content.lower()

    def test_key_benefits_field(self, skill_content):
        assert "key benefits" in skill_content.lower()

    def test_target_industries_field(self, skill_content):
        assert "target industries" in skill_content.lower()


class TestStep2Personas:
    """Verify persona generation methodology is complete."""

    def test_eight_personas(self, skill_content):
        assert "8" in skill_content, "Must specify 8 personas"

    def test_skeptic_distribution(self, skill_content):
        assert "2 skeptic" in skill_content.lower()

    def test_neutral_distribution(self, skill_content):
        assert "3 neutral" in skill_content.lower()

    def test_enthusiastic_distribution(self, skill_content):
        assert "3 enthusiastic" in skill_content.lower()

    def test_tech_savviness_levels(self, skill_content):
        lower = skill_content.lower()
        assert "low" in lower and "medium" in lower and "high" in lower

    def test_budget_authority_levels(self, skill_content):
        lower = skill_content.lower()
        assert "none" in lower
        assert "influencer" in lower
        assert "decision-maker" in lower

    def test_competitor_user_required(self, skill_content):
        assert "competing solution" in skill_content.lower()

    def test_abandoned_user_required(self, skill_content):
        assert "abandoned" in skill_content.lower()

    def test_diversity_age(self, skill_content):
        assert "age" in skill_content.lower()

    def test_diversity_company_size(self, skill_content):
        assert "company" in skill_content.lower()


class TestStep3Interviews:
    """Verify interview simulation methodology is complete."""

    def test_six_to_seven_exchanges(self, skill_content):
        assert "6-7" in skill_content or "6 to 7" in skill_content.lower()

    def test_topic_current_workflow(self, skill_content):
        assert "current workflow" in skill_content.lower()

    def test_topic_initial_reaction(self, skill_content):
        assert "initial reaction" in skill_content.lower()

    def test_topic_feature_interest(self, skill_content):
        lower = skill_content.lower()
        assert "features interest" in lower or "feature interest" in lower or "which features" in lower

    def test_topic_concerns(self, skill_content):
        assert "concerns" in skill_content.lower()

    def test_topic_willingness_to_pay(self, skill_content):
        lower = skill_content.lower()
        assert "willing" in lower and "pay" in lower

    def test_topic_switching(self, skill_content):
        assert "switch" in skill_content.lower()

    def test_topic_recommendation(self, skill_content):
        assert "recommendation" in skill_content.lower()

    def test_key_quotes_output(self, skill_content):
        assert "key" in skill_content.lower() and "quote" in skill_content.lower()

    def test_sentiment_output(self, skill_content):
        assert "sentiment" in skill_content.lower()

    def test_would_adopt_output(self, skill_content):
        assert "adopt" in skill_content.lower()

    def test_skeptics_push_back(self, skill_content):
        assert "push back" in skill_content.lower()

    def test_enthusiasts_still_have_concerns(self, skill_content):
        lower = skill_content.lower()
        assert "enthusiast" in lower and "concern" in lower

    def test_anchor_pricing(self, skill_content):
        assert "anchor" in skill_content.lower() and "pay" in skill_content.lower()


class TestStep4Analysis:
    """Verify feedback analysis methodology is complete."""

    def test_themes(self, skill_content):
        assert "theme" in skill_content.lower()

    def test_frequency_counting(self, skill_content):
        assert "frequency" in skill_content.lower()

    def test_pain_points_ranked(self, skill_content):
        assert "pain point" in skill_content.lower()

    def test_feature_requests(self, skill_content):
        assert "feature request" in skill_content.lower()

    def test_adoption_barriers(self, skill_content):
        assert "adoption barrier" in skill_content.lower()

    def test_wtp_signals(self, skill_content):
        lower = skill_content.lower()
        assert "willingness" in lower and "pay" in lower

    def test_segment_interest(self, skill_content):
        assert "segment" in skill_content.lower()

    def test_sentiment_distribution(self, skill_content):
        assert "sentiment distribution" in skill_content.lower()

    def test_surprising_findings(self, skill_content):
        assert "surprising" in skill_content.lower()


class TestStep5Scoring:
    """Verify the scoring framework is complete and accurate."""

    DIMENSIONS = [
        "problem validity",
        "solution fit",
        "market demand",
        "competitive position",
        "monetization potential",
    ]

    def test_all_five_dimensions_present(self, skill_content):
        lower = skill_content.lower()
        for dim in self.DIMENSIONS:
            assert dim in lower, f"Missing scoring dimension: {dim}"

    def test_scale_1_to_10(self, skill_content):
        assert "1-10" in skill_content or "1 to 10" in skill_content.lower()

    def test_verdict_strong(self, skill_content):
        assert "7.5" in skill_content
        assert "strong opportunity" in skill_content.lower()

    def test_verdict_promising(self, skill_content):
        assert "5.5" in skill_content
        assert "promising" in skill_content.lower()

    def test_verdict_concerns(self, skill_content):
        assert "3.5" in skill_content
        assert "significant concerns" in skill_content.lower()

    def test_verdict_reconsider(self, skill_content):
        assert "reconsider" in skill_content.lower()

    def test_score_anchor_strong(self, skill_content):
        assert "8+" in skill_content or "8 +" in skill_content

    def test_score_anchor_moderate(self, skill_content):
        assert "4-5" in skill_content

    def test_score_anchor_weak(self, skill_content):
        assert "<3" in skill_content


class TestStep5ReportStructure:
    """Verify the report format instructions are complete."""

    REQUIRED_SECTIONS = [
        "executive summary",
        "overall score",
        "key findings",
        "audience segmentation",
        "risks",
        "recommendations",
        "appendix",
    ]

    def test_all_report_sections_specified(self, skill_content):
        lower = skill_content.lower()
        for section in self.REQUIRED_SECTIONS:
            assert section in lower, f"Missing report section: {section}"

    def test_breakdown_table(self, skill_content):
        assert "breakdown" in skill_content.lower()

    def test_interview_summaries_in_appendix(self, skill_content):
        lower = skill_content.lower()
        assert "appendix" in lower and "interview" in lower


class TestStep5Output:
    """Verify file output instructions are present."""

    def test_outputs_directory(self, skill_content):
        assert "outputs/" in skill_content or "outputs\\" in skill_content

    def test_date_in_filename(self, skill_content):
        assert "date" in skill_content.lower()

    def test_slug_in_filename(self, skill_content):
        assert "slug" in skill_content.lower()

    def test_markdown_file_extension(self, skill_content):
        assert ".md" in skill_content

    def test_write_tool_instruction(self, skill_content):
        lower = skill_content.lower()
        assert "write" in lower

    def test_summary_to_conversation(self, skill_content):
        lower = skill_content.lower()
        assert "summary" in lower or "print" in lower


class TestInputHandling:
    """Verify the skill handles all input types: inline text, file, and directory."""

    def test_file_extension_detection_docs(self, skill_content):
        assert ".txt" in skill_content and ".md" in skill_content

    def test_file_extension_detection_code(self, skill_content):
        lower = skill_content.lower()
        assert ".py" in lower and ".js" in lower and ".ts" in lower

    def test_read_instruction(self, skill_content):
        lower = skill_content.lower()
        assert "read" in lower

    def test_directory_input_supported(self, skill_content):
        lower = skill_content.lower()
        assert "directory" in lower or "folder" in lower

    def test_directory_lists_files(self, skill_content):
        lower = skill_content.lower()
        assert "glob" in lower or "list" in lower

    def test_directory_reads_code_files(self, skill_content):
        lower = skill_content.lower()
        assert ".py" in lower and ".json" in lower

    def test_directory_reads_office_files(self, skill_content):
        lower = skill_content.lower()
        assert ".docx" in lower and ".pptx" in lower and ".xlsx" in lower

    def test_directory_reads_pdfs(self, skill_content):
        assert ".pdf" in skill_content.lower()

    def test_directory_excludes_node_modules(self, skill_content):
        assert "node_modules" in skill_content

    def test_three_input_modes(self, skill_content):
        lower = skill_content.lower()
        assert "directory" in lower or "folder" in lower
        assert "file" in lower
        assert "inline" in lower or "text" in lower
