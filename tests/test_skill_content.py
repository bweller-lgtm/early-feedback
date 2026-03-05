"""Tests that the SKILL.md skill file contains all required methodology.

These tests ensure that any edits to the skill preserve the complete
evaluation framework -- scoring, persona diversity, interview coverage,
honesty guardrails, report structure, and output instructions.
"""

import pytest
from conftest import SKILL_PATH, LEGACY_SKILL_PATH


class TestSkillFileExists:
    def test_skill_file_exists(self):
        assert SKILL_PATH.exists(), f"Skill file missing: {SKILL_PATH}"

    def test_skill_file_not_empty(self, skill_content):
        assert len(skill_content.strip()) > 500, "Skill file appears too short"

    def test_arguments_placeholder(self, skill_content):
        assert "$ARGUMENTS" in skill_content, "Must reference $ARGUMENTS for user input"

    def test_legacy_command_exists(self):
        assert LEGACY_SKILL_PATH.exists(), (
            f"Legacy command file missing: {LEGACY_SKILL_PATH} "
            "(keeps /evaluate working in Claude Code without plugin install)"
        )


class TestSkillMdFrontmatter:
    """Verify SKILL.md has valid Agent Skills frontmatter."""

    def test_starts_with_frontmatter(self, skill_content):
        assert skill_content.strip().startswith("---"), "SKILL.md must start with YAML frontmatter"

    def test_has_closing_frontmatter(self, skill_content):
        parts = skill_content.strip().split("---", 2)
        assert len(parts) >= 3, "SKILL.md must have opening and closing --- for frontmatter"

    def test_name_field(self, skill_content):
        frontmatter = skill_content.split("---")[1]
        assert "name:" in frontmatter
        assert "evaluate" in frontmatter.lower()

    def test_name_matches_directory(self, skill_content):
        """Per Agent Skills spec, name must match parent directory."""
        frontmatter = skill_content.split("---")[1]
        import re
        match = re.search(r"name:\s*(\S+)", frontmatter)
        assert match, "name field not found in frontmatter"
        assert match.group(1) == "evaluate", "name must be 'evaluate' to match parent directory"
        assert SKILL_PATH.parent.name == "evaluate", "Parent directory must be named 'evaluate'"

    def test_description_field(self, skill_content):
        frontmatter = skill_content.split("---")[1]
        assert "description:" in frontmatter

    def test_description_not_empty(self, skill_content):
        frontmatter = skill_content.split("---")[1]
        # Description should be substantive (>50 chars after the key)
        assert "description:" in frontmatter
        desc_start = frontmatter.index("description:")
        desc_section = frontmatter[desc_start:desc_start + 200]
        assert len(desc_section) > 60, "Description should be substantive"

    def test_metadata_version(self, skill_content):
        frontmatter = skill_content.split("---")[1]
        assert "version:" in frontmatter

    def test_metadata_author(self, skill_content):
        frontmatter = skill_content.split("---")[1]
        assert "author:" in frontmatter

    def test_compatibility_field(self, skill_content):
        frontmatter = skill_content.split("---")[1]
        assert "compatibility:" in frontmatter


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

    def test_information_gaps(self, skill_content):
        lower = skill_content.lower()
        assert "information gaps" in lower, "Must flag missing information instead of inferring"


class TestStep2Personas:
    """Verify persona generation methodology is complete."""

    def test_default_eight_personas(self, skill_content):
        lower = skill_content.lower()
        assert "default 8" in lower or ("8" in skill_content and "4-12" in skill_content)

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


