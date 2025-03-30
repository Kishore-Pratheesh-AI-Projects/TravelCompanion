"""
Agents package for the travel planner application.
"""

from agents.agent_factory import create_web_research_agent, create_travel_agent, create_reporter_agent
from agents.agent_tasks import (
    research_destination, 
    research_events, 
    research_weather, 
    search_flights, 
    write_travel_report
)

__all__ = [
    'create_web_research_agent',
    'create_travel_agent',
    'create_reporter_agent',
    'research_destination',
    'research_events',
    'research_weather',
    'search_flights',
    'write_travel_report'
]