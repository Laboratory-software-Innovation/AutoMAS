import ast

def get_react_agent_summary(code_source):
    if not isinstance(code_source, str) or not code_source.strip():
        return {"error": "Empty input"}

    if code_source.count("'''") % 2 != 0: 
        code_source += "\n'''"

    try:
        tree = ast.parse(code_source.strip())
        tool_details = []
        agent_config = {"intent": "Unknown", "logic_flow": []}

        for node in ast.walk(tree):
            func_id = ""
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_id = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_id = node.func.attr

                if func_id in ['Tool', 'StructuredTool']:
                    tool_info = {"name": "unknown", "description": "none"}
                    for kw in node.keywords:
                        if kw.arg == 'name':
                            tool_info['name'] = ast.unparse(kw.value).strip("'\"")
                        if kw.arg == 'description':
                            desc = ast.unparse(kw.value).strip("'\"")
                            tool_info['description'] = desc.split('.')[0] + "."
                    tool_details.append(tool_info)

                if func_id == 'create_react_agent':
                    agent_config['intent'] = "Reasoning and tool execution."
                    agent_config['logic_flow'] = ["Input ➔ Thought ➔ Action ➔ Observation ➔ Final Answer"]
                    if len(node.args) >= 2:
                        agent_config['tools_variable'] = ast.unparse(node.args[1])
                    for kw in node.keywords:
                        if kw.arg == 'tools':
                            agent_config['tools_variable'] = ast.unparse(kw.value)

                if func_id == 'AgentExecutor':
                    for kw in node.keywords:
                        if kw.arg == 'max_iterations':
                            agent_config['max_loops'] = ast.unparse(kw.value)
                
                if func_id in ['StateGraph', 'Graph']:
                    agent_config['logic_flow'] = []

            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == 'add_edge' and len(node.args) >= 2:
                    start_node = ast.unparse(node.args[0]).strip("'\"")
                    end_node = ast.unparse(node.args[1]).strip("'\"")
                    agent_config['logic_flow'].append(f"{start_node} ➔ {end_node}")
                
                if node.func.attr == 'add_conditional_edges' and len(node.args) >= 1:
                    source = ast.unparse(node.args[0]).strip("'\"")
                    agent_config['logic_flow'].append(f"{source} ➔ [Conditional Branching]")

            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                target_name = ""
                if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                    target_name = node.targets[0].id
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    target_name = node.target.id
                
                if target_name.lower() in ['prompt', 'instructions', 'system_message']:
                    val = ast.unparse(node.value).strip("'\"")
                    agent_config['intent'] = (val[:97] + '...') if len(val) > 100 else val

        if not agent_config['logic_flow']:
            agent_config['logic_flow'] = ["Sequential Execution (No graph detected)"]

        return {
            "Agent Intent": agent_config.get('intent'),
            "Architecture": "Graph-Based" if "➔" in "".join(agent_config['logic_flow']) and "ReAct" not in agent_config['intent'] else "ReAct (Fixed Cyclic)",
            "Active Tools (Logic Nodes)": tool_details,
            "Logic Flow": agent_config['logic_flow'],
            "Constraints": f"Max Iterations: {agent_config.get('max_loops', 'default')}"
        }

    except SyntaxError as e:
        return {"error": "SyntaxError", "line": e.lineno, "msg": str(e)}
    except Exception as e:
        return {"error": "Unexpected Error", "msg": str(e)}
