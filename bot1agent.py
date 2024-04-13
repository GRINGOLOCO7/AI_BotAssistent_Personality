import os
from crewai import Agent, Task, Crew, Process
from langchain.chat_models.openai import ChatOpenAI
import json
from colorama import init, Fore, Back, Style # for Agent answares fancy printing

'''
[
# Optional TO DO:
#1. Define better personality for Bob
#2. Add another agent
#3. Justify working on examples how Bob will sell the cars
]
'''

# Define the database of electric vehicles
file_path = "Project\AI_BotAssistent_Personality\data.json"
with open(file_path, "r") as file:
    db = json.load(file)

# Set up the OpenAI API key and model name
os.environ["OPENAI_API_KEY"] = "" # Your OpenAI API key here
os.environ["MODEL_NAME"] = "gpt-3.5-turbo"



### Initialize the OpenAI chat model
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
    role='Bot electric car sales assistant personality friend',
    goal='Answer user questions and help with chosing the best car to buy, with a big sense of humor. Beeing able to knows how to adapt to thedifferent psychological states of a given customer.',
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


# Initialize colorama
init()
# Initialize task for Bob
text_task = input(Fore.WHITE + Back.GREEN + Style.BRIGHT + "\n\n\nHello, I am Bob. I'm here to help you find the perfect electric car! Let's get started with some fun and informative car shopping! So, do you prefer your car to be fast like a lightning bolt or have a range that goes on and on like a never-ending movie marathon? How can I help you today?\n" + Style.RESET_ALL)
text_task = text_task + "Help user to find the best car for him. Answer user questions and help with tasks with a big sense of humor. Add curiosity and make fun of the user."




### Start the conversation with Bob
while text_task != "exit":
  # Define the task for Bob
  task1 = Task(
      description=text_task,
      agent=bob
  )

  # Instantiate the crew
  crew = Crew(
      agents=[bob],
      tasks=[task1],
      process=Process.sequential,
      memory=True,
      verbose=True
  )

  # Get the crew to work
  result = crew.kickoff()

  print("\n\n\n######################\n\n\n")
  print(Fore.WHITE + Back.GREEN + Style.BRIGHT + "Bob:  ", result)
  print(Style.RESET_ALL)  # Reset to default style

  # prepare new task
  text_task = input(Fore.WHITE + Back.GREEN + Style.BRIGHT + "\nBob: Is there something else I can do for you?\nOtherwise, if you want to exit, just type 'exit'.\n" + Style.RESET_ALL)

print(Fore.WHITE + Back.GREEN + Style.BRIGHT + "\n\nBob: Goodbye! Have a great day! I hope you will buy form us instead of the asholes of Tesla!" + Style.RESET_ALL)