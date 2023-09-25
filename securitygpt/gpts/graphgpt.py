
from schema.schema_cve import CVEStructureJson, CVERemediationJson
from prompts.prompts_knowledge_graph import PromptKnowledgeGraph
from schema.schema_knowledge_graph import KnowledgeGraph, Node, Edge
from utils.url_utils import headless_browser_utils
from tools.openai import chat_complete
from typing import List, Dict, Any, Optional
from schema.schema_base_openai import openai_function
from utils import graph_utils
from selenium.webdriver.common.by import By
import ast


def fetch_text(url) -> List[str]:
        text_arr = []
        try :

            browser = headless_browser_utils.initiate_driver_return_browser(url)
            el = browser.find_element(By.TAG_NAME,'body')
            for text in (el.text).split('\n'):
                if len (text) > 200:
                    #print (url)
                    #print ("fetchtext --", text)
                    text_arr.append(text)
            return ".".join (text_arr)
        except Exception as e:
            
            print ("exceptin in fetch_text")
            return "NA"


def draw_threat_graph(url:str, objective:str):
    prompt_content = PromptKnowledgeGraph().return_string
    system_content = "You are an an awesome information researcher and knowledge graph developer"

    kg_schema = openai_function.openai_schema (KnowledgeGraph)
    kc = fetch_text(url)
    prompt_string =prompt_content.format(objective = objective, article=kc)
    completion = chat_complete (model = "gpt-3.5-turbo-16k", system_content=system_content, temperature=0.5, user_content=prompt_string, functions = [kg_schema] ).completion

    #st.write (completion)
    dot = graph_utils.visualize_knowledge_graph ( ast.literal_eval (completion['choices'][0].message['function_call']['arguments']) )
    return dot
