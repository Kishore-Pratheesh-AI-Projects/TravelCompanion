"""
Task-specific functions for agents to perform.
"""

import traceback
from typing import Optional

def research_destination(agent, destination: str, interests: str) -> str:
    """
    Research destination with enhanced image handling
    
    Args:
        agent: The web research agent
        destination (str): The destination to research
        interests (str): Specific interests to focus on
        
    Returns:
        str: Detailed report about the destination
    """
    try:
        prompt = (
            f"Research {destination} with a focus on {interests}. Follow these steps one at a time:\n"
            f"1. First, find general information about {destination} using Wikipedia search\n"
            f"2. After you have the general information, search for 2-3 images of key attractions separately\n"
            f"3. Then, search specifically for {interests}-related attractions\n"
            f"4. Finally, compile everything into a comprehensive report with:\n"
            f"   - 2-3 high-quality images with proper URLs (format: ![Description](https://full-image-url))\n"
            f"   - A brief caption for each image\n"
            f"   - Images placed naturally throughout the relevant content\n"
            f"   - Information organized in sections with proper headings\n"
            f"   - Details about {interests}-related attractions\n"
            f"   - Practical visitor information\n"
            f"Format your final answer in clean markdown"
        )

        response = agent.chat(prompt)
        return response.response

    except ValueError as e:
        # Handle specific known errors
        if "max iterations" in str(e).lower():
            # Try a simpler approach with fewer requirements
            try:
                fallback_prompt = (
                    f"Create a simple report about {destination} related to {interests}. "
                    f"Include basic information and 1 image if possible."
                )
                fallback_response = agent.chat(fallback_prompt)
                return fallback_response.response
            except Exception:
                return f"# {destination} Report\n\nUnable to generate a detailed report at this time. Please try again later with a more specific request or check your internet connection."

        # Handle other ValueError cases
        return f"# Error Researching {destination}\n\nUnable to complete research: {str(e)}\n\nPlease try again with a different destination or interests."

    except Exception as e:
        # Catch-all for any other unexpected errors
        error_message = f"# Unexpected Error\n\nAn unexpected error occurred while researching {destination}: {str(e)}"
        error_message += f"\n\n```\n{traceback.format_exc()}\n```"
        return error_message


def research_events(agent, destination: str, dates: str, interests: str) -> str:
    """
    Research events with enhanced image handling
    
    Args:
        agent: The web research agent
        destination (str): The destination to research events for
        dates (str): The date range for the events
        interests (str): Specific interests to focus on
        
    Returns:
        str: Detailed report about events at the destination
    """
    try:
        prompt = (
            f"Research events in {destination} during {dates} that match these interests: {interests}.\n\n"
            f"IMPORTANT: Use the browse_webpage tool to visit websites found in search results "
            f"to get detailed event information. Don't just rely on search snippets.\n\n"
            f"For each event, include:\n"
            f"- Event name\n"
            f"- Date and time\n"
            f"- Venue/location\n"
            f"- Ticket information (if applicable)\n"
            f"- A short description of the event\n"
            f"- Format event images as: ![Event Name](https://full-image-url)\n"
            f"- Format images as: ![Description](https://full-image-url)\n"
            f"- Ensure images are full URLs starting with http:// or https://\n"
            f"- Information is accurate and up-to-date\n"
            f"- Place images naturally throughout the content where relevant\n"
            f"- Format the entire response in clean markdown"
        )

        response = agent.chat(prompt)
        return response.response
    except Exception as e:
        error_message = f"# Error Researching Events\n\nUnable to complete event research: {str(e)}"
        return error_message


def research_weather(agent, destination: str, dates: str) -> str:
    """
    Research weather information
    
    Args:
        agent: The travel agent
        destination (str): The destination to research weather for
        dates (str): The date range for the weather forecast
        
    Returns:
        str: Weather report for the destination
    """
    try:
        prompt = (
            f"Provide detailed weather information for {destination} during {dates} including:\n"
            f"1. Temperature ranges\n"
            f"2. Precipitation chances\n"
            f"3. General weather patterns\n"
            f"4. Recommended clothing/gear\n"
            f"Format your response in clean markdown with clear sections."
        )

        response = agent.chat(prompt)
        return response.response
    except Exception as e:
        error_message = f"# Error Researching Weather\n\nUnable to complete weather research: {str(e)}"
        return error_message


def search_flights(agent, current_location: str, destination: str, dates: str) -> str:
    """
    Search flight options
    
    Args:
        agent: The travel agent
        current_location (str): The departure location
        destination (str): The destination
        dates (str): The date range for the flights
        
    Returns:
        str: Flight options report
    """
    try:
        prompt = (
            f"Find top 3 affordable and convenient flight options from {current_location} to {destination} on {dates}.\n"
            f"Provide concise bullet-point information for each option including airline, departure/arrival times, price, and any notable features."
        )

        response = agent.chat(prompt)
        return response.response
    except Exception as e:
        error_message = f"# Error Searching Flights\n\nUnable to complete flight search: {str(e)}"
        return error_message


def write_travel_report(
    agent, 
    destination_report: str, 
    events_report: str, 
    weather_report: str, 
    flight_report: str
) -> str:
    """
    Create final travel report
    
    Args:
        agent: The reporter agent
        destination_report (str): Research about the destination
        events_report (str): Information about events
        weather_report (str): Weather forecast
        flight_report (str): Flight options
        
    Returns:
        str: Comprehensive travel report
    """
    try:
        prompt = (
            "Create a comprehensive travel report that:\n"
            "1. Maintains all images from the destination and events reports\n"
            "2. Organizes information in a clear, logical structure\n"
            "3. Keeps all markdown formatting intact\n"
            "4. Ensures images are properly displayed with captions\n"
            "5. Includes all key information from each section\n\n"
            f"Here are the sections to combine:\n\n"
            f"DESTINATION REPORT:\n{destination_report}\n\n"
            f"EVENTS REPORT:\n{events_report}\n\n"
            f"WEATHER REPORT:\n{weather_report}\n\n"
            f"FLIGHT REPORT:\n{flight_report}"
        )

        response = agent.chat(prompt)
        return response.response
    except Exception as e:
        error_message = f"# Error Creating Travel Report\n\nUnable to compile travel report: {str(e)}"
        return error_message