class TestStep2OrganicSentiment:
    """Verify persona sentiment is organic, not forced."""

    def test_no_forced_distribution(self, skill_content):
        """The skill should NOT contain a forced ratio like '2 skeptics, 3 neutral'."""
        lower = skill_content.lower()
        assert "2 skeptic" not in lower, "Should not force skeptic count"
        assert "3 neutral" not in lower, "Should not force neutral count"
        assert "3 enthusiastic" not in lower, "Should not force enthusiastic count"

    def test_organic_sentiment_instruction(self, skill_content):
        """The skill should instruct organic/authentic/honest sentiment."""
        lower = skill_content.lower()
        assert any(word in lower for word in ["organic", "honest", "authentic", "natural"])

    def test_sentiment_emerges_from_product(self, skill_content):
        """Sentiment should depend on the product, not be predetermined."""
        lower = skill_content.lower()
        assert any(phrase in lower for phrase in ["emerge", "naturally", "honest reaction", "honest first reaction", "actual merit"])

    def test_still_labels_sentiment(self, skill_content):
        """Personas should still be labeled skeptic/neutral/enthusiastic."""
        lower = skill_content.lower()
        assert "skeptic" in lower
        assert "neutral" in lower
        assert "enthusiastic" in lower

    def test_weak_idea_produces_skeptics(self, skill_content):
        """A bad idea should yield more skeptics."""
        lower = skill_content.lower()
        assert any(word in lower for word in ["weak", "poorly targeted"])


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

    def test_anchor_pricing(self, skill_content):
        assert "anchor" in skill_content.lower() and "pay" in skill_content.lower()


class TestAdaptiveInterviews:
    """Verify interviews adapt to product type, not just fixed questions."""

    def test_product_specific_questions(self, skill_content):
        lower = skill_content.lower()
        assert "specific" in lower and ("product" in lower or "context" in lower)

    def test_marketplace_questions(self, skill_content):
        lower = skill_content.lower()
        assert "marketplace" in lower and ("chicken-and-egg" in lower or "supply-side" in lower or "supply" in lower)

    def test_regulated_industry_questions(self, skill_content):
        lower = skill_content.lower()
        assert "regulated" in lower and ("compliance" in lower or "regulatory" in lower)


class TestHonestyGuardrails:
    """Verify the skill enforces honest, unbiased evaluation."""

    def test_no_charitable_inference(self, skill_content):
        """Should flag gaps instead of making optimistic assumptions."""
        lower = skill_content.lower()
        assert "do not fill gaps" in lower or "flag it as unknown" in lower

    def test_symmetric_hedging(self, skill_content):
        """Skeptics acknowledge strengths AND enthusiasts voice concerns."""
        lower = skill_content.lower()
        assert "skeptic" in lower and "strength" in lower
        assert "enthusiast" in lower and "concern" in lower

    def test_experts_must_disagree(self, skill_content):
        """Experts should disagree where domains conflict."""
        lower = skill_content.lower()
        assert "disagree" in lower

    def test_use_full_scoring_scale(self, skill_content):
        """Should not cluster in the 5-7 range."""
        lower = skill_content.lower()
        assert "full" in lower and "scale" in lower
        assert any(phrase in lower for phrase in ["do not cluster", "full 1-10", "full scale"])

    def test_blunt_verdict_instruction(self, skill_content):
        """Truth over encouragement."""
        lower = skill_content.lower()
        assert "truth" in lower and ("encourage" in lower or "founder" in lower)

    def test_product_specific_critical_dimensions(self, skill_content):
        """Should identify the most critical dimensions for this specific product."""
        lower = skill_content.lower()
        assert "most critical" in lower or "1-2 dimensions" in lower

    def test_information_gaps_flagged(self, skill_content):
        """Missing info should be flagged, not filled in."""
        lower = skill_content.lower()
        assert "information gaps" in lower


class TestViabilityGate:
    """Verify the viability gate after interviews."""

    def test_viability_gate_exists(self, skill_content):
        lower = skill_content.lower()
        assert "viability gate" in lower or "viability" in lower

    def test_early_termination_on_rejection(self, skill_content):
        lower = skill_content.lower()
        assert "early termination" in lower or "critical issues report" in lower

    def test_critical_issues_report(self, skill_content):
        lower = skill_content.lower()
        assert "critical" in lower and ("issues" in lower or "report" in lower)

    def test_full_flag_overrides(self, skill_content):
        assert "--full" in skill_content


