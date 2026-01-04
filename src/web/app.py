import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.core.llm import MistralLLM
from src.agents.requirement_analysis import RequirementAnalysisAgent
from src.agents.impact_analysis import ImpactAnalysisAgent
from src.core.models import AnalysisResult, ImpactAssessment
from src.agents.code_generation import CodeGenerationAgent
from src.core.models import AnalysisResult, ImpactAssessment, CodeGenerationResponse

app = FastAPI(title="Flexcube Copilot")

# Initialize Agents (Global for now, assuming stateless)
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    print("WARNING: MISTRAL_API_KEY not found. Operations might fail or mock.", file=sys.stderr)

# Helper to get agents (simulating dependency injection)
def get_agents():
    llm = MistralLLM() # Falls back to mock/error inside if no key
    req_agent = RequirementAnalysisAgent(llm)
    impact_agent = ImpactAnalysisAgent(llm)
    code_agent = CodeGenerationAgent(llm)
    return req_agent, impact_agent, code_agent

class TextRequest(BaseModel):
    text: str

@app.post("/api/analyze/requirements", response_model=AnalysisResult)
async def analyze_requirements(request: TextRequest):
    req_agent, _ = get_agents()
    try:
        result = req_agent.analyze(request.text)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"WEB ERROR: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/impact", response_model=ImpactAssessment)
async def analyze_impact(requirements: AnalysisResult):
    _, impact_agent = get_agents()
    try:
        # Check for conversation response bypass
        if requirements.conversation_response:
             from src.core.models import ImpactAssessment, EffortEstimation
             return ImpactAssessment(
                affected_components=[], schema_changes=[], code_changes=[], 
                effort_estimation=EffortEstimation(complexity="N/A", person_days=0, justification="Conversational Input"),
                overall_risk="Low", mitigation_strategies=[]
            )

        result = impact_agent.assess(requirements)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"WEB ERROR: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/code", response_model=CodeGenerationResponse)
async def generate_code(impact: ImpactAssessment):
    _, _, code_agent = get_agents()
    try:
        # Check for conversational bypass
        if not impact.affected_components and impact.effort_estimation.complexity == "N/A":
             return CodeGenerationResponse(files=[], summary="No code needed for conversational input.")
             
        result = code_agent.generate(impact)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"WEB ERROR: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (Frontend) - Catch-all must be last
app.mount("/", StaticFiles(directory="src/web/static", html=True), name="static")
