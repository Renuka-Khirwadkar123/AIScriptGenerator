import os
from datetime import datetime


def convert_step_to_qmate(step: str, mode: str = "ui5") -> str:
    step = step.lower().strip()

    def format_selector(target: str) -> str:
        if mode == "non-ui5":
            return f'$("#{target}")'
        else:
            return f'ui5.control({{ selector: {{ id: "{target}" }} }})'

    if step.startswith("click on http") or step.startswith("open http") or "www." in step:
        url = step.split("on")[-1].strip() if "on" in step else step.split("open")[-1].strip()
        return f'await browser.url("{url}");'

    elif "enter" in step and "in" in step:
        try:
            value = step.split("enter")[1].split("in")[0].strip()
            field = step.split("in")[1].strip().replace(" ", "")
            if mode == "non-ui5":
                return f'await {format_selector(field)}.setValue("{value}");'
            else:
                return f'await {format_selector(field)}.setValue("{value}");'
        except:
            return f'// Could not parse input step: {step}'

    elif step.startswith("click on"):
        target = step.replace("click on", "").strip().replace(" ", "")
        if mode == "non-ui5":
            return f'await {format_selector(target)}.click();'
        else:
            return f'await {format_selector(target)}.press();'

    elif step.startswith("select") or step.startswith("choose"):
        try:
            value = step.split(" ")[1]
            field = step.split("from")[1].strip().replace(" ", "")
            return f'await {format_selector(field)}.setSelected("{value}");'
        except:
            return f'// Could not parse selection step: {step}'

    else:
        return f'// Unrecognized step: {step}'


def generate_test_script_from_steps(steps: list[str], mode: str = "ui5") -> str:
    action_lines = [convert_step_to_qmate(step, mode) for step in steps]

    script = f"""\
describe("QMate Auto-Generated Test", () => {{
  it("performs steps from natural language", async () => {{
    {chr(10).join("    " + line for line in action_lines)}
  }});
}});
"""
    return script


def save_script(script_code: str, directory: str = "tests/generated") -> str:
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"auto_generated_{timestamp}.test.js"
    path = os.path.join(directory, filename)
    with open(path, "w") as f:
        f.write(script_code)
    return path
