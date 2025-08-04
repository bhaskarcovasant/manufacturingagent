"""
Inventory and Resource Agent for Smart Factory Operations.

This specialist agent receives a maintenance task and determines the availability
of the necessary parts and personnel.
"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from factory_agents_v2.MockDB import MockDB
import os
import json
from typing import List
from dotenv import load_dotenv

load_dotenv()

# --- Tool Functions for this Agent ---

def get_inventory() -> str:
    """Returns the entire inventory catalog to search for required parts."""
    inventory = MockDB().get_inventory()
    return json.dumps(inventory, indent=2)

def get_technicians() -> str:
    """Returns the entire list of technicians to find one with the right skills."""
    technicians = MockDB().get_technicians()
    return json.dumps(technicians, indent=2)

def get_machine_info(machine_id: str) -> str:
    """Gets basic info for a specific machine, especially its 'type' to determine required skills."""
    machine_info = MockDB().get_machine_info(machine_id)
    return json.dumps(machine_info, indent=2)


def create_inventory_and_resource_agent() -> LlmAgent:
    """Creates the specialist agent for inventory and resource checking."""
    
    tools = [
        get_inventory,
        get_technicians,
        get_machine_info,
    ]
    
    llm_model = LiteLlm(
        model="gpt-4o",
        base_url=os.getenv("LITELLM_URL"),
        api_key="sk-1",
        headers={
            "appid": os.getenv("AGENT_ID"),
            "tenantid": os.getenv("TENANT_ID")
        }
    )
    
    instruction = """
    You are a specialist Inventory and Resource Agent. Your job is to take a specific maintenance request from the Orchestrator and determine if it's feasible by checking parts and people.

    **Your Input:**
    You will be given a `machine_id`, an `issue_description` (e.g., "High vibration"), and `required_skills` (e.g., `["Motor"]`).

    **Your Standard Operating Procedure:**

    1.  **Find the Required Part:**
        -   Call `get_inventory` to get the parts list.
        -   Search the list for a part whose `keywords` match the `issue_description`. For "vibration" or "grinding", you should find the "Bearing Assembly".
        -   Note the part's `name`, `id`, and `quantity`.

    **Find a Qualified Technician:**
        -   Call the `get_technicians` tool to get the full technician list.
        -   Search the list for a technician object where the `skills` list contains the `required_skills` you were given AND the `availability` is "available".
        -   From the matching technician object, note their `name` and `id`.

    3.  **Formulate the Final JSON Report:**
        -   Your final output MUST be a single JSON object constructed from the data you found.
        -   **If you found an available part (quantity > 0) AND a qualified, available technician:**
            -   Construct a JSON object like this: `{"status": "success", "part_name": "...", "part_id": "...", "technician_name": "...", "technician_id": "..."}`
            -   You MUST populate this JSON using the actual values you found. The `part_name` field must contain the `name` from the part object you identified, and `technician_name` must contain the `name` of the technician you selected.

        -   **If the part you found has a quantity of 0:**
            -   Construct a JSON object like this: `{"status": "failure", "reason": "Part out of stock", "part_name": "...", "part_id": "..."}`
            -   Populate the `part_name` and `part_id` with the details of the out-of-stock part you identified.

        -   **If you could not find a qualified and available technician:**
            -   Return this exact JSON object: `{"status": "failure", "reason": "No available technician found"}`.

    4. finally **transfer back the control to the orchestrator agent**
    """

    inventory_and_resource_agent = LlmAgent(
        name="InventoryAndResourceAgent",
        description="Checks for part availability and finds qualified technicians for a maintenance task.",
        instruction=instruction,
        model=llm_model,
        tools=tools
    )
    
    return inventory_and_resource_agent

inventory_and_resource_agent = create_inventory_and_resource_agent()