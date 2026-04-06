"""
Task definitions for the AI Career Development & Performance Coach.
Each task represents a stage in the feedback-to-development-plan pipeline.
"""

from crewai import Task, Agent


def create_feedback_analysis_task(agent: Agent) -> Task:
    """Task: Analyze all 360-degree feedback and produce a comprehensive assessment."""
    return Task(
        description=(
            "Analyze the complete 360-degree feedback for the employee. Follow these steps:\n\n"
            "1. First, retrieve the employee profile to understand their role and context.\n"
            "2. Retrieve aggregated ratings to see quantitative scores across all dimensions.\n"
            "3. Review the manager feedback for official performance assessment.\n"
            "4. Review all peer feedback for cross-functional perspectives.\n"
            "5. Review direct report feedback for leadership effectiveness signals.\n"
            "6. Review the self-assessment to understand the employee's own perspective.\n\n"
            "Then synthesize your findings into a structured analysis that includes:\n"
            "- Top 3-5 strengths with supporting evidence from multiple sources\n"
            "- Top 3-5 development gaps with patterns across reviewers\n"
            "- Blind spots (gaps between self-assessment and others' feedback)\n"
            "- Key themes that emerge across all feedback sources\n"
            "- Priority ranking of development areas based on career impact"
        ),
        expected_output=(
            "A detailed feedback analysis report with:\n"
            "1. Employee Overview (name, role, level, career goals)\n"
            "2. Strengths Summary (top strengths with evidence quotes)\n"
            "3. Development Gaps (prioritized list with supporting data)\n"
            "4. Blind Spots Analysis (self vs. others perception gaps)\n"
            "5. Key Themes (recurring patterns across all feedback)\n"
            "6. Priority Development Areas (ranked by impact on career goals)"
        ),
        agent=agent,
    )


def create_learning_recommendation_task(agent: Agent, context: list[Task]) -> Task:
    """Task: Match skill gaps to learning resources and build a learning pathway."""
    return Task(
        description=(
            "Based on the feedback analysis, create a targeted learning pathway:\n\n"
            "1. Take the top priority development areas identified in the feedback analysis.\n"
            "2. For each development area, search for matching learning resources using "
            "relevant skill keywords.\n"
            "3. Curate the best resources for each gap, ensuring a mix of formats "
            "(workshops, courses, books, communities, practice opportunities).\n"
            "4. Consider practical factors: prioritize free/company-sponsored resources, "
            "balance time commitment, and include both quick wins and deeper investments.\n"
            "5. Create a recommended learning pathway that sequences resources logically.\n\n"
            "Important: Search for resources matching these skill areas at minimum:\n"
            "- communication, stakeholder management\n"
            "- leadership, delegation\n"
            "- visibility, influence\n"
            "- mentorship, coaching"
        ),
        expected_output=(
            "A curated learning pathway document with:\n"
            "1. Development Area -> Resource Mapping (which resources address which gaps)\n"
            "2. Recommended Learning Sequence (what to start with and why)\n"
            "3. Resource Details (title, format, duration, cost for each)\n"
            "4. Quick Wins (resources that can show impact within 2 weeks)\n"
            "5. Deep Investments (longer programs for sustained growth)\n"
            "6. Community & Networking opportunities"
        ),
        agent=agent,
        context=context,
    )


def create_development_plan_task(agent: Agent, context: list[Task]) -> Task:
    """Task: Generate a 90-day development plan with measurable milestones."""
    return Task(
        description=(
            "Create a comprehensive 90-day career development plan that brings together "
            "the feedback analysis and learning recommendations:\n\n"
            "1. Define 3-4 SMART development goals aligned with the employee's career "
            "aspirations (Staff Engineer track).\n"
            "2. For each goal, create specific weekly/monthly milestones.\n"
            "3. Map learning resources to specific weeks in the timeline.\n"
            "4. Include on-the-job stretch assignments and practice opportunities.\n"
            "5. Define measurable success criteria for each goal.\n"
            "6. Add accountability checkpoints (manager 1:1 topics, self-reflection prompts).\n"
            "7. Include a 'quick wins' section for the first 2 weeks to build momentum.\n\n"
            "The plan should be practical, not overwhelming - assume the employee has "
            "about 4-5 hours per week for dedicated development activities alongside "
            "their regular work."
        ),
        expected_output=(
            "A complete 90-Day Career Development Plan formatted as:\n\n"
            "## EXECUTIVE SUMMARY\n"
            "Brief overview of focus areas and expected outcomes\n\n"
            "## DEVELOPMENT GOALS (3-4 SMART goals)\n"
            "Each with: Goal statement, success metrics, timeline\n\n"
            "## WEEK-BY-WEEK ROADMAP\n"
            "Weeks 1-2: Quick wins and foundation\n"
            "Weeks 3-6: Core skill building\n"
            "Weeks 7-10: Application and practice\n"
            "Weeks 11-13: Integration and measurement\n\n"
            "## LEARNING RESOURCES SCHEDULE\n"
            "When to start each resource and expected completion\n\n"
            "## STRETCH ASSIGNMENTS\n"
            "On-the-job opportunities to practice new skills\n\n"
            "## ACCOUNTABILITY FRAMEWORK\n"
            "Check-in schedule, reflection prompts, manager discussion topics\n\n"
            "## SUCCESS METRICS\n"
            "How to measure progress at 30, 60, and 90 days"
        ),
        agent=agent,
        context=context,
    )
