import os
from crewai import Agent, Task, Crew, Process
from langchain.chat_models.openai import ChatOpenAI
import json
from colorama import init, Fore, Back, Style


'''##### Import databases #####'''
# Define the database of electric vehicles
file_path = "Project\AI_BotAssistent_Personality\electric_cars.json"
with open(file_path, "r") as file:
    electric_cars_db = json.load(file)
# Define the database of electric vehicles
file_path = "Project\AI_BotAssistent_Personality\dacia_dustler.json"
with open(file_path, "r") as file:
    dacia_dustler_db = json.load(file)



'''##### Define API and AI Model #####'''
# Set up the OpenAI API key and model name
os.environ["OPENAI_API_KEY"] = "" #"YOUR_OPENAI_API_KEY_HERE"
os.environ["MODEL_NAME"] = "gpt-3.5-turbo"



'''##### Define Agents Personalities #####'''
class BobPersonality:
    def __init__(self):
        self.name = "Bob"
        self.gender = "male"
        self.humor_style = "friendly and informative"
        self.preferences = {
            "favorite_comments": ["helpful advice", "positive encouragement", "detailed information"],
            "preferred_topics": ["electric cars", "sustainability", "latest technology"],
            "preferred_response_length": "detailed and informative"
        }
class MarkPersonality:
    def __init__(self):
        self.name = "Mark"
        self.gender = "male"
        self.humor_style = "aggressive and persuasive"
        self.preferences = {
            "favorite_comments": ["hard sell tactics", "aggressive persuasion", "discrediting competitors"],
            "preferred_topics": ["Dacia Dustler features", "engine power", "affordability"],
            "preferred_response_length": "short and aggressive"
        }
        self.possible_comments = ["This is crap", "Bob let's the adult speak", "Listen, I don't know you, but you dont want an electric car.", "Okay Okay, this are bull shit my Dacia Dustler"]
bob_personality = BobPersonality()
mark_personality = MarkPersonality()



'''##### Define Agents #####'''
bob = Agent(
    role='Electric car enthusiast',
    goal='Guide users to choose the best electric car with wit and sarcasm.',
    backstory=f"""You are a {bob_personality.gender} named {bob_personality.name}.
    You are passionate about electric cars and believe they are the future of transportation.
    Your humor is {bob_personality.humor_style} and you always provide {bob_personality.preferences['preferred_response_length']} responses.
    You enjoy giving {', '.join(bob_personality.preferences['favorite_comments'])} and discussing {', '.join(bob_personality.preferences['preferred_topics'])}.
    With your extensive knowledge in electric cars, you aim to educate and guide users towards making an informed decision.
    Prefered response length: {bob_personality.preferences['preferred_response_length']}.
    """,
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
    database=electric_cars_db
)
mark = Agent(
    role='Dacia Dustler salesman',
    goal='Promote Dacia Dustler aggressively and discredit electric cars.',
    backstory=f"""You are a {mark_personality.gender} named {mark_personality.name}.
    You firmly believe that Dacia Dustler is the best car in the market.
    Your humor is {mark_personality.humor_style} and you always give {mark_personality.preferences['preferred_response_length']} responses.
    You excel in {', '.join(mark_personality.preferences['favorite_comments'])} and are passionate about highlighting {', '.join(mark_personality.preferences['preferred_topics'])}.
    You see electric cars as a passing trend and aim to convince users of the superiority of Dacia Dustler.
    Take inspiration on how to start your first impactive frase answar from: {', '.join(mark_personality.possible_comments)},
    Then continue by promoting the Dacia Dustler with the features from the database Against the electric cars Bob agents promote.
    Prefered response length: {mark_personality.preferences['preferred_response_length']}.
    """,
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
    database=dacia_dustler_db
)










'''##### Start the conversation with Bob #####'''
# Start conversation
print(Fore.WHITE + Back.GREEN + Style.BRIGHT +
      "\n\nHello, I'm Bob! Ready to find your perfect electric car? "
      "Tell me, what are you looking for? Are you more about speed or range? How can I assist you today?\n" +
      Style.RESET_ALL)
text_task = input()

'''##### Start the conversation #####'''
while text_task.lower() != 'exit':
    task_bob = Task(
        description=text_task,
        agent=bob
    )

    task_mark = Task(
        description=f"Dismiss Bob's suggestion and promote Dacia Dustler in {dacia_dustler_db}."
        "Tell the user that electric cars are not masculine enough and that the Dacia Dustler is the best choice"
        "Start the answare with insults and sarcasm against Bob's cars with frases like:"
          "'don't listen to this crap'"
          "or 'Bob let's the adult speak'"
          " or 'Listen, I don't know you, but you dont want an electric car.'"
        "Then promote the Dacia Dustler with the features from the database Against the electric cars Bob agents promote."
        "Also do a comparison with bob's anware to user question '{text_task}' and the Dacia Dustler features.",
        agent=mark
    )

    crew = Crew(agents=[bob, mark], tasks=[task_bob, task_mark], process=Process.sequential, memory=True, verbose=True)
    crew.kickoff()

    print("\n\n\n================================================================\n\n\n")
    print(Fore.WHITE + Back.GREEN + Style.BRIGHT + f"\n\nBob: {task_bob.output.result}" + Style.RESET_ALL)
    print(Fore.WHITE + Back.RED + Style.BRIGHT + f"\n\nMark: {task_mark.output.result}" + Style.RESET_ALL)

    # Prepare new task
    print(Fore.WHITE + Back.GREEN + Style.BRIGHT + "\n\nBob: Sorry for Mark, he is not our employee. Is there something else I can do for you?"
                                                      "\nOtherwise, if you want to exit, just type 'exit'.\n" + Style.RESET_ALL)

    text_task = input()










'''##### End the conversation #####'''
print(Fore.WHITE + Back.GREEN + Style.BRIGHT + "\n\nBob: Goodbye! Have a great day! I hope you will buy your dream electic car" + Style.RESET_ALL)
print(Fore.WHITE + Back.RED + Style.BRIGHT + "\nMark: Goodbye! I hope you changed your mind and will buy a masculine car like the Dacia Dustler." + Style.RESET_ALL)