class TestStep4ExpertPanel:
    """Verify expert panel review methodology is complete."""

    def test_default_three_experts(self, skill_content):
        lower = skill_content.lower()
        assert "default 3" in lower or ("3" in skill_content and "1-5" in skill_content)

    def test_experts_selected_by_context(self, skill_content):
        lower = skill_content.lower()
        assert "product" in lower and ("context" in lower or "domain" in lower)

    def test_experts_critique_questions(self, skill_content):
        lower = skill_content.lower()
        assert "critique" in lower or "evaluate" in lower or "review" in lower

    def test_experts_suggest_followups(self, skill_content):
        lower = skill_content.lower()
        assert "follow-up" in lower or "followup" in lower or "follow up" in lower

    def test_expert_credentials(self, skill_content):
        lower = skill_content.lower()
        assert "credential" in lower or "expertise" in lower

    def test_expert_examples_by_product_type(self, skill_content):
        lower = skill_content.lower()
        assert "marketplace" in lower and "b2b" in lower.replace("b2b_saas", "b2b")

    def test_experts_identify_gaps(self, skill_content):
        lower = skill_content.lower()
        assert "gap" in lower or "missed" in lower or "surface-level" in lower

    def test_experts_can_be_skipped(self, skill_content):
        assert "--no-experts" in skill_content


class TestStep5FollowupInterviews:
    """Verify follow-up interview methodology is complete."""

    def test_followup_from_experts(self, skill_content):
        lower = skill_content.lower()
        assert "follow-up" in lower and "expert" in lower

    def test_followup_in_character(self, skill_content):
        lower = skill_content.lower()
        assert "in character" in lower or "character" in lower

    def test_followup_informed_by_round_1(self, skill_content):
        lower = skill_content.lower()
        assert "round 1" in lower or "initial interview" in lower or "step 3" in lower

    def test_followup_attributed_to_expert(self, skill_content):
        lower = skill_content.lower()
        assert "attribute" in lower or "expert who" in lower


class TestStep6ExpertSynthesis:
    """Verify expert synthesis and feedback analysis methodology."""

    def test_expert_assessment(self, skill_content):
        lower = skill_content.lower()
        assert "assessment" in lower and "expert" in lower

    def test_expert_domain_evaluation(self, skill_content):
        lower = skill_content.lower()
        assert "domain" in lower and ("evaluation" in lower or "specific" in lower)

    def test_expert_recommendation(self, skill_content):
        lower = skill_content.lower()
        assert "recommendation" in lower

    def test_expert_references_interviews(self, skill_content):
        lower = skill_content.lower()
        assert "reference" in lower or "interview response" in lower


class TestStep6Analysis:
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

    def test_combined_interview_data(self, skill_content):
        lower = skill_content.lower()
        assert "initial" in lower and "follow-up" in lower


class TestStep7Scoring:
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
        assert "<4" in skill_content

    def test_expanded_scoring_table(self, skill_content):
        """Scoring table should include 6-7 range, not just 8+/4-5/<3."""
        assert "6-7" in skill_content


