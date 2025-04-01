# -*- coding: utf-8 -*-
"""
Main Gradio application for Travel Planner with tabbed interface.
"""

import os
import sys
import gradio as gr
import time
from typing import Dict, Any, List, Optional, Tuple

# Import our configuration
from config import setup_env, APP_SETTINGS

# Import agent modules
from agents.agent_factory import (
    create_web_research_agent,
    create_travel_agent,
    create_reporter_agent
)
from agents.agent_tasks import (
    research_destination,
    research_events,
    research_weather,
    search_flights,
    write_travel_report
)

# Check environment variables
if not setup_env():
    print("Missing required environment variables. Check your .env file.")
    sys.exit(1)

# Global agent instances
web_agent = None
travel_agent = None
reporter_agent = None

def initialize_agents():
    """
    Initialize all the agents needed for the application.
    
    Returns:
        str: Status message
    """
    global web_agent, travel_agent, reporter_agent
    
    try:
        web_agent = create_web_research_agent()
        travel_agent = create_travel_agent()
        reporter_agent = create_reporter_agent()
        return "✅ Agents initialized successfully!"
    except Exception as e:
        return f"❌ Error initializing agents: {str(e)}"

def generate_travel_plan(
    origin: str,
    destination: str,
    travel_dates: str,
    interests: str,
    progress=gr.Progress()
):
    """
    Generate a complete travel plan based on user inputs.
    
    Args:
        origin (str): Departure location
        destination (str): Destination to visit
        travel_dates (str): Date range for the trip
        interests (str): User's interests or preferences
        progress: Gradio progress tracker
        
    Returns:
        tuple: (Status, Reasoning, Travel Plan) as markdown strings
    """
    global web_agent, travel_agent, reporter_agent
    
    # Initialize agents if not already done
    if not web_agent or not travel_agent or not reporter_agent:
        init_status = initialize_agents()
        if "Error" in init_status:
            return init_status, "Agents not initialized properly", ""
    
    # Define progress steps
    total_steps = 5
    current_step = 0
    
    # Create initial status display
    status_display = "# 🔍 Planning Your Trip...\n\n"
    status_display += f"👤 From: **{origin}**\n"
    status_display += f"🌍 To: **{destination}**\n"
    status_display += f"📅 When: **{travel_dates}**\n"
    status_display += f"❤️ Interests: **{interests}**\n\n"
    status_display += "## Current Status:\n"
    
    # Initial reasoning display
    reasoning_display = "## 💭 Planning Process\n\n"
    reasoning_display += "Starting research for your trip...\n"
    
    progress(current_step/total_steps, desc="Starting travel research...")
    progress_messages = []
    
    try:
        # Step 1: Research destination
        current_step += 1
        progress(current_step/total_steps, desc=f"Researching {destination}...")
        progress_messages.append(f"⏳ Researching {destination}...")
        
        status_update = status_display + f"🔄 **Step 1/5:** Researching {destination} tourism information...\n"
        reasoning_update = reasoning_display + f"Gathering information about {destination}...\n"
        yield status_update, reasoning_update, ""
        
        destination_report = research_destination(web_agent, destination, interests)
        progress_messages.append(f"✅ Destination research complete")
        
        status_update = status_display + f"✅ **Step 1/5:** Completed destination research\n"
        reasoning_update = reasoning_display + f"Completed research on {destination} including attractions and points of interest based on your preferences.\n"
        yield status_update, reasoning_update, ""
        
        # Step 2: Research events
        current_step += 1
        progress(current_step/total_steps, desc=f"Finding events in {destination}...")
        progress_messages.append(f"⏳ Finding events in {destination}...")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"🔄 **Step 2/5:** Finding events in {destination} during {travel_dates}...\n"
        reasoning_update = reasoning_display + f"Searching for events and activities in {destination} during {travel_dates}...\n"
        yield status_update, reasoning_update, ""
        
        events_report = research_events(web_agent, destination, travel_dates, interests)
        progress_messages.append(f"✅ Events research complete")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        reasoning_update = reasoning_display + f"Found relevant events and activities taking place during your stay.\n"
        yield status_update, reasoning_update, ""
        
        # Step 3: Research weather
        current_step += 1
        progress(current_step/total_steps, desc="Checking weather conditions...")
        progress_messages.append(f"⏳ Checking weather conditions...")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        status_update += f"🔄 **Step 3/5:** Checking weather forecasts for {destination}...\n"
        reasoning_update = reasoning_display + f"Analyzing typical and forecasted weather conditions for {destination} during {travel_dates}...\n"
        yield status_update, reasoning_update, ""
        
        weather_report = research_weather(travel_agent, destination, travel_dates)
        progress_messages.append(f"✅ Weather research complete")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        status_update += f"✅ **Step 3/5:** Completed weather forecast\n"
        reasoning_update = reasoning_display + f"Compiled weather information to help you pack appropriately.\n"
        yield status_update, reasoning_update, ""
        
        # Step 4: Search flights
        current_step += 1
        progress(current_step/total_steps, desc="Finding flight options...")
        progress_messages.append(f"⏳ Searching flights from {origin} to {destination}...")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        status_update += f"✅ **Step 3/5:** Completed weather forecast\n"
        status_update += f"🔄 **Step 4/5:** Searching flights from {origin} to {destination}...\n"
        reasoning_update = reasoning_display + f"Finding optimal flight options between {origin} and {destination}...\n"
        yield status_update, reasoning_update, ""
        
        flights_report = search_flights(travel_agent, origin, destination, travel_dates)
        progress_messages.append(f"✅ Flight search complete")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        status_update += f"✅ **Step 3/5:** Completed weather forecast\n"
        status_update += f"✅ **Step 4/5:** Completed flight search\n"
        reasoning_update = reasoning_display + f"Identified flight options with the best combinations of price and convenience.\n"
        yield status_update, reasoning_update, ""
        
        # Step 5: Generate final report
        current_step += 1
        progress(current_step/total_steps, desc="Generating final travel report...")
        progress_messages.append(f"⏳ Creating comprehensive travel plan...")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        status_update += f"✅ **Step 3/5:** Completed weather forecast\n"
        status_update += f"✅ **Step 4/5:** Completed flight search\n"
        status_update += f"🔄 **Step 5/5:** Creating your comprehensive travel plan...\n"
        reasoning_update = reasoning_display + f"Organizing all gathered information into a comprehensive travel plan...\n"
        yield status_update, reasoning_update, ""
        
        final_report = write_travel_report(
            reporter_agent,
            destination_report,
            events_report,
            weather_report,
            flights_report
        )
        progress_messages.append(f"✅ Travel plan generation complete!")
        
        status_update = status_display
        status_update += f"✅ **Step 1/5:** Completed destination research\n"
        status_update += f"✅ **Step 2/5:** Completed events research\n"
        status_update += f"✅ **Step 3/5:** Completed weather forecast\n"
        status_update += f"✅ **Step 4/5:** Completed flight search\n"
        status_update += f"✅ **Step 5/5:** Completed travel plan\n\n"
        status_update += "## 🎉 Your travel plan is ready! See the full report in the Travel Plan tab."
        
        reasoning_update = reasoning_display + f"All tasks complete! Your personalized travel plan is now ready in the Travel Plan tab.\n"
        
        yield status_update, reasoning_update, final_report
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        
        # Fix for the f-string issue - create the progress list separately
        progress_list = ''.join([f'- {msg}\n' for msg in progress_messages])
        
        error_message = (
            f"# Error Creating Travel Plan\n\n"
            f"An error occurred while generating your travel plan: {str(e)}\n\n"
            f"```\n{error_trace}\n```\n\n"
            f"Progress before error:\n"
            f"{progress_list}"
        )
        return error_message, "An error occurred during planning", ""

