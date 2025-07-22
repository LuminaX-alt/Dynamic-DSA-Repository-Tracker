pip install radon
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def analyze_code_complexity(code: str) -> str:
    try:
        complexity_results = cc_visit(code)
        mi_score = mi_visit(code, True)
        result = [f"Cyclomatic Complexity: {node.name} - {node.complexity}" for node in complexity_results]
        result.append(f"Maintainability Index: {mi_score:.2f}")
        return "\n".join(result)
    except Exception as e:
        return f"Error analyzing complexity: {e}"
pip install pygments
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from pygments import lex

def count_tokens(code: str, language: str = "python") -> str:
    lexer = get_lexer_by_name(language.lower())
    token_counts = {}
    for tok_type, _ in lex(code, lexer):
        token_name = str(tok_type)
        token_counts[token_name] = token_counts.get(token_name, 0) + 1
    summary = "\n".join([f"{k}: {v}" for k, v in token_counts.items() if v > 1])
    return summary or "No significant tokens found."