class TestStep7ReportStructure:
    """Verify the report format instructions are complete."""

    REQUIRED_SECTIONS = [
        "executive summary",
        "overall score",
        "key findings",
        "expert assessments",
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

    def test_interview_transcripts_in_appendix(self, skill_content):
        lower = skill_content.lower()
        assert "appendix" in lower and "interview" in lower

    def test_full_qa_dialogue_required(self, skill_content):
        lower = skill_content.lower()
        assert "transcript" in lower or "dialogue" in lower or "q&a" in lower

    def test_expert_assessments_in_report(self, skill_content):
        lower = skill_content.lower()
        assert "expert assessments" in lower


class TestStep7Output:
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


class TestConfigParsing:
    """Verify the skill reads and applies configuration."""

    def test_mentions_config_file(self, skill_content):
        assert "evaluate.config.yaml" in skill_content

    def test_config_is_optional(self, skill_content):
        lower = skill_content.lower()
        assert "without" in lower or "no config" in lower or "if no config" in lower

    def test_yaml_format(self, skill_content):
        lower = skill_content.lower()
        assert "yaml" in lower

    def test_experts_count_configurable(self, skill_content):
        lower = skill_content.lower()
        assert "experts" in lower and "count" in lower

    def test_personas_count_configurable(self, skill_content):
        lower = skill_content.lower()
        assert "personas" in lower and "count" in lower

    def test_web_research_config(self, skill_content):
        assert "web_research" in skill_content or "web research" in skill_content.lower()

    def test_deep_report_config(self, skill_content):
        assert "deep_report" in skill_content or "deep report" in skill_content.lower()

    def test_additional_dimensions_config(self, skill_content):
        lower = skill_content.lower()
        assert "additional" in lower and "dimension" in lower

    def test_required_questions_config(self, skill_content):
        assert "required_questions" in skill_content or "required questions" in skill_content.lower()

    def test_must_include_personas_config(self, skill_content):
        assert "must_include" in skill_content or "must include" in skill_content.lower()


class TestInlineFlags:
    """Verify the skill parses inline flags from $ARGUMENTS."""

    def test_experts_flag(self, skill_content):
        assert "--experts" in skill_content

    def test_deep_flag(self, skill_content):
        assert "--deep" in skill_content

    def test_web_search_flag(self, skill_content):
        assert "--web-search" in skill_content

    def test_no_experts_flag(self, skill_content):
        assert "--no-experts" in skill_content

    def test_personas_flag(self, skill_content):
        assert "--personas" in skill_content

    def test_questions_flag(self, skill_content):
        assert "--questions" in skill_content

    def test_config_flag(self, skill_content):
        assert "--config" in skill_content

    def test_full_flag(self, skill_content):
        assert "--full" in skill_content

    def test_flags_override_config(self, skill_content):
        lower = skill_content.lower()
        assert "override" in lower


class TestWebResearch:
    """Verify the conditional web research step."""

    def test_web_research_step_exists(self, skill_content):
        lower = skill_content.lower()
        assert "web research" in lower

    def test_web_research_is_conditional(self, skill_content):
        lower = skill_content.lower()
        assert "skip" in lower and "web research" in lower

    def test_searches_competitors(self, skill_content):
        lower = skill_content.lower()
        assert "competitor" in lower and "search" in lower

    def test_market_context_brief(self, skill_content):
        lower = skill_content.lower()
        assert "market context brief" in lower

    def test_websearch_tool_mentioned(self, skill_content):
        assert "WebSearch" in skill_content


class TestDeepReport:
    """Verify the conditional deep research report."""

    def test_deep_report_step_exists(self, skill_content):
        lower = skill_content.lower()
        assert "deep research report" in lower or "deep-dive" in lower

    def test_deep_report_is_conditional(self, skill_content):
        lower = skill_content.lower()
        assert "skip" in lower and "deep" in lower

    def test_market_sizing_section(self, skill_content):
        lower = skill_content.lower()
        assert "market sizing" in lower or "tam" in lower

    def test_competitive_landscape_section(self, skill_content):
        lower = skill_content.lower()
        assert "competitive landscape" in lower

    def test_regulatory_section(self, skill_content):
        lower = skill_content.lower()
        assert "regulatory" in lower

    def test_technical_feasibility_section(self, skill_content):
        lower = skill_content.lower()
        assert "technical feasibility" in lower

    def test_go_to_market_section(self, skill_content):
        lower = skill_content.lower()
        assert "go-to-market" in lower or "go to market" in lower

    def test_key_experiments_section(self, skill_content):
        lower = skill_content.lower()
        assert "experiment" in lower

    def test_separate_output_file(self, skill_content):
        assert "deep-research.md" in skill_content


class TestExternalFiles:
    """Verify support for optional external files."""

    def test_experts_md_support(self, skill_content):
        assert "experts.md" in skill_content

    def test_questions_md_support(self, skill_content):
        assert "questions.md" in skill_content

    def test_context_md_support(self, skill_content):
        assert "context.md" in skill_content

    def test_files_are_optional(self, skill_content):
        lower = skill_content.lower()
        assert "optional" in lower

    def test_checks_file_existence(self, skill_content):
        assert "test -f" in skill_content


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
