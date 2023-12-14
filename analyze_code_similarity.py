import ast
import Levenshtein
import csv


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


def calculate_group_distances(grouped_codes, codes):
    group_distances = []

    for group in grouped_codes:
        distances = []
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                ast1 = generate_ast(codes[group[i]])
                ast2 = generate_ast(codes[group[j]])
                distance = calculate_edit_distance(ast1, ast2)
                distances.append(distance)
        # グループ内の平均編集距離を計算
        avg_distance = sum(distances) / len(distances) if distances else 0
        group_distances.append(avg_distance)

    return group_distances


def calculate_inter_group_distances(grouped_codes, codes):
    inter_group_distances = []

    # 各グループの「中心」を計算
    group_centers = []
    for group in grouped_codes:
        asts = [generate_ast(codes[i]) for i in group]
        ast_strs = [ast.dump(a) for a in asts]
        center = sum(len(ast_str) for ast_str in ast_strs) / len(ast_strs)
        group_centers.append(center)

    # すべてのグループペアの中心間の編集距離を計算
    for i in range(len(group_centers)):
        for j in range(i+1, len(group_centers)):
            distance = abs(group_centers[i] - group_centers[j])
            inter_group_distances.append(distance)

    return inter_group_distances


# CSVファイルを開く
with open('crawling_output/output.csv', 'r') as f:
    reader = csv.reader(f)
    # リストに変換
    codes = [row[2] for row in reader]

# 確認のために出力
# print(codes)

threshold = 2000  # 編集距離の閾値

# ASTを生成してグループ化
grouped_codes = group_codes_by_similarity(codes, threshold)

# グループ内の平均編集距離を計算
group_distances = calculate_group_distances(grouped_codes, codes)

# グループ間の平均編集距離を計算
inter_group_distances = calculate_inter_group_distances(grouped_codes, codes)

print("Grouped Codes:", grouped_codes)
print("Group Distances:", group_distances)
print("Inter-Group Distances:", inter_group_distances)
