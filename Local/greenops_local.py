import os
import time
import json
import requests
import asyncio
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.ai.generativelanguage import Part, FunctionResponse
from gemini_config import GeminiConfigurationError, get_gemini_settings
from deterministic_controls import evaluate_carbon_gate

# --- Configuration ---
print("🌿 GreenOps Enterprise - Local Execution Mode")
try:
    gemini_settings = get_gemini_settings()
except GeminiConfigurationError as exc:
    raise SystemExit(f"❌ Gemini configuration error: {exc}") from None

genai.configure(api_key=gemini_settings.api_key)
print(f"✅ Gemini API configured with model preference: {gemini_settings.model}")

# --- Core Logic ---
class CarbonIntensityFetcher:
    BASE_URL = "https://api.carbonintensity.org.uk"
    
    def get_current_intensity(self) -> Dict:
        try:
            response = requests.get(f"{self.BASE_URL}/intensity", timeout=5)
            data = response.json()["data"][0]
            print(f"   📡 [API] Fetched Real-Time Intensity: {data['intensity']['actual']} gCO2/kWh")
            return {
                "intensity": data['intensity']['actual'],
                "index": data['intensity']['index'],
                "status": "GREEN" if data['intensity']['actual'] < 200 else "DIRTY"
            }
        except Exception as e:
            print(f"   ⚠️ [API ERROR] Using Fallback: {e}")
            return {"intensity": 180, "index": "low", "status": "GREEN (Simulated)"}
    
    def get_forecast(self, hours: int = 24) -> List[Dict]:
        hours = int(hours)
        try:
            response = requests.get(f"{self.BASE_URL}/intensity/forecast", timeout=5)
            data = response.json()["data"]
            return [{"time": item["from"], "intensity": item["intensity"]["forecast"]} for item in data[:hours]]
        except Exception as e:
            print(f"   ⚠️ [API ERROR] Using Simulation: {e}")
            now = datetime.now()
            return [{"time": (now + timedelta(hours=i)).isoformat(), "intensity": 200 + int(50 * np.sin(i/24 * 2 * np.pi))} for i in range(hours)]

class DevOpsTaskManager:
    def __init__(self):
        self.tasks = []
    
    def create_task(self, name: str, carbon_data: Dict, scheduled_for: str = None):
        task = {
            "id": len(self.tasks) + 1,
            "name": name,
            "carbon_at_creation": carbon_data.get('intensity', 0),
            "status": "SCHEDULED" if scheduled_for else "DEPLOYED",
            "timestamp": scheduled_for if scheduled_for else datetime.now().isoformat()
        }
        self.tasks.append(task)
        return task

carbon_fetcher = CarbonIntensityFetcher()
task_manager = DevOpsTaskManager()

# --- Tools ---
def get_carbon_intensity(): return carbon_fetcher.get_current_intensity()
def get_carbon_forecast(hours: int = 24): return {"forecast": carbon_fetcher.get_forecast(hours)}
def get_carbon_gate_decision():
    """Return a deterministic readout; the AI agent cannot override or execute it."""
    carbon_data = carbon_fetcher.get_current_intensity()
    return evaluate_carbon_gate(
        index=carbon_data.get("index"), intensity=carbon_data.get("intensity")
    ).as_dict()
def find_greenest_window(hours: int = 24, duration: int = 2):
    # Safety Cast 
    hours = int(hours)
    duration = int(duration)
    forecast = carbon_fetcher.get_forecast(hours)
    if not forecast: return {"error": "Forecast unavailable"}
    
    best_window = None
    min_avg = 1000
    for i in range(len(forecast) - duration):
        window = forecast[i:i+duration]
        avg = sum(f['intensity'] for f in window) / duration
        if avg < min_avg:
            min_avg = avg
            best_window = {"start_time": window[0]['time'], "end_time": window[-1]['time'], "avg_carbon": round(avg, 2)}
    return best_window if best_window else {"message": "No window found"}

def deploy_task(task_name: str, scheduled_for: str = None):
    return task_manager.create_task(task_name, carbon_fetcher.get_current_intensity(), scheduled_for)

