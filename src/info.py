import os
import glob
from src.util import postprocess

DOMAINS = [
    "barman",
    "blocksworld",
    "floortile",
    "grippers",
    "storage",
    "termes",
    "tyreworld"
]

class Domain:
    def __init__(self, name):
        assert name in DOMAINS, \
            f"Domain {name} not found."
        self.name = name
        self.data_dir = os.path.join("./datasets", name)
        self.exp_dir = os.path.join("./experiments/test", name)
        os.makedirs(self.exp_dir, exist_ok=True)

        self.problems = self._grab_problems()
    
    def _grab_problems(self):
        nls = []
        for fn in glob.glob(os.path.join(self.data_dir, "*.nl")):
            fn_ = fn.split("/")[-1]
            if "domain" not in fn_:
                nls.append(fn)
        return sorted(nls)

    def get_domain_desc_file(self):
        return os.path.join(self.data_dir, "domain.nl")

    def get_domain_base_pddl_file(self):
        return os.path.join(self.data_dir, "base_domain.pddl")

    def get_domain_pddl_file(self):
        return os.path.join(self.exp_dir, "domain.pddl")
    
    def get_problem_context_desc_file(self):
        return os.path.join(self.exp_dir, "p_example.nl")
    
    def get_problem_context_pddl_file(self):
        return os.path.join(self.exp_dir, "p_example.pddl")
    
    def get_problem_desc_file(self, index):
        return self.problems[index]
    
    def get_problem_pddl_file(self, index):
        problem_desc_file = self.get_problem_desc_file(index)
        file_name = problem_desc_file.split("/")[-1].replace(".nl", ".pddl")
        return os.path.join(self.exp_dir, file_name)
