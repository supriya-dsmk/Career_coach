"""
Custom tools for the AI Career Coach multi-agent system.
These tools allow agents to parse feedback data and match skills to learning resources.
"""

import json
from crewai.tools import tool


def _load_feedback_data(filepath: str = "sample_data/feedback_360.json") -> dict:
    """Load the 360-degree feedback JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@tool("Parse Feedback Data")
def parse_feedback_data(section: str = "all") -> str:
    """
    Parse and extract structured feedback data from the 360-degree review.
    Use section parameter to get specific parts:
    - 'all': Complete feedback data
    - 'manager': Manager review only
    - 'peers': Peer reviews only
    - 'reports': Direct report reviews only
    - 'self': Self-assessment only
    - 'employee': Employee profile info
    - 'ratings': Aggregated ratings across all reviewers
    """
    data = _load_feedback_data()

    if section == "manager":
        return json.dumps(data["manager_review"], indent=2)
    elif section == "peers":
        return json.dumps(data["peer_reviews"], indent=2)
    elif section == "reports":
        return json.dumps(data["direct_report_reviews"], indent=2)
    elif section == "self":
        return json.dumps(data["self_assessment"], indent=2)
    elif section == "employee":
        return json.dumps(data["employee"], indent=2)
    elif section == "ratings":
        return _aggregate_ratings(data)
    else:
        return json.dumps(data, indent=2)


def _aggregate_ratings(data: dict) -> str:
    """Aggregate ratings across all reviewers into averages."""
    all_ratings = {}

    # Manager ratings
    for skill, score in data["manager_review"]["ratings"].items():
        all_ratings.setdefault(skill, []).append(score)

    # Peer ratings
    for peer in data["peer_reviews"]:
        for skill, score in peer["ratings"].items():
            all_ratings.setdefault(skill, []).append(score)

    # Direct report ratings
    for report in data["direct_report_reviews"]:
        for skill, score in report["ratings"].items():
            all_ratings.setdefault(skill, []).append(score)

    aggregated = {
        skill: round(sum(scores) / len(scores), 2)
        for skill, scores in all_ratings.items()
    }
    aggregated_sorted = dict(sorted(aggregated.items(), key=lambda x: x[1]))

    result = {
        "aggregated_ratings": aggregated_sorted,
        "lowest_rated": list(aggregated_sorted.keys())[:3],
        "highest_rated": list(aggregated_sorted.keys())[-3:],
    }
    return json.dumps(result, indent=2)


@tool("Match Skills to Learning Resources")
def match_learning_resources(skills: str) -> str:
    """
    Given a comma-separated list of skills or development areas,
    find matching learning resources from the company catalog.
    Example input: 'communication, leadership, delegation'
    Returns matched resources with details.
    """
    data = _load_feedback_data()
    catalog = data.get("learning_resources_catalog", [])
    target_skills = [s.strip().lower() for s in skills.split(",")]

    matched = []
    for resource in catalog:
        resource_skills = [s.lower() for s in resource["skills"]]
        overlap = set(target_skills) & set(resource_skills)
        if overlap:
            matched.append({
                "id": resource["id"],
                "title": resource["title"],
                "type": resource["type"],
                "provider": resource["provider"],
                "duration_hours": resource["duration_hours"],
                "format": resource["format"],
                "cost": resource["cost"],
                "matching_skills": list(overlap),
                "all_skills": resource["skills"],
            })

    matched.sort(key=lambda x: len(x["matching_skills"]), reverse=True)

    return json.dumps({
        "query_skills": target_skills,
        "total_matches": len(matched),
        "resources": matched,
    }, indent=2)
