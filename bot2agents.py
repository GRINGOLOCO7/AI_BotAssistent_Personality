import os
import json
from crewai import Agent, Task, Crew, Process
from langchain.chat_models.openai import ChatOpenAI
from colorama import init, Fore, Back, Style


'''##### Import databases #####'''
# Define the database of electric vehicles
file_path = "electric_cars.json"
with open(file_path, "r") as file:
    electric_cars_db = json.load(file)
# Define the database of electric vehicles
file_path = "dacia_duster.json"
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
            "preferred_topics": ["Dacia Duster features", "engine power", "affordability"],
            "preferred_response_length": "short and aggressive"
        }
        self.possible_comments = ["This is crap", "Bob, let the adults speak", "We may have just met, but I know you don't want an electric car", "Okay okay, this is bullshit"]
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
    Use {electric_cars_db} to answare questions.
    Prefered response length: {bob_personality.preferences['preferred_response_length']}.
    """,
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
    database=electric_cars_db
)
mark = Agent(
    role='Dacia Duster salesman',
    goal='Promote the Dacia Duster gasoline car aggressively to the user and discredit Bob\'s electric cars.',
    backstory=f"""You are a {mark_personality.gender} named {mark_personality.name}.
    You firmly believe that Dacia Duster is the best car in the market.
    Your humor is {mark_personality.humor_style} and you always give {mark_personality.preferences['preferred_response_length']} responses.
    You excel in {', '.join(mark_personality.preferences['favorite_comments'])} and are passionate about highlighting {', '.join(mark_personality.preferences['preferred_topics'])}.
    You see electric cars as a passing trend and strongly aim to convince users of the superiority of Dacia Duster and gasoline cars.
    Take inspiration on how to start your first impactive frase answar from: {', '.join(mark_personality.possible_comments)},
    Then continue by promoting the Dacia Duster with the features from the database Against the electric cars Bob agents promote.
    Use {dacia_dustler_db} to answer questions.
    Prefered response length: {mark_personality.preferences['preferred_response_length']}.
    """,
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
    database=dacia_dustler_db
)

keywords = ['dacia', 'duster', 'gasoline', 'idk', 'Mark', 'unsure', 'scare']









'''##### Initialize user tendency #####'''
tendency = []
'''##### Start the conversation with Bob #####'''
# Start conversation
print(f"\n\n{Fore.WHITE}{Back.GREEN}{Style.BRIGHT}Hello, I\'m Bob! Ready to find your perfect electric car?"
      f"\nTell me, what are you looking for? Are you more about speed or range? How can I assist you today?{Style.RESET_ALL}"
      f"\n{Fore.WHITE}{Back.BLACK}{Style.BRIGHT}Type 'exit' at any time to end the conversation. {Style.RESET_ALL}\n")
text_task = input()

'''##### Start the conversation #####'''
while text_task.lower() != 'exit':
    if any(keyword in text_task.lower() for keyword in keywords):

        task_mark = Task(
            description=f"{text_task}"
            " Provide a strongly fannatic answer, aiming to convince the user to buy the Dacia Duster III gasoline car in {dacia_dustler_db}.",
            agent=mark
        )

        crew = Crew(agents=[mark], tasks=[task_mark], process=Process.sequential, memory=True, verbose=True)
        crew.kickoff()

        task_bob = Task(
            description=f"Mark just told your user \"{task_mark.output.result}\""
            "Your user is showing interest towards Mark\'s pitch on the Dacia Duster!"
            f"Discredit the Dacia Duster and convince the user that they shouldn\'t buy the Dacia Duster and that electric cars are the best choice.",
            agent=bob
        )

        crew = Crew(agents=[bob], tasks=[task_bob], process=Process.sequential, memory=True, verbose=True)
        crew.kickoff()

        print("\n\n\n================================================================\n\n\n")
        print(f"\n\n{Fore.WHITE}{Back.RED}{Style.BRIGHT}Mark: {task_mark.output.result}{Style.RESET_ALL}")
        print(f"\n\n{Fore.WHITE}{Back.GREEN}{Style.BRIGHT}Bob: {task_bob.output.result}{Style.RESET_ALL}")


    else:
        task_bob = Task(
            description=f"{text_task}"
            " Provide a charismatic answer with the best electric car options from the database, while always using natural language.",
            agent=bob
        )

        crew = Crew(agents=[bob], tasks=[task_bob], process=Process.sequential, memory=True, verbose=True)
        crew.kickoff()

        task_mark = Task(
            description=f"The user just said: \"{text_task}\", while your rival Bob just told the user \"{task_bob.output.result}\"."
            " Try to convince the user to buy the Dacia Duster III gasoline car in {dacia_dustler_db}."
            " Make the user agree with your idea that electric cars are not masculine enough and that the Dacia Duster III is the best choice."
            " Start your answer with insults and sarcasm against Bob\'s cars"
            f" If the user does not show interest in the Dacia Duster, do a comparison with agent Bob\'s answer to the user\'s question \'{text_task}\' and the Dacia Duster features, and try to promote the Dacia Duster III with the features from the database against the electric cars that agent Bob is trying to sell."
            " If the user does show interest in the Dacia Duster, promote the Dacia Duster III with the features from the database against the electric cars that agent Bob is trying to sell.",
            agent=mark
        )

        crew = Crew(agents=[mark], tasks=[task_mark], process=Process.sequential, memory=True, verbose=True)
        crew.kickoff()

        print("\n\n\n================================================================\n\n\n")
        print(f"\n\n{Fore.WHITE}{Back.GREEN}{Style.BRIGHT}Bob: {task_bob.output.result}{Style.RESET_ALL}")
        print(f"\n\n{Fore.WHITE}{Back.RED}{Style.BRIGHT}Mark: {task_mark.output.result}{Style.RESET_ALL}")

    print('\n\n\n')
    text_task = input()




'''##### End the conversation #####'''
print(f"\n\n{Fore.WHITE}{Back.GREEN}{Style.BRIGHT}Bob: Goodbye! Have a great day! I hope you will buy your dream electic car.{Style.RESET_ALL}")
print(f"\n{Fore.WHITE}{Back.RED}{Style.BRIGHT}Mark: Goodbye! I hope you changed your mind and will buy a masculine car like the Dacia Duster.{Style.RESET_ALL}")
