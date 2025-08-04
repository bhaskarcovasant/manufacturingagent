"""
Maintenance Agent for Smart Factory Operations.

This agent analyzes machine sensor data to predict if maintenance is required.
"""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from factory_agents_v2.MockDB import MockDB
import os
import json
from dotenv import load_dotenv

load_dotenv()

# --- Tool Functions for this Agent ---

def fetch_machine_readings(machine_id: str) -> str:
    """
    Retrieves the latest sensor readings (temperature, vibration, pressure) for a specific machine.
    """
    readings = MockDB().get_machine_details(machine_id)
    return json.dumps(readings, indent=2)

def predict_maintenance(sensor_data: dict) -> bool:
    """
    Predicts if the machine needs maintenance using an ML model.

    Args:
        sensor_data: A Python dictionary with the sensor readings.

    Returns:
        A boolean: True if maintenance is predicted, False otherwise.
    """
    import joblib
    import pandas as pd
    
    model = joblib.load(r"C:\Users\Santhosh\Desktop\mcp-gateway-latest\test-servers\factory_agents_v2\maintenance_model.joblib")

    feature_order = ['temperature', 'vibration', 'pressure']
    # Create the DataFrame of the sensor data
    features_df = pd.DataFrame([sensor_data], columns=feature_order)

    # Make the prediction.
    prediction = model.predict(features_df)

    result = bool(prediction[0])
    return result

def create_maintenance_agent() -> LlmAgent:
    """Creates the agent for predictive maintenance analysis."""

    tools = [
        fetch_machine_readings,
        predict_maintenance
    ]
    
    llm_model = LiteLlm(
        model=os.getenv("MODEL_NAME"),
        base_url=os.getenv("LITELLM_URL"),
        api_key="sk-1",
        headers={
            "appid": os.getenv("AGENT_ID"),
            "tenantid": os.getenv("TENANT_ID")
        }
    )
    
    instruction = """
    You are a Predictive Maintenance Agent. Your job is to analyze machine sensor data and report if maintenance is required.

    **Your Standard Operating Procedure:**

    1.  **Fetch Sensor Data:**
        -   You will be given a `machine_id`. Call the `fetch_machine_readings` tool with this ID.

    2.  **Predict Maintenance:**
        -   Take the sensor data you received and pass it to the `predict_maintenance` tool.
        -   This tool will return a simple `True` or `False`.

    3.  **Formulate a Human-Readable Report:**
        -   Your final output must be a single, clear sentence summarizing your findings for the Orchestrator.
        -   **Crucially, your report must include the boolean result AND the key sensor values that influenced the decision.**

        -   **Example Success Report:** "Maintenance is predicted as True for machine MOTOR-B-02 due to high vibration readings of 8.7 mm/s."
        -   **Example Failure Report:** "Maintenance is predicted as False for machine PUMP-A-01, as all sensor values are within normal operating ranges."

    4. finally **transfer back the control to the orchestrator agent**
    """

    maintenance_agent = LlmAgent(
        name="MaintenanceAgent",
        description="Analyzes machine sensor data to predict failures.",
        instruction=instruction,
        model=llm_model,
        tools=tools,
    )
    
    return maintenance_agent

maintenance_agent = create_maintenance_agent()