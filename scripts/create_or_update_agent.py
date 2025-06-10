import json
import os
import re

import click
import dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Load the environment variables from the .env file (ensuring first that the file exists)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if not os.path.exists(env_path):
    raise FileNotFoundError("No .env file found in the project root directory")

dotenv.load_dotenv(env_path)


@click.command()
@click.argument("agent_config_file", type=click.Path(exists=True))
@click.argument("project_connection_string", envvar="PROJECT_CONNECTION_STRING")
def deploy_agent(agent_config_file, project_connection_string):
    print(project_connection_string)
    # Load the json agent config and replace any references with environment variables
    with open(agent_config_file, "r") as f:
        config_str = f.read()

        # Replace any references with environment variables
        config_str = re.sub(r"\$(\w+)", lambda x: os.environ[x.group(1)], config_str)

        # Load the config as a json object
        config = json.loads(config_str)

        print(config)

    project_client = AIProjectClient(
        endpoint=project_connection_string,
        credential=DefaultAzureCredential(),
    )

    # Check if agent already exists
    agents = list(project_client.agents.list_agents())
    print(agents)

    if config.get("name") in [agent.name for agent in agents]:
        print(
            f"Agent {config.get('name')} already exists. Updating existing agent with new config."
        )
        agent_id = next(
            agent.id for agent in agents if agent.name == config.get("name")
        )
        agent = project_client.agents.update_agent(
            agent_id=agent_id,
            name=config.get("name"),
            model=config["model"],
            description=config.get("description"),
            instructions=config.get("instructions"),
            headers=config.get("headers"),
            tools=config.get("tools"),
            tool_resources=config.get("tool_resources"),
        )

    else:
        # Create an agent with the Azure Function tool to get the weather
        agent = project_client.agents.create_agent(
            name=config.get("name"),
            model=config["model"],
            description=config.get("description"),
            instructions=config.get("instructions"),
            headers=config.get("headers"),
            tools=config.get("tools"),
            tool_resources=config.get("tool_resources"),
        )
        print(f"Agent {agent.name} created.")


if __name__ == "__main__":
    deploy_agent()