def create_gradio_app():
    """
    Create and configure the Gradio app with tabbed interface.
    
    Returns:
        gr.Blocks: Configured Gradio app
    """
    with gr.Blocks(title=APP_SETTINGS["title"]) as app:
        gr.Markdown(
            """
            # 🌍 AI Travel Planner
            
            Let AI research and plan your next trip! This tool will:
            - Research your destination
            - Find events happening during your trip
            - Check weather forecasts
            - Suggest flight options
            - Generate a comprehensive travel report
            
            Just enter your details below and click "Plan My Trip"!
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Trip Details Section
                gr.Markdown("### Trip Details")
                with gr.Group():
                    origin = gr.Textbox(
                        label="Current Location (Origin)", 
                        placeholder="e.g., Boston, NYC, LAX",
                        info="Enter city name or airport code"
                    )
                    destination = gr.Textbox(
                        label="Destination", 
                        placeholder="e.g., Barcelona, Spain",
                        info="Where would you like to go?"
                    )
                    dates = gr.Textbox(
                        label="Travel Dates", 
                        placeholder="e.g., April 15-22, 2025",
                        info="When are you planning to travel?"
                    )
                    interests = gr.Textbox(
                        label="Interests/Preferences", 
                        placeholder="e.g., historical sites, cuisine, outdoor activities",
                        info="What are you interested in seeing or doing?"
                    )
                    
                    init_agents_btn = gr.Button("Initialize Agents", variant="secondary")
                    generate_btn = gr.Button("Plan My Trip", variant="primary")
                
                # Tips Section
                gr.Markdown("### Tips")
                with gr.Group():
                    gr.Markdown(
                        """
                        - Be specific about your interests to get better recommendations
                        - Include your travel dates in a clear format
                        - For destinations, you can specify cities, regions, or countries
                        - The first search might take a bit longer as the system initializes
                        - Check the different tabs to see your plan's progress
                        """
                    )
            
            # Right side for outputs with tabs
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.TabItem("Status"):
                        status_output = gr.Markdown(value="Waiting to start...")
                    
                    with gr.TabItem("AI Reasoning"):
                        reasoning_output = gr.Markdown(value="The planning process will appear here once planning starts.")
                    
                    with gr.TabItem("Travel Plan"):
                        plan_output = gr.Markdown(value="Your travel plan will appear here when ready.")
        
        # Set up event handlers
        init_agents_btn.click(initialize_agents, inputs=None, outputs=status_output)
        generate_btn.click(
            generate_travel_plan, 
            inputs=[origin, destination, dates, interests],
            outputs=[status_output, reasoning_output, plan_output]
        )
        
        # Add example inputs
        gr.Examples(
            [
                ["New York", "Paris", "June 10-17, 2025", "Art, cuisine, architecture"],
                ["San Francisco", "Kyoto", "September 5-15, 2025", "Historical sites, gardens, traditional culture"],
                ["London", "Barcelona", "April 20-27, 2025", "Beaches, food, nightlife"],
            ],
            inputs=[origin, destination, dates, interests]
        )
    
    return app

if __name__ == "__main__":
    # Create and launch the app
    app = create_gradio_app() 
    app.launch(share=APP_SETTINGS["share"],server_name="0.0.0.0")

    """
    Test comment to check if the deployment works correctly and the CI-CD pipeline is functioning.
    """