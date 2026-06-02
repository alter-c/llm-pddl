import argparse
import glob
import os
import time
import backoff

import openai

FAST_DOWNWARD_ALIAS = "lama-first"

DOMAINS = [
    "barman",
    "blocksworld",
    "floortile",
    "grippers",
    "storage",
    "termes",
    "tyreworld",
    "manipulation"
]


def postprocess(x):
    return x.strip()


def get_cost(x):
    splitted = x.split()
    counter = 0
    found = False
    cost = 1e5
    for i, xx in enumerate(splitted):
        if xx == "cost":
            counter = i
            found = True
            break
    if found:
        cost = float(splitted[counter+2])
    return cost


class Planner:
    def __init__(self, model="deepseek"):
        self.available_models = ["openai", "deepseek"]
        self.model = model
        assert self.model in self.available_models, f"{self.model} is not in {self.available_models}"

    def query(self, prompt_text):
        server_flag = 0
        server_cnt = 0
        result_text = ""
        while server_cnt < 10:
            try:
                if self.model == "openai":
                    client = openai.OpenAI(
                        api_key=os.getenv("OPENAI_API_KEY"),
                        base_url="https://api.bianxie.ai/v1"
                    )
                    @backoff.on_exception(backoff.expo, openai.RateLimitError)
                    def completions_with_backoff(**kwargs):
                        return client.chat.completions.create(**kwargs)

                    response = completions_with_backoff(
                        model="gpt-5.1",
                        temperature=0.0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt_text},
                        ],
                    )
                    result_text = response.choices[0].message.content
                elif self.model == "deepseek":
                    client = openai.OpenAI(
                        api_key=os.getenv("DEEPSEEK_API_KEY"),
                        base_url="https://api.deepseek.com"
                    )
                    @backoff.on_exception(backoff.expo, openai.RateLimitError)
                    def completions_with_backoff(**kwargs):
                        return client.chat.completions.create(**kwargs)

                    response = completions_with_backoff(
                        model="deepseek-v4-flash",
                        temperature=0.0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt_text},
                        ],
                    )
                    result_text = response.choices[0].message.content
                else:
                    raise ValueError(f"{self.model} model not supported.")
                server_flag = 1
                if server_flag:
                    break
            except Exception as e:
                server_cnt += 1
                print(e)
        return result_text

    def parse_result(self, pddl_string):
        try:
           pddl_string = pddl_string.replace("```",'').replace("pddl",'').replace("lisp",'')
        except:
           raise Exception("[error] cannot find ```pddl-file``` in the pddl string")
        return pddl_string

    def create_llm_ic_pddl_prompt(self, task_nl, domain_pddl, context):
        context_nl, context_pddl, context_sol = context
        prompt = f"I want you to solve planning problems. " + \
                 f"An example planning problem is: \n {context_nl} \n" + \
                 f"The problem PDDL file to this problem is: \n {context_pddl} \n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Provide me with the problem PDDL file that describes " + \
                 f"the new planning problem directly without further explanations? Only return the PDDL file. Do not return anything else."
        return prompt


