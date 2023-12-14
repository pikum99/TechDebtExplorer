import ast
import Levenshtein

def generate_ast(code):
    return ast.parse(code)

def calculate_edit_distance(ast1, ast2):
    # ここでASTの比較を行う
    # 例: ast.dump(ast1) と ast.dump(ast2) を比較する
    return Levenshtein.distance(ast.dump(ast1), ast.dump(ast2))

def group_codes_by_similarity(codes, threshold):
    groups = []

    for i, code1 in enumerate(codes):
        ast1 = generate_ast(code1)
        
        # 新しいグループを作成
        new_group = [i]
        
        for j, code2 in enumerate(codes):
            if i != j:  # 同じコードとの比較は不要
                ast2 = generate_ast(code2)
                distance = calculate_edit_distance(ast1, ast2)
                
                if distance <= threshold:
                    new_group.append(j)
        
        # 既存のグループに含まれるかどうかを確認
        merged = False
        for group in groups:
            if any(index in group for index in new_group):
                group.update(new_group)
                merged = True
                break
        
        # 新しいグループを追加
        if not merged:
            groups.append(set(new_group))
    
    return [list(group) for group in groups]

# テスト用のコードサンプル
code1 = "print('Hello, world!')"
code2 = "print('Hi there!')"
code3 = "for i in range(10): print(i)"
code4 = "print('Hello, world!')"

codes = [code1, code2, code3, code4]
threshold = 5  # 編集距離の閾値

# ASTを生成してグループ化
grouped_codes = group_codes_by_similarity(codes, threshold)

print("Grouped Codes:", grouped_codes)
