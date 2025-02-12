import nltk

# 下载 nltk 必要的数据
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
def has_verb(sentence):
    """
    检查句子中是否包含谓语动词
    """
    # 对句子进行分词
    tokens = nltk.word_tokenize(sentence)
    # 进行词性标注
    tagged_tokens = nltk.pos_tag(tokens)
    # 检查是否存在动词词性（以 'VB' 开头的标签表示动词）
    for _, tag in tagged_tokens:
        if tag.startswith('VB'):
            return True
    return False

def is_valid_sentence(sentence):
    """
    检查句子是否有效，要求句子长度大于 3 且包含谓语动词
    """
    return len(sentence.strip()) > 3 and has_verb(sentence)

def extract_and_write_sentences(input_file_path, output_file_path):
    try:
        # 读取输入文件内容
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            text = input_file.read()

        # 使用 nltk 进行句子分割
        sentences = nltk.sent_tokenize(text)

        # 将分割后的有效句子逐行写入输出文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for sentence in sentences:
                if is_valid_sentence(sentence):
                    output_file.write(sentence + '\n')

        print(f"有效句子已成功写入 {output_file_path}。")
    except FileNotFoundError:
        print(f"文件 {input_file_path} 未找到。")
    except Exception as e:
        print(f"发生错误: {e}")


# 使用示例
input_path = '/Users/caotony/PycharmProjects/csg_thesis/textex/ANTA_2022.txt'
output_path = '/Users/caotony/PycharmProjects/csg_thesis/sentences/ANTA_2022.txt'
extract_and_write_sentences(input_path, output_path)