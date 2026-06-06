import os
from typing import Optional
from src.core.llm import LLM
from src.core.agent import Agent
from src.info import Domain
from src.util import postprocess
from src.tool import syntax_validate

from src.agents.prompt import DOMAIN_SYSTEM_PROMPT, DOMAIN_GENERATE_PROMPT, DOMAIN_FIX_PROMPT


class DomainAgent(Agent):
    def __init__(
        self, 
        llm: LLM, 
        domain: Domain,
        system_prompt: Optional[str] = None,
    ):
        super().__init__(llm, system_prompt)
        self.system_prompt = DOMAIN_SYSTEM_PROMPT
        self.generate_prompt = DOMAIN_GENERATE_PROMPT
        self.fix_prompt = DOMAIN_FIX_PROMPT

        self.domain = domain

    def _create_generate_prompt(self):
        domain_desc_file = self.domain.get_domain_desc_file()
        domain_base_pddl_file = self.domain.get_domain_base_pddl_file()
        with open(domain_desc_file, "r") as f:
            domain_desc = f.read()
        with open(domain_base_pddl_file, "r") as f:
            domain_base_pddl = f.read()
        prompt = self.generate_prompt.format(
            domain_base_pddl=domain_base_pddl,
            domain_desc=domain_desc
        )
        return prompt

    def _create_fix_prompt(self, error_message):
        domain_pddl_file = self.domain.get_domain_pddl_file()
        with open(domain_pddl_file, "r") as f:
            domain_pddl = f.read()
        prompt = self.fix_prompt.format(domain_pddl=domain_pddl, error_message=error_message)
        return prompt

    def run(self, input_text):
        self.add_message(f"TASK:\n{input_text}")
        prompt = "\n".join(self.history)
        output_text = self.llm.query(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        return output_text

    def generate_domain(self):
        domain_pddl_file = self.domain.get_domain_pddl_file()
        if os.path.exists(domain_pddl_file):
            with open(domain_pddl_file, "r") as f:
                domain_pddl = f.read()
        else:
            prompt = self._create_generate_prompt()
            domain_pddl = postprocess(self.run(prompt))
            with open(domain_pddl_file, "w") as f:
                f.write(domain_pddl)
        return domain_pddl
    
    def fix_domain(self, error_message):
        self.clear_history()
        prompt = self._create_fix_prompt(error_message)
        domain_pddl = postprocess(self.run(prompt))
        domain_pddl_file = self.domain.get_domain_pddl_file()
        with open(domain_pddl_file, "w") as f:
            f.write(domain_pddl)
        return domain_pddl
    
    def parse(self):
        return syntax_validate(self.domain.get_domain_pddl_file())
        
