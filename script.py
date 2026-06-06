from src.core.llm import LLM
from src.agents.domain_agent import DomainAgent
from src.agents.problem_agent import ProblemAgent
from src.info import Domain, DOMAINS
from src.util import repeat

from dataclasses import dataclass
import time

@dataclass
class TestConfig:
    model: str
    domain_name: str
    problem_index: int

config = TestConfig(
    model="deepseek-v4-flash",
    domain_name="barman",
    problem_index=0
)

start_time = time.time()

llm = LLM(model=config.model)
domain = Domain(name=config.domain_name)
agent = DomainAgent(llm=llm, domain=domain)
agent.generate_domain()
@repeat(3)
def parse_domain():
    print("Parsing domain...")
    suc, error_message = agent.parse()
    if suc:
        print("Domain generate successfully!")
        return True
    else:
        print("Domain generate failed!")
        print(error_message)
        agent.fix_domain(error_message)
        return False
parse_domain()


problem_agent = ProblemAgent(llm=llm, domain=domain)
problem_agent.set_problem_index(config.problem_index)
problem_agent.generate_context_description()
problem_agent.generate_context_pddl()
@repeat(3)
def parse_context():
    print("Parsing context...")
    suc, error_message = problem_agent.parse(example=True)
    if suc:
        print("Context generate successfully!")
        return True
    else:
        print("Context generate failed!")
        print(error_message)
        problem_agent.fix_problem(error_message, example=True)
        return False
parse_context()

res = problem_agent.generate_problem()
@repeat(3)
def parse_problem():
    print("Parsing problem...")
    suc, error_message = problem_agent.parse()
    if suc:
        print("Problem generate successfully!")
        return True
    else:
        print("Problem generate failed!")
        print(error_message)
        problem_agent.fix_problem(error_message)
        return False
parse_problem()

end_time = time.time()

print(f"Total time: {end_time - start_time:.2f} seconds")