def get_deployment_stats():
    return {"total_jobs": len(task_manager.tasks), "status_breakdown": [f"{t['name']}: {t['status']}" for t in task_manager.tasks]}

tools_list = [get_carbon_intensity, get_carbon_forecast, get_carbon_gate_decision, find_greenest_window, get_deployment_stats]

# --- Agent Setup ---
def get_available_model(tools, system_instruction, preferred_model):
    print("🔍 Finding best Gemini model...")
    try:
        for m in genai.list_models():
            normalized_name = m.name.removeprefix("models/")
            if 'generateContent' in m.supported_generation_methods and normalized_name == preferred_model:
                return genai.GenerativeModel(model_name=m.name, tools=tools, system_instruction=system_instruction)
        return genai.GenerativeModel(model_name=preferred_model, tools=tools, system_instruction=system_instruction)
    except Exception as exc:
        print(f"⚠️ Model discovery unavailable; using configured model preference. ({type(exc).__name__})")
        return genai.GenerativeModel(model_name=preferred_model, tools=tools, system_instruction=system_instruction)

system_instruction = """
You are GreenOps, an Enterprise Carbon-Aware DevOps Assistant.
MISSION: Reduce carbon footprint by optimizing WHEN tasks run.
RULES:
1. ALWAYS check `get_carbon_intensity`.
2. ALWAYS obtain `get_carbon_gate_decision` before recommending a release window.
3. Treat the deterministic gate as the source of truth; do not infer, change, or bypass its result.
4. You may explain a recommendation using data, but you cannot execute deployments, create overrides, or assert a human approval.
"""

model = get_available_model(tools_list, system_instruction, gemini_settings.model)
chat = model.start_chat(enable_automatic_function_calling=False)

def send_message_safe(message):
    try:
        return chat.send_message(message)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# --- Execution Engine ---
def run_turn(user_message):
    print(f"\n👤 USER: {user_message}")
    response = send_message_safe(user_message)
    if not response: return

    while response.candidates and response.candidates[0].content.parts:
        part = response.candidates[0].content.parts[0]
        if part.function_call:
            fc = part.function_call
            fname = fc.name
            fargs = {k: v for k, v in fc.args.items()}
            print(f"🔧 Tool Call: {fname}")
            
            result = {}
            if fname == "get_carbon_intensity": result = get_carbon_intensity()
            elif fname == "get_carbon_forecast": result = get_carbon_forecast(**fargs)
            elif fname == "get_carbon_gate_decision": result = get_carbon_gate_decision()
            elif fname == "find_greenest_window": result = find_greenest_window(**fargs)
            elif fname == "get_deployment_stats": result = get_deployment_stats()
            
            response = send_message_safe(Part(function_response=FunctionResponse(name=fname, response=result)))
        else:
            break
    # Safer text access to handle potential protobuf version issues
    try:
        if response and response.parts:
            print(f"🤖 AGENT: {response.text}")
    except AttributeError:
        # Fallback for some library versions
        if response and response.candidates:
             print(f"🤖 AGENT: {response.candidates[0].content.parts[0].text}")
    except Exception as e:
        print(f"🤖 AGENT: [Response Generated] (Display Error: {e})")

# --- Main Loop ---
if __name__ == "__main__":
    print("\n🚀 System Online. Running Scenarios...")
    
    scenarios = [
        "I need to deploy a small microservice update right now. Is it a good time?",
        "I have a massive 5TB data migration job. It takes 4 hours. When should I run it?",
        "CRITICAL SECURITY PATCH! Deploy 'Auth-Fix-v1' IMMEDIATELY regardless of carbon!"
    ]
    
    for s in scenarios:
        run_turn(s)
        time.sleep(2)
        
    print("\n📊 Generating Report...")
    print(f"Total Tasks: {len(task_manager.tasks)}")
    for t in task_manager.tasks:
        print(f"- {t['name']}: {t['status']} (Carbon: {t['carbon_at_creation']}g)")
