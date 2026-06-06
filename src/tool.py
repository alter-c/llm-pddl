import subprocess
import re
from typing import Optional

def syntax_validate(
    domain_file: str, 
    problem_file: Optional[str] = None
) -> tuple[bool, str]:
    parser = "./VAL/bin/Parser"
    if problem_file:
        cmd = [parser, domain_file, problem_file]
    else:
        cmd = [parser, domain_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    warning_pattern = r"Warning:\s*(.*)"
    error_pattern = r"Error:\s*(.*)"
    warning_list = re.findall(warning_pattern, output)
    error_list = re.findall(error_pattern, output)
    if warning_list or error_list:
        messages = []
        if warning_list:
            messages.append("Warnings:")
            messages.extend(warning_list)
        if error_list:
            messages.append("Errors:")
            messages.extend(error_list)
        return False, "\n".join(messages)
    else:
        return True, "Syntax is valid."