class Domain:
    def __init__(self):
        self.context = ("p_example.nl", "p_example.pddl", "p_example.sol")
        self.tasks = []

        self.grab_tasks()

    def grab_tasks(self):
        path = f"./domains/{self.name}"
        nls = []
        for fn in glob.glob(f"{path}/*.nl"):
            fn_ = fn.split("/")[-1]
            if "domain" not in fn_ and "p_example" not in fn_:
                if os.path.exists(fn.replace("nl", "pddl")):
                    nls.append(fn_)
        sorted_nls = sorted(nls)
        self.tasks = [(nl, nl.replace("nl", "pddl")) for nl in sorted_nls]

    def __len__(self):
        return len(self.tasks)

    def get_task_suffix(self, i):
        nl, pddl = self.tasks[i]
        return f"{self.name}/{pddl}"

    def get_task_file(self, i):
        nl, pddl = self.tasks[i]
        return f"./domains/{self.name}/{nl}", f"./domains/{self.name}/{pddl}"

    def get_task(self, i):
        nl_f, pddl_f = self.get_task_file(i)
        with open(nl_f, 'r') as f:
            nl = f.read()
        with open(pddl_f, 'r') as f:
            pddl = f.read()
        return postprocess(nl), postprocess(pddl)

    def get_context(self):
        nl_f   = f"./domains/{self.name}/{self.context[0]}"
        pddl_f = f"./domains/{self.name}/{self.context[1]}"
        sol_f  = f"./domains/{self.name}/{self.context[2]}"
        with open(nl_f, 'r') as f:
            nl   = f.read()
        with open(pddl_f, 'r') as f:
            pddl = f.read()
        with open(sol_f, 'r') as f:
            sol  = f.read()
        return postprocess(nl), postprocess(pddl), postprocess(sol)

    def get_domain_pddl(self):
        domain_pddl_f = self.get_domain_pddl_file()
        with open(domain_pddl_f, 'r') as f:
            domain_pddl = f.read()
        return postprocess(domain_pddl)

    def get_domain_pddl_file(self):
        domain_pddl_f = f"./domains/{self.name}/domain.pddl"
        return domain_pddl_f

    def get_domain_nl(self):
        domain_nl_f = self.get_domain_nl_file()
        try:
            with open(domain_nl_f, 'r') as f:
                domain_nl = f.read()
        except:
            domain_nl = "Nothing"
        return postprocess(domain_nl)

    def get_domain_nl_file(self):
        domain_nl_f = f"./domains/{self.name}/domain.nl"
        return domain_nl_f


class Barman(Domain):
    name = "barman"


class Floortile(Domain):
    name = "floortile"


class Termes(Domain):
    name = "termes"


class Tyreworld(Domain):
    name = "tyreworld"


class Grippers(Domain):
    name = "grippers"


class Storage(Domain):
    name = "storage"


class Blocksworld(Domain):
    name = "blocksworld"


class Manipulation(Domain):
    name = "manipulation"


def llm_ic_pddl_planner(args, planner, domain):
    """
    Our method:
        context: (task natural language, task problem PDDL)
        Condition on the context (task description -> task problem PDDL),
        LLM will be asked to provide the problem PDDL of a new task description.
        Then, we use a planner to find the near optimal solution, and translate
        that back to natural language.
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_ic_pddl/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_ic_pddl/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_ic_pddl/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task)
    prompt             = planner.create_llm_ic_pddl_prompt(task_nl, domain_pddl, context)
    raw_result         = planner.query(prompt)
    task_pddl_         = planner.parse_result(raw_result)

    # B. write the problem file into the problem folder
    task_pddl_file_name = f"./experiments/run{args.run}/problems/llm_ic_pddl/{task_suffix}"
    with open(task_pddl_file_name, "w") as f:
        f.write(task_pddl_)
    time.sleep(1)

    ## C. run fastforward to plan
    plan_file_name = f"./experiments/run{args.run}/plans/llm_ic_pddl/{task_suffix}"
    sas_file_name  = f"./experiments/run{args.run}/plans/llm_ic_pddl/{task_suffix}.sas"
    os.system(f"python ./downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--search-time-limit {args.time_limit} --plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{domain_pddl_file} {task_pddl_file_name}")

    # D. collect the least cost plan
    best_cost = 1e10
    best_plan = None
    for fn in glob.glob(plan_file_name):
        with open(fn, "r") as f:
            plans = f.readlines()
            cost = get_cost(plans[-1])
            if cost < best_cost:
                best_cost = cost
                best_plan = "\n".join([p.strip() for p in plans[:-1]])

    # E. translate the plan back to natural language, and write it to result
    end_time = time.time()
    if best_plan:
        print(f"[info] task {task} takes {end_time - start_time} sec, found a plan with cost {best_cost}")
    else:
        print(f"[info] task {task} takes {end_time - start_time} sec, no solution found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-PDDL Planner")
    parser.add_argument('--domain', type=str, choices=DOMAINS, default="blocksworld")
    parser.add_argument('--time-limit', type=int, default=200)
    parser.add_argument('--task', type=int, default=0)
    parser.add_argument('--run', type=int, default=0)
    args = parser.parse_args()

    domain = eval(args.domain.capitalize())()
    planner = Planner()
    llm_ic_pddl_planner(args, planner, domain)