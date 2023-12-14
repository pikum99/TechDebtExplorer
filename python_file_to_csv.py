import csv
import os


def get_python_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)


def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def write_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    directory = './'  # フォルダを指定
    output_csv = './crawling_output/output.csv'  # 出力するCSVファイル名を指定

    data = []
    for file_path in get_python_files(directory):
        content = get_file_content(file_path)
        data.append([file_path, len(content), ''.join(content)])

    write_to_csv(output_csv, data)


if __name__ == "__main__":
    main()
