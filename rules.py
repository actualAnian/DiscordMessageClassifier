import ast
import rules as  R

def is_in_specified_channels(message, channels):
    if message.channel.id not in channels:
        return False
    return True

def is_in_specified_forums(message, forums):
    if "thread" not in message.channel.type.name:
        return False
    if message.channel.parent_id not in forums:
        return False
    return True

def is_in_specified_categories(message, categories):
    if message.channel.category_id == None or message.channel.category_id not in categories:
        return False
    return True

def has_specified_role(message, roles):
    for role_id in roles:
        role = message.guild.get_role(role_id)
        if role in message.author.roles:
            return True
    return False

def eval_node(node, context, message):
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return all(eval_node(v, context, message) for v in node.values)
        elif isinstance(node.op, ast.Or):
            return any(eval_node(v, context, message) for v in node.values)
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not eval_node(node.operand, context, message)
    elif isinstance(node, ast.Name):
        name = node.id.lower()
        data = context["rules"][name]
        match data["type"]:
            case "is_in_specified_channels":
                return R.is_in_specified_channels(message, data["channels"])
            case "is_in_specified_forums":
                return R.is_in_specified_forums(message, data["forums"])
            case "is_in_specified_categories":
                return R.is_in_specified_categories(message, data["categories"])
            case "has_specified_role":
                return R.has_specified_role(message, data["roles"])
            case _:
                raise ValueError(f"Unknown variable '{name}' in expression.")
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def evaluate_expression(context, message):
    """
    Evaluate a logical expression string like:
        ((channels AND forums) OR categories)
    where each variable corresponds to a function call in R.
    """
    expr_str = context["rules"]["rule_expression"]
    # Normalize to Python boolean syntax
    expr_str = expr_str.replace("AND", "and").replace("OR", "or").replace("NOT", "not")

    # Parse safely into an AST
    tree = ast.parse(expr_str, mode="eval")

    return eval_node(tree.body, context, message)
