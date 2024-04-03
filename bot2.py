import os
from crewai import Agent, Task, Crew
from langchain.chat_models.openai import ChatOpenAI

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

db = {
  "electric_vehicles": [
    {
      "brand": "Voltic Motors",
      "model": "EcoCharge X",
      "main_features": {
        "battery_capacity_kWh": 90,
        "range_miles": 300,
        "acceleration_0_60_mph": 4.5,
        "charging_time_hours": {
          "fast_charge": 1.5,
          "normal_charge": 8
        },
        "seating_capacity": 5
      },
      "price": 55000,
      "applicable_offers": {
        "federal_tax_credit": 7500,
        "manufacturer_discount": 2000,
        "trade_in_bonus": 1000
      }
    },
    {
      "brand": "ElectraDrive",
      "model": "ThunderBolt S",
      "main_features": {
        "battery_capacity_kWh": 75,
        "range_miles": 280,
        "acceleration_0_60_mph": 4.8,
        "charging_time_hours": {
          "fast_charge": 2,
          "normal_charge": 10
        },
        "seating_capacity": 4
      },
      "price": 60000,
      "applicable_offers": {
        "state_rebate": 3000,
        "manufacturer_discount": 1500
      }
    },
    {
      "brand": "Zenith Motors",
      "model": "ZenDrive Z5",
      "main_features": {
        "battery_capacity_kWh": 80,
        "range_miles": 320,
        "acceleration_0_60_mph": 5.2,
        "charging_time_hours": {
          "fast_charge": 2.5,
          "normal_charge": 12
        },
        "seating_capacity": 5
      },
      "price": 58000,
      "applicable_offers": {
        "manufacturer_discount": 2500,
        "loyalty_bonus": 750
      }
    },
    {
      "brand": "EcoMotion",
      "model": "EcoSpark EV",
      "main_features": {
        "battery_capacity_kWh": 70,
        "range_miles": 260,
        "acceleration_0_60_mph": 5.5,
        "charging_time_hours": {
          "fast_charge": 2.5,
          "normal_charge": 14
        },
        "seating_capacity": 5
      },
      "price": 52000,
      "applicable_offers": {
        "federal_tax_credit": 6500,
        "trade_in_bonus": 1500
      }
    },
    {
      "brand": "NovaTech",
      "model": "NovaPower EV",
      "main_features": {
        "battery_capacity_kWh": 85,
        "range_miles": 300,
        "acceleration_0_60_mph": 5.0,
        "charging_time_hours": {
          "fast_charge": 2,
          "normal_charge": 11
        },
        "seating_capacity": 5
      },
      "price": 56000,
      "applicable_offers": {
        "state_rebate": 2000,
        "manufacturer_discount": 1000
      }
    }
  ]
}
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

print("######################")
print(result)
