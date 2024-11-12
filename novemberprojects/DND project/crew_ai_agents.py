import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
import os
from keys import get_openai_api_key

# Retrieve and set OpenAI API key
openai_api_key = get_openai_api_key()
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    raise EnvironmentError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

#### Agent for generating a biography-style backstory with article formatting

# Backstory Creator Agent (Article Style)
backstory_creator = Agent(
    role="Backstory Reporter",
    goal="Write a compelling, detailed biography in the style of a newspaper article or blog post for a {race} {class} companion.",
    backstory=(
        "As a skilled journalist, you capture stories with depth and flair. Your job is to write an extensive, immersive article "
        "on this companion, structuring it like a newspaper feature or blog post. The article should include sections for the character's "
        "Name, Race, and Class, and delve into their life's journey, achievements, and challenges, creating a vivid portrait of their personality. "
        "You may choose to either inspire readers with their accomplishments or draw them in with an aura of mystery surrounding the character."
    ),
    allow_delegation=False
)

#### Task to Create the Article-Style Backstory
create_article_biography = Task(
    description=(
        "Write an extensive, detailed article-style biography for this {race} {class} companion. "
        "The article should include labeled sections for Name, Race, and Class at the beginning, and follow with a "
        "deeply engaging story that could read like a feature in a major newspaper or popular blog. "
        "Choose to inspire readers with their triumphs and growth, or weave in an element of mystery that hints at untold secrets. "
        "Ensure to include the companion's Name as a separate section in the output."
    ),
    expected_output="A fully formatted, article-style biography for the companion, including a Name section.",
    agent=backstory_creator,
)

#### Crew setup for generating the article-style backstory
crew = Crew(
    agents=[backstory_creator],
    tasks=[create_article_biography]
)

def generate_companion_backstory(race, character_class):
    """Generates a complete, article-style backstory for a companion."""
    # Run Crew task to generate a newspaper or blog-style biography
    result = crew.kickoff(inputs={"race": race, "class": character_class})

    # Convert CrewOutput to a string and return it as a single backstory
    backstory = str(result)
    print("Generated Article-Style Backstory:", backstory)  # Debug output

    return backstory
