DOMAIN_SYSTEM_PROMPT = """You are an expert in AI planning and good at writing and fixing PDDL domain files. """

DOMAIN_GENERATE_PROMPT = """You should complete the imcomplete domain pddl file include predicates and actions based on the given planning domain description in natural language. Note that you cannot change the requirements. You need to generate a PDDL domain file for the description without anything else. 

The imcomplete domain pddl is:
{domain_base_pddl}

The domain description is: 
{domain_desc}
"""

DOMAIN_FIX_PROMPT = """The generated PDDL domain file failed to parse or execute. You need to fix it based on the provided error message. Note that you cannot change the requirements. You should generate the correct PDDL domain file without anything else. 

The domain pddl to fix is: 
{domain_pddl}
The error message is:
{error_message}
"""


PROBLEM_SYSTEM_PROMPT = """You are an expert in AI planning and good at writing and fixing PDDL problem files."""

PROBLEM_CONTEXT_DESCRIPTION_GENERATE_PROMPT = """You should simplify the planning problem from the given complex problem description in natural language. You can reduce the amount of objects, iniital and goal state. You need to generate the simplified description for the complex problem in the same natural language style as the original without anything else.

The complex problem description is:
{problem_desc}
"""

PROBLEM_CONTEXT_PDDL_GENERATE_PROMPT = """You will be given a given simplified planning problem description in natural language and a PDDL domain file. You need to convert the problem into a valid PDDL prbloem file based on the domain and pay attention to syntax and semantics. You should generate a PDDL problem file for the description without anything else.

The domain pddl is:
{domain_pddl}

The simplified problem description is:
{problem_context_desc}
"""

PROBLEM_GENERATE_PROMPT = """I want you to solve a planning problems. An example planning problem description in natural language and the problem PDDL file to it will be provided. Now I have a new complex planning problem. You should generate the PDDL problem file for the description based on the given prblem and its PDDL without anything else.

The example problem description is:
{problem_context_desc}

The example problem PDDL is:
{problem_context_pddl}

The complex problem description is:
{problem_desc}
"""

PROBLEM_FIX_PROMPT = """The generated PDDL problem file failed to parse or solve. You need to fix it based on the provided error message. You should generate the correct PDDL problem file without anything else. 

The domain pddl of the problem is:
{domain_pddl}

The problem pddl to fix is:
{problem_pddl}

The error message is:
{error_message}
"""


REVIEW_SYSTEM_PROMPT = """You are an expert in AI planning and good at reviewing PDDL domain and problem files. You can identify errors and suggest improvements from the PDDL files. You should give the concise error message and improvement suggestion for the given PDDL files without anything else.

The domain pddl is:
{domain_pddl}

The problem pddl is:
{problem_pddl}
"""
