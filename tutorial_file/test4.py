import ast
import Levenshtein

def generate_ast(code):
    return ast.parse(code)

def calculate_edit_distance(ast1, ast2):
    return Levenshtein.distance(ast.dump(ast1), ast.dump(ast2))

def calculate_group_center(group, codes):
    # グループの中心点として各ASTの平均を計算
    center_ast = ast.parse("")
    for index in group:
        center_ast = ast.fix_missing_locations(
            ast.increment_lineno(
                ast.fix_missing_locations(
                    ast.Module(body=center_ast.body + generate_ast(codes[index]).body)
                )
            )
        )
    
    return center_ast

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

def calculate_distances_to_center(grouped_codes, codes):
    distances = {}
    
    for group in grouped_codes:
        center_ast = calculate_group_center(group, codes)
        
        for index in group:
            code_ast = generate_ast(codes[index])
            distance_to_center = calculate_edit_distance(center_ast, code_ast)
            distances[index] = distance_to_center
    
    return distances

# テスト用のコードサンプル
code1 = """
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'show_name', 'images', 'self_intro', 'search_word_1', 'search_word_2', 'search_word_3')
"""
code2 = """
class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
"""
code3 = "for i in range(10): print(i)"
code4 = "print('Hello, world!')"

codes = [code1, code2, code3, code4]
threshold = 5  # 編集距離の閾値

# ASTを生成してグループ化
grouped_codes = group_codes_by_similarity(codes, threshold)

# 各コードとそのグループの中心点との距離を計算
distances_to_center = calculate_distances_to_center(grouped_codes, codes)

print("Grouped Codes:", grouped_codes)
print("Distances to Center:", distances_to_center)
