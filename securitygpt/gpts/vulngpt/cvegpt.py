import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from schema.schema_cve import CVEStructureJson, CVERemediationJson
from prompts.prompts_vuln import PromptCVERole, PromptCVETask
from tools.openai import chat_complete
from utils import cve_utils

def summmarize_cve(cve_id:str):

    paragraphs = cve_utils.run(cve_id)

    paragraphs_text = ' '.join(paragraphs)

    system_content =  PromptCVERole().return_string
    
    prompt_string = """ 
        your goal is to analyze the text and summarize the text, the return is json.
        """  + paragraphs_text
    
    completion = chat_complete (model = "gpt-3.5-turbo-16k", system_content=system_content, user_content=prompt_string, functions = [CVEStructureJson.openai_schema] ).completion


    return completion["choices"][0].message.function_call.arguments