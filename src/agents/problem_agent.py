import os
from typing import Optional
from src.core.llm import LLM
from src.core.agent import Agent
from src.info import Domain
from src.util import postprocess
from src.tool import syntax_validate

from src.agents.prompt import (
    PROBLEM_SYSTEM_PROMPT, PROBLEM_CONTEXT_DESCRIPTION_GENERATE_PROMPT,
    PROBLEM_CONTEXT_PDDL_GENERATE_PROMPT,
    PROBLEM_GENERATE_PROMPT,
    PROBLEM_FIX_PROMPT
)


class ProblemAgent(Agent):
    def __init__(
        self, 
        llm: LLM, 
        domain: Domain,
        system_prompt: Optional[str] = None,
    ):
        super().__init__(llm, system_prompt)
        self.system_prompt = PROBLEM_SYSTEM_PROMPT
        self.context_description_generate_prompt = PROBLEM_CONTEXT_DESCRIPTION_GENERATE_PROMPT
        self.context_pddl_generate_prompt = PROBLEM_CONTEXT_PDDL_GENERATE_PROMPT
        self.generate_prompt = PROBLEM_GENERATE_PROMPT
        self.fix_prompt = PROBLEM_FIX_PROMPT

        self.domain = domain

    def set_problem_index(self, index):
        self.index = index
        self.clear_history()

    def _create_context_description_generate_prompt(self):
        problem_desc_file = self.domain.get_problem_desc_file(self.index)
        with open(problem_desc_file, "r") as f:
            problem_desc = f.read()
        prompt = self.context_description_generate_prompt.format(problem_desc=problem_desc)
        return prompt
    
    def _create_context_pddl_generate_prompt(self):
        domain_pddl_file = self.domain.get_domain_pddl_file()
        problem_context_desc_file = self.domain.get_problem_context_desc_file()
        with open(domain_pddl_file, "r") as f:
            domain_pddl = f.read()
        with open(problem_context_desc_file, "r") as f:
            problem_context_desc = f.read()
        prompt = self.context_pddl_generate_prompt.format(
            domain_pddl=domain_pddl,
            problem_context_desc=problem_context_desc
        )
        return prompt

    def _create_generate_prompt(self):
        problem_context_desc_file = self.domain.get_problem_context_desc_file()
        problem_context_pddl_file = self.domain.get_problem_context_pddl_file()
        problem_desc_file = self.domain.get_problem_desc_file(self.index)
        with open(problem_context_desc_file, "r") as f:
            problem_context_desc = f.read()
        with open(problem_context_pddl_file, "r") as f:
            problem_context_pddl = f.read()
        with open(problem_desc_file, "r") as f:
            problem_desc = f.read()
        prompt = self.generate_prompt.format(
            problem_context_desc=problem_context_desc,
            problem_context_pddl=problem_context_pddl,
            problem_desc=problem_desc,
        )
        return prompt

    def _create_fix_prompt(self, error_message, example=False):
        if example:
            domain_pddl_file = self.domain.get_problem_context_pddl_file()
            problem_pddl_file = self.domain.get_problem_context_desc_file()
        else:
            domain_pddl_file = self.domain.get_domain_pddl_file()
            problem_pddl_file = self.domain.get_problem_pddl_file(self.index)
        with open(domain_pddl_file, "r") as f:
            domain_pddl = f.read()
        with open(problem_pddl_file, "r") as f:
            problem_pddl = f.read()
        prompt = self.fix_prompt.format(
            domain_pddl=domain_pddl,
            problem_pddl=problem_pddl, 
            error_message=error_message)
        return prompt

    def run(self, input_text):
        self.add_message(f"TASK:\n{input_text}")
        prompt = "\n".join(self.history)
        output_text = self.llm.query(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )
        return output_text
    
    def generate_context_description(self):
        context_description_file = self.domain.get_problem_context_desc_file()
        if os.path.exists(context_description_file):
            with open(context_description_file, "r") as f:
                context_description = f.read()
        else:
            prompt = self._create_context_description_generate_prompt()
            context_description = postprocess(self.run(prompt))
            with open(context_description_file, "w") as f:
                f.write(context_description)
        return context_description
    
    def generate_context_pddl(self):
        context_pddl_file = self.domain.get_problem_context_pddl_file()
        if os.path.exists(context_pddl_file):
            with open(context_pddl_file, "r") as f:
                context_pddl = f.read()
        else:
            prompt = self._create_context_pddl_generate_prompt()
            context_pddl = postprocess(self.run(prompt))
            with open(context_pddl_file, "w") as f:
                f.write(context_pddl)
        return context_pddl
    
    def generate_problem(self):
        self.clear_history()
        problem_pddl_file = self.domain.get_problem_pddl_file(self.index)
        if os.path.exists(problem_pddl_file):
            with open(problem_pddl_file, "r") as f:
                problem_pddl = f.read()
        else:
            prompt = self._create_generate_prompt()
            problem_pddl = postprocess(self.run(prompt))
            with open(problem_pddl_file, "w") as f:
                f.write(problem_pddl)
        return problem_pddl
    
    def fix_problem(self, error_message, example=False):
        self.clear_history()
        if example:
            prompt = self._create_fix_prompt(error_message, example=True)
            problem_pddl_file = self.domain.get_problem_context_pddl_file()
        else:    
            prompt = self._create_fix_prompt(error_message)
            problem_pddl_file = self.domain.get_problem_pddl_file(self.index)
        problem_pddl = postprocess(self.run(prompt))
        with open(problem_pddl_file, "w") as f:
            f.write(problem_pddl)
        return problem_pddl
    
    def parse(self, example=False):
        if example:
            return syntax_validate(
                self.domain.get_domain_pddl_file(),
                self.domain.get_problem_context_pddl_file()
            )
        else:
            return syntax_validate(
                self.domain.get_domain_pddl_file(),
                self.domain.get_problem_pddl_file(self.index)   
            )
        
