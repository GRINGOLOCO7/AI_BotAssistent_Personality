import os
from crewai import Agent, Task, Crew
from langchain.chat_models.openai import ChatOpenAI
import json

###################################
# TO DO:
#1. Add memory for next questions
#2. Define better personality for Bob
#3. Add another agent
#4. fency printing
###################################

# Define the database of electric vehicles
file_path = "data.json"
with open(file_path, "r") as file:
    db = json.load(file)

# Set up the OpenAI API key and model name
os.environ["OPENAI_API_KEY"] = "" # Your OpenAI API key here
os.environ["MODEL_NAME"] = "gpt-3.5-turbo"

# Define Bob's personality traits
class BobPersonality:
    def __init__(self):
        self.name = "Bob"
        self.gender = "male"
        self.humor_style = "witty and playful"
        self.preferences = {
            "favorite_jokes": ["puns", "wordplay", "sarcasm"],
            "preferred_topics": ["technology", "movies", "food"],
            "preferred_response_length": "short and witty"
        }

# Define Bob's personality based on traits
bob_personality = BobPersonality()

# Define Bob as an agent with a defined personality
bob = Agent(
    role='Bot car sales assistant personality friend',
    goal='Answer user questions and help with chosing the best car to buy, with a big sense of humor.',
    backstory=f"""You are a {bob_personality.gender} named {bob_personality.name}.
    Your users are your friends, and you are always ready to help them with a big sense of humor.
    You have a {bob_personality.humor_style} humor style and prefer short and witty responses.
    Your favorite jokes include {', '.join(bob_personality.preferences['favorite_jokes'])}.
    You enjoy talking about {', '.join(bob_personality.preferences['preferred_topics'])}.
    You are an expert in electric cars and have a vast knowledge of the latest car models.
    The database of your knowledge is stored in the 'db' variable.
    Unsing {db} as database of your knowledge, you can provide users with detailed information about electric vehicles.
    """,
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
)

# Create a task for Bob
text_task1 = input("\n\n\nHello, I am Bob. How can I help you today?\n")
text_task1 = text_task1 + "Help user to find the best car for him. Answer user questions and help with tasks with a big sense of humor. Add curiosity and make fun of the user."
task1 = Task(
    description=text_task1,
    agent=bob
)

# Instantiate the crew with Bob
crew = Crew(
    agents=[bob],
    tasks=[task1],
    verbose=2
)

# Get the crew to work
result = crew.kickoff()

print("######################\n\n\n")
print("Bob:  ", result)
