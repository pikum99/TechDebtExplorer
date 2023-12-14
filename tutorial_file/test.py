import ast
import Levenshtein

def generate_ast(source_code):
    """
    ソースコードからASTを生成する関数
    """
    try:
        parsed_ast = ast.parse(source_code)
        return parsed_ast
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return None

def calculate_ast_edit_distance(ast1, ast2):
    """
    2つのASTの編集距離を計算する関数
    """
    if ast1 is None or ast2 is None:
        return float('inf')  # エラーケースなどで距離が無限大になるようにする

    # ASTを文字列に変換してLevenshtein距離を計算
    ast_str1 = ast.dump(ast1)
    ast_str2 = ast.dump(ast2)
    edit_distance = Levenshtein.distance(ast_str1, ast_str2)

    return edit_distance

source_code1 = "def add_numbers(a, b):"
source_code2 = "def add_numbers(a, b):"


# ASTを生成
ast1 = generate_ast(source_code1)
ast2 = generate_ast(source_code2)

# ASTの編集距離を計算
edit_distance = calculate_ast_edit_distance(ast1, ast2)

# 結果を出力
print(f"AST Edit Distance: {edit_distance}")
