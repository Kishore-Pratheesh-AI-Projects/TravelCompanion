"""
Agent factory module for creating different types of agents.
"""
import os
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer

# Import tools
from tools.search_tool import (
    serper_search,
    wikipedia_search_articles, 
    wikipedia_search_images,
    browse_webpage
)
from tools.travel_tool import (
    get_weather_data,
    search_flights
)

def create_web_research_agent():
    """
    Create a web research agent with appropriate tools.
    
    Returns:
        ReActAgent: An agent configured for web research tasks
    """
    # Create tool instances
    web_search_tool = FunctionTool.from_defaults(
        fn=serper_search,
        name="serper_search",
        description="Search the web for information"
    )
    
    wiki_articles_tool = FunctionTool.from_defaults(
        fn=wikipedia_search_articles,
        name="wikipedia_search_articles",
        description="Search Wikipedia articles for information"
    )
    
    wiki_images_tool = FunctionTool.from_defaults(
        fn=wikipedia_search_images,
        name="wikipedia_search_images",
        description="Search Wikipedia for images related to a topic"
    )
    
    web_browse_tool = FunctionTool.from_defaults(
        fn=browse_webpage,
        name="browse_webpage",
        description="Browse a webpage and extract its content"
    )
    
    # Combine tools
    web_tools = [web_search_tool, wiki_articles_tool, wiki_images_tool, web_browse_tool]

    # Create memory for the agent
    memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

    # Create the agent with format instructions
    agent = ReActAgent.from_tools(
        web_tools,
        llm=OpenAI(model="gpt-4o", temperature=0.2),
        memory=memory,
        verbose=True,
        system_prompt=(
            "You are a Web Research Agent. Your goal is to research destinations and find relevant images. "
            "You are diligent, thorough, comprehensive, and visual-focused. "
            "Always provide detailed information and relevant images when available.\n\n"
            "IMPORTANT: You have the ability to browse webpages using the browse_webpage tool. "
            "After finding URLs with serper_search, you should use browse_webpage to visit those URLs "
            "and extract detailed information. Don't just rely on search snippets.\n\n"
            "You must strictly follow this format when reasoning:\n"
            "1. Start with 'Thought: ' followed by a single reasoning step\n"
            "2. Then write 'Action: ' followed by exactly one tool name\n"
            "3. Then write 'Action Input: ' followed by the input parameters for that tool\n"
            "4. Wait for the observation before taking another step\n"
            "5. Never chain multiple thoughts together without taking an action in between\n"
            "6. After observations, start a new thought\n"
            "7. When you have all the information, provide your final answer after a 'Thought: ' step"
        ),
        max_iterations=50
    )

    return agent

def create_travel_agent():
    """
    Create a travel agent with appropriate tools.
    
    Returns:
        ReActAgent: An agent configured for travel planning tasks
    """
    # Create tool instances
    flight_tool = FunctionTool.from_defaults(
        fn=search_flights,
        name="search_flights",
        description="Search for flights between locations"
    )
    
    weather_tool = FunctionTool.from_defaults(
        fn=get_weather_data,
        name="get_weather_data",
        description="Get weather information for a location"
    )
    
    web_search_tool = FunctionTool.from_defaults(
        fn=serper_search,
        name="web_search_tool",
        description="Search the web for travel information"
    )
    
    web_browse_tool = FunctionTool.from_defaults(
        fn=browse_webpage,
        name="web_browse_tool",
        description="Browse a webpage and extract travel information"
    )
    
    # Combine tools
    travel_tools = [flight_tool, weather_tool, web_search_tool, web_browse_tool]
    
    # Create memory for the agent
    memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
    
    # Create the agent
    agent = ReActAgent.from_tools(
        travel_tools,
        llm=OpenAI(model="gpt-4o", temperature=0.2),
        memory=memory,
        verbose=True,
        system_prompt=(
            "You are a Travel Agent. Your goal is to assist travelers with their queries. "
            "You are friendly, hardworking, and detailed in reporting back to users. "
            "Provide specific and actionable information about flights, weather, and travel logistics.\n\n"
            "IMPORTANT: You have access to tools that can search for flights, check weather information, "
            "perform web searches, and browse webpages. After finding URLs with web_search_tool, "
            "you should use web_browse_tool to visit those URLs and extract detailed information "
            "such as hotel prices, tour details, local transportation options, and more. "
            "Always verify information with multiple sources when possible.\n\n"
            "You must strictly follow this format when reasoning:\n"
            "1. Start with 'Thought: ' followed by a single reasoning step\n"
            "2. Then write 'Action: ' followed by exactly one tool name\n"
            "3. Then write 'Action Input: ' followed by the input parameters for that tool\n"
            "4. Wait for the observation before taking another step\n"
            "5. Never chain multiple thoughts together without taking an action in between\n"
            "6. After observations, start a new thought\n"
            "7. When you have all the information, provide your final answer after a 'Thought: ' step"
        ),
        max_iterations=30
    )
    
    return agent

def create_reporter_agent():
    """
    Create a reporter agent for final travel reports.
    
    Returns:
        ReActAgent: An agent configured for creating travel reports
    """
    # Create memory for the agent
    memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
    
    # Create the agent
    agent = ReActAgent.from_tools(
        [],  # No tools needed for this agent
        llm=OpenAI(model="gpt-4o", temperature=0.2),
        memory=memory,
        verbose=True,
        system_prompt=(
            "You are a Travel Report Agent. Your goal is to write comprehensive travel reports with visual elements. "
            "You are friendly, hardworking, visual-oriented, and detailed in reporting. "
            "Create well-structured, informative, and visually appealing travel reports.\n\n"
            "IMPORTANT: Your primary task is to compile information from various sources into a cohesive, "
            "engaging travel report. You should preserve all formatting, especially image URLs and markdown "
            "elements. Organize information logically with clear section headings and maintain a consistent "
            "style throughout the document.\n\n"
            "You must strictly follow this format when reasoning:\n"
            "1. Start with 'Thought: ' followed by a single reasoning step\n"
            "2. Analyze the information provided to you systematically\n"
            "3. Wait for any additional input before proceeding\n"
            "4. After analyzing all information, provide your final report after a 'Thought: ' step\n"
            "5. Ensure the final report maintains all image references and markdown formatting"
        ),
        max_iterations=20
    )
    
    return agent