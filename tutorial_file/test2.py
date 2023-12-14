def generate_ngrams(tokens, N):
    """
    トークン列からN-gramsを生成する関数
    """
    ngrams = []
    for i in range(len(tokens) - N + 1):
        ngram = tuple(tokens[i:i + N])
        ngrams.append(ngram)
    return ngrams

def calculate_ngram_similarity(code1, code2, N):
    """
    2つのコードのN-gram類似度を計算する関数
    """
    # コードをトークンに分割
    tokens1 = code1.split()
    tokens2 = code2.split()

    # N-gramsを生成
    ngrams1 = generate_ngrams(tokens1, N)
    ngrams2 = generate_ngrams(tokens2, N)

    # 共通のN-gramsを抽出
    common_ngrams = set(ngrams1) & set(ngrams2)

    # 類似度を計算
    similarity = len(common_ngrams) / max(len(ngrams1), len(ngrams2))

    return similarity

# 例として2つのコードを用意
code1 = "def add_numbers(a, b): return a + b"
code2 = "def sum_numbers(x, y): return x + y"

# N-gramの次元（ここでは2-gram）
N = 2

# N-gram類似度を計算
similarity = calculate_ngram_similarity(code1, code2, N)

# 結果を出力
print(f"{N}-gram Similarity: {similarity}")
