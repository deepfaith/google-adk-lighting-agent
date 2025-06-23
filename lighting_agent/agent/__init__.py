# This file makes lighting_agent/agent a module
# Import and expose the root_agent at this level
from lighting_agent.agent.recommendation_agent import LightingRecommendationAgent, root_agent

# Ensure root_agent is accessible directly from this module
__all__ = ['LightingRecommendationAgent', 'root_agent']