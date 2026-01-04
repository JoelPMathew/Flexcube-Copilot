from src.core.llm import MistralLLM
from src.core.models import ImpactAssessment, CodeGenerationResponse, GeneratedFile

class CodeGenerationAgent:
    def __init__(self, llm: MistralLLM):
        self.llm = llm
        self.system_prompt = """
        You are an Expert Oracle PL/SQL Developer specialized in Oracle Flexcube Investor Services (FCIS).
        Your task is to generate production-ready code based on the Technical Impact Assessment provided.
        
        Guidelines:
        1. **Naming Conventions**: Follow strict Oracle naming conventions (e.g., packages ending in _PKG, tables in _MASTER/_EXT).
        2. **Modularity**: Create separate files for Tables (DDL), Packages (SPC/SQL), and Data (DML).
        3. **Safety**: Always include `CREATE OR REPLACE` for logic and `CREATE TABLE IF NOT EXISTS` patterns (or standard exception handling) for DDL.
        4. **Comments**: Add detailed comments explaining the business logic.
        5. **Error Handling**: Implement standard FCIS exception handling.
        
        Input: Impact Assessment JSON.
        Output: A list of files with their content.
        """

    def generate(self, impact: ImpactAssessment) -> CodeGenerationResponse:
        prompt = f"""
        {self.system_prompt}
        
        --- IMPACT ASSESSMENT START ---
        {impact.model_dump_json(indent=2)}
        --- IMPACT ASSESSMENT END ---
        
        Generate the required PL/SQL code, DDLs, and DMLs now.
        """
        
        # We use strict JSON generation for the file list
        return self.llm.generate_structured(prompt, CodeGenerationResponse)
