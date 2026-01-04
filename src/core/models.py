from typing import List, Optional
from pydantic import BaseModel, Field

class FunctionalRequirement(BaseModel):
    id: str = Field(description="Unique identifier for the requirement (e.g., FR-001)")
    description: str = Field(description="Clear, concise description of the functional requirement")
    acceptance_criteria: List[str] = Field(description="List of testable acceptance criteria")
    priority: str = Field(default="Medium", description="Priority level (High, Medium, Low)")

class TechnicalImplication(BaseModel):
    module: str = Field(description="Impacted Flexcube module (e.g., FCIS, CASA, FX)")
    description: str = Field(description="Technical description of the impact")
    risk_level: str = Field(default="Low", description="Risk level associated with this technical change")

class AnalysisResult(BaseModel):
    business_objective: str = Field(default="N/A", description="1. Business Objective")
    client_type: str = Field(default="N/A", description="2. Client Type")
    regulatory_constraints: List[str] = Field(default_factory=list, description="3. Regulatory Constraints")
    functional_requirements: List[str] = Field(default_factory=list, description="4. Functional Requirements")
    non_functional_requirements: List[str] = Field(default_factory=list, description="5. Non-Functional Requirements")
    business_rules: List[str] = Field(default_factory=list, description="6. Business Rules")
    data_requirements: List[str] = Field(default_factory=list, description="7. Data Requirements")
    interface_requirements: List[str] = Field(default_factory=list, description="8. Interface Requirements")
    ui_ux_requirements: List[str] = Field(default_factory=list, description="9. UI/UX Requirements")
    reporting_requirements: List[str] = Field(default_factory=list, description="10. Reporting Requirements")
    audit_and_logging: List[str] = Field(default_factory=list, description="11. Audit & Logging")
    historical_issues: List[str] = Field(default_factory=list, description="12. Historical Issues")
    risk_tolerance: str = Field(default="N/A", description="13. Risk Tolerance")
    conversation_response: Optional[str] = Field(default=None, description="Response if input is a general conversation/question, not a BRD")

class AffectedComponent(BaseModel):
    component_name: str = Field(description="Name of the component (e.g., STDCIF, FCIS_PC_PKG)")
    component_type: str = Field(description="Type: Table, Package, Screen, API, Job")
    nature_of_change: str = Field(description="New, Modify, Deprecate")

class EffortEstimation(BaseModel):
    complexity: str = Field(description="Low, Medium, High")
    person_days: int = Field(description="Estimated person-days")
    justification: str = Field(description="Reason for the estimate")

class GeneratedFile(BaseModel):
    file_name: str = Field(description="Name of the file (e.g., sttm_fund_ext.sql)")
    file_content: str = Field(description="Content of the file")
    file_type: str = Field(description="Type of file (e.g., DLL, DML, INC, PLSQL)")

class CodeGenerationResponse(BaseModel):
    files: List[GeneratedFile]
    summary: str = Field(description="Brief summary of generated code")

class ImpactAssessment(BaseModel):
    affected_components: List[AffectedComponent] = Field(description="List of all technical components touched")
    schema_changes: List[str] = Field(description="SQL changes required (DDL/DML)")
    code_changes: List[str] = Field(description="Files/Packages to be modified")
    effort_estimation: EffortEstimation
    overall_risk: str = Field(description="High/Medium/Low risk score")
    mitigation_strategies: List[str] = Field(description="Technical mitigations for identified risks")
