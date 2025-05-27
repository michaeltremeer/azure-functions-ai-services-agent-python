import os
import subprocess

# Define the path to the agents folder in the repo root
agents_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents")

# Iterate through each agent config file in the agents folder
for filename in os.listdir(agents_folder):
    if filename.endswith(".json"):
        config_path = os.path.join(agents_folder, filename)
        print(f"Processing agent config: {config_path}")

        # Execute deploy_agent.py with the config file as an argument
        subprocess.run(["python", "scripts/create_or_update_agent.py", config_path])
