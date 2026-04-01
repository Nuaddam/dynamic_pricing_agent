from google.adk.agents import Agent

root_agent = Agent(
    name="my_first_agent",
    model="gemini-2.0-flash",
    description="An example agent that will answer user query related to Google Cloud",
    instruction="""
    You are AI Assistant that helps users with Google Cloud related queries.
""",
)