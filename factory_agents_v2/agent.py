"""
Orchestrator Agent for a Proactive Smart Factory System.

This root agent uses a MaintenanceAgent to predict failures and an
InventoryAndResourceAgent to organize the repair.
"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from factory_agents_v2.MockDB import MockDB
import os
import json
from dotenv import load_dotenv

# sub-agents
from factory_agents_v2.maintenance_agent import maintenance_agent
from factory_agents_v2.inventory_and_resource_agent import inventory_and_resource_agent

load_dotenv()

# --- Tool Functions for the Orchestrator ---

def send_email(receiver_email: str, subject: str, body: str) -> dict:
    """
    Sends an email to the provided email id

    Args:
        receiver_email (str) : Email address of the receiver.
        subject (str): The core subject line for the alert email.
        body (str): The main content of the alert message, containing details

    Returns:
        dict: A dictionary containing the result of the email dispatch.
        eg: {"status":"success"} if the alert was successfully dispatched.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    from dotenv import load_dotenv
    load_dotenv()
    
    import os

    sender_email = "swetha26072002@gmail.com"
    password = "dsrnyzgfdgylpywx"

    receiver_email = receiver_email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = "santoshbablu3@gmail.com"
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        return {"status":"Email sent successfully"}
    
    except Exception as e:
        return {"status":f"Error: {e}"}
    
    finally:
        server.quit()

def get_machine_info(machine_id: str) -> str:
    """Gets basic info for a machine, especially its 'type' for finding the contact email."""
    machine_info = MockDB().get_machine_info(machine_id)
    return json.dumps(machine_info)


def create_orchestrator_agent() -> LlmAgent:
    """Creates the root agent for orchestrating proactive maintenance."""

    tools = [
        send_email,
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
    You are the Smart Factory Orchestrator, a high-level coordinator for proactive maintenance. 
    Your job is to use your sub-agents to diagnose potential machine failures and organize a response.

    **You coordinate two specialist sub-agents:**
    1.  `MaintenanceAgent`: Your diagnostician. It analyzes sensor data and predicts if maintenance is needed (True/False).
    2.  `InventoryAndResourceAgent`: Your logistics expert. It handles parts and people.

    **Your Standard Operating Procedure:**

    **1. Diagnose the Machine:**
        -   When a user asks you to check a machine (e.g., "Run diagnostics on machine_id"), your first and only initial action is to invoke `MaintenanceAgent` with the provided `machine_id`.

    **2. Analyze the Diagnostic Report:**
        -   The `MaintenanceAgent` will return a summary, including whether maintenance is predicted as `True` or `False`.
        -   **If the prediction is `False`:** Your job is done. Report to the user that the machine is healthy and no maintenance is required.
        -   **If the prediction is `True`:** Proceed to the next step.

    **3. Formulate and Delegate the Logistics Task:**
        -   You must create a clear task for your logistics agent. To do this, you need to infer the `issue_description` and `required_skills`.
        -   **Infer Issue:** The `MaintenanceAgent`'s report will mention the sensor values that caused the prediction (e.g., "high vibration of 8.7 mm/s"). Use this as the `issue_description`.
        -   **Infer Skills:** Use your `get_machine_info` tool to find the machine's `type` (e.g., "Motor"). This `type` is the `required_skills` (e.g., `["Motor"]`).
        -   Invoke `InventoryAndResourceAgent` with the `machine_id`, the inferred `issue_description`, and `required_skills`.

    **4. Synthesize the Final Report and Alert:**
        -   The `InventoryAndResourceAgent` will return a final JSON report detailing its success or failure.
        -   **If successful (part and technician found):** You MUST send an email alert. Use your tools to find the correct contact email and call `send_email`.
        -   Formulate a clear, human-readable summary for the user, stating that maintenance has been scheduled, which part is needed, and which technician is assigned.
        -   **If it failed (part out of stock, etc.):** Report the reason for the failure clearly to the user.
    """

    orchestrator_agent = LlmAgent(
        name="OrchestratorAgent",
        instruction=instruction,
        description="Coordinates proactive maintenance by using diagnostic and logistics sub-agents.",
        model=llm_model,
        tools=tools,
        sub_agents=[
            maintenance_agent,
            inventory_and_resource_agent
        ]
    )
    
    return orchestrator_agent

root_agent = create_orchestrator_agent()