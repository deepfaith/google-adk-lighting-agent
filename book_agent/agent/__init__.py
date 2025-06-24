# This file makes book_agent/agent a module
# Import and expose the root_agent at this level
from book_agent.agent.writing_agent import BookWritingAgent, root_agent

# Ensure root_agent is accessible directly from this module
__all__ = ['BookWritingAgent', 'root_agent']