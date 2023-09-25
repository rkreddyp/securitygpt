from typing import List, Optional, Type, Union
from enum import Enum, auto
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field, create_model
import openai, boto3, requests, json

from schema.schema_base_prompt import SystemMessage, UserMessage, PromptContext, ChatCompletionMessage, MessageRole, Message


class PromptCVERole(BaseModel):
    role_string: str = Field(default="na")
    role_string = """ 
    # Your Role
     You are an excellent information security researcher, who can research vulnerabilities and exploits in software and hardware.
    
     """
    @property
    def return_string(self):
        return self.role_string
   

class PromptCVETask(BaseModel):
    task_string: str = Field(default="na")
    task_string = """ 
    # Your Task
    Your task is to look at given CVE vulnerability texts from national vulnerability database and 
    MITRE, vendors such as Ubuntu and Amazon and a) come up with a summary of the vulnerability, b) come up with a list of remediation tactics
    and techniques that a company can employ to remediate and/or mitigate the vulnerabilities.
    """
    @property
    def return_string(self):
        return self.task_string

# may be goal
class PromptCVEOutput(BaseModel):
    output_string: str = Field(default="na")
    output_string = """ 
    # Your response 
    Your response should be a verdict on the email whether its malicious email or not,
     with along with reasons.  Each of the reasons should be a probability that its a CVE
     because of that reason.  The response should be in json format. 

    """
    @property
    def return_string(self):
        return self.output_string
        
class PromptCVEExample(BaseModel):
    example_string: str = Field(default="na")
    example_string = """ 
    
    # Example response:
    ```
        {{
            "verdict": "CVEing",
            "CVE_characterestic": {{
                "urgency": 8,
                "lack_of_detail": 8,
                "attachments": 8,
                "generic_salutation": 8,
                "unusual_requests": 8,
                "spelling_and_grammar": 8
            }},
            "over_all_confidence": 8,
            "attack_technique": "spear CVEing"

        }}
        ```
    """
    @property
    def return_string(self):
        return self.example_string
    
class PromptCVEInputString(BaseModel):
    input_string: str = Field(default="na")
    input_string = """ 
    # Email Content
    {email_text}
    """
    @property
    def return_string(self):
        return self.input_string
    
class PrompCVETips(BaseModel):
    tips_string: str = Field(default="na")
    tips_string = """ 
    # Tips  
    Look at the email for the following  attack techniques for business email compromise - - Exploiting Trusted Relationships
    - To urge victims to take quick action on email requests, attackers make a concerted effort to exploit an existing trusted relationship. Exploitation can take many forms, such as a vendor requesting invoice payments, an executive requesting iTunes gift cards, or an [employee sharing new payroll direct deposit details.
    - Replicating Common Workflows
        - An organization and its employees execute an endless number of business workflows each day, many of which rely on automation, and many of which are conducted over email. The more times employees are exposed to these workflows, the quicker they execute tasks from muscle memory. BEC attacks [try to replicate these day-to-day workflows]to get victims to act before they think.
    - Compromised workflows include:
        - Emails requesting a password reset
        - Emails pretending to share files and spreadsheets
        - Emails from commonly used apps asking users to grant them access
    - Suspicious Attachments
        - Suspicious attachments in email attacks are often associated with malware. However, attachments used in BEC attacks forego malware in exchange for fake invoices and other social engineering tactics that add to the conversation’s legitimacy. These attachments are lures designed to ensnare targets further.
    - Socially Engineered Content and Subject Lines
        - BEC emails often rely on subject lines that convey urgency or familiarity and aim to induce quick action.
        - Common terms used in subject lines include:
            - Request
            - Overdue
            - Hello FirstName
            - Payments
            - Immediate Action
        - Email content often follows along the same vein of trickery, with manipulative language that pulls strings to make specific, seemingly innocent requests. Instead of using phishing links, BEC attackers use language as the payload.
    - Leveraging Free Software
        - Attackers make use of freely available software to lend BEC scams an air of legitimacy and help emails sneak past security technologies that block known bad links and domains.
        - For example, attackers use SendGrid to create spoofed email addresses and Google Sites to stand up phishing pages.
    - Spoofing Trusted Domains      

    The following are the categories of business email compromise - - CEO Fraud
    - Attackers impersonate the CEO or executive of a company. As the CEO, they request that an employee within the accounting or finance department transfer funds to an attacker-controlled account.
    - Lawyer Impersonation
        - Attackers pose as a lawyer or legal representative, often over the phone or email. These attacks’ common targets are lower-level employees who may not have the knowledge or experience to question the validity of an urgent legal request.
    - Data Theft
        - Data theft attacks typically target HR personnel to obtain personal information about a company’s CEO or other high-ranking executives. The attackers can then use the data in future attacks like CEO fraud.
    - Email Account Compromise
        - In an [email account compromise]attack, an employee’s email account is hacked and used to request payments from vendors. The money is then sent to attacker-controlled bank accounts.
    - Vendor Email Compromise
        - Companies with foreign suppliers are common targets of [vendor email compromise] Attackers pose as suppliers, request payment for a fake invoice, then transfer the money to a fraudulent account.



    """
    @property
    def return_string(self):
        return self.tips_string

class PromptPhishReflect(BaseModel):
    reflect_string: str = Field(default="na")
    reflect_string = """ 
      
      - Think step by step. Reflect to see if you are producing the correct and complete json format.  if not, then you need to fix your repsponse. 
    
    """
    @property
    def return_string(self):
        return self.reflect_string