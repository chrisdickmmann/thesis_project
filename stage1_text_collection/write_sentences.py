import os
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import re
import nltk
import spacy
from nltk.corpus import words
from pdfminer.high_level import extract_text
# Or if you need hOCR output specifically
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_pages


nlp = spacy.load("en_core_web_sm")
# 下载 nltk 必要的数据
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

# NLTK's valid words set
valid_words = set(words.words())


def getlist():
    source_path = "./origin"
    origin_lst = [item for item in os.listdir(source_path) if item[-4:] == ".pdf"]
    return origin_lst


def clean_text(text):
    # keep only english
    text = re.sub(r"[^a-zA-Z0-9\s.,;!\\?&\-'()]", " ", text)

    # Step 1: Remove extra spaces
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space

    # Step 2: Connect split sentences
    # Remove line breaks and hyphens that split words
    text = re.sub(r"-\n", "", text)  # Handle hyphenated words split across lines

    # Step 3: Fix punctuation and spacing
    text = re.sub(r"\s+([.,;!?])", r"\1", text)  # Remove spaces before punctuation
    text = re.sub(r"([.,;!?])(\w)", r"\1 \2", text)  # Add space after punctuation
    text = text.strip()
    return text


nlp = spacy.load("en_core_web_sm")


def is_valid_sentence(sentence):
    """
    检查句子是否是一个合理的自然语言句子:
    - 包含至少一个名词和一个动词
    - 名词先出现
    - 语法结构合理 (SVO结构)
    """
    valid_words = set(words.words())

    # 使用 spaCy 进行分词和词性标注
    doc = nlp(sentence)

    first_noun_index = float('inf')
    first_verb_index = float('inf')

    for index, token in enumerate(doc):
        if token.pos_ == "NOUN" and first_noun_index == float('inf'):
            first_noun_index = index
        if token.pos_ == "VERB" and token.text.lower() in valid_words and first_verb_index == float('inf'):
            first_verb_index = index

    # 语法结构验证: 是否包含主谓结构
    has_subject = any(token.dep_ in ["nsubj", "nsubjpass"] for token in doc)
    # check token for features (nominal subject or nominal subject in a passive sentence

    has_verb = any(token.pos_ == "VERB" for token in doc)

    return first_noun_index < first_verb_index and has_subject and has_verb


def custom_sent_tokenize(text):
    # 定义会导致分句的标点符号及其对应的占位符
    punctuation_mapping = {
        '.': 'TEMP_DOT_PLACEHOLDER',
        ',': 'TEMP_COMMA_PLACEHOLDER',
        '?': 'TEMP_QUESTION_PLACEHOLDER',
        '!': 'TEMP_EXCLAMATION_PLACEHOLDER'
    }
    reverse_mapping = {v: k for k, v in punctuation_mapping.items()}

    # 处理 No.\d 和 d.\d 形式的文本
    def replace_in_special_patterns(match):
        content = match.group(0)
        for punc, placeholder in punctuation_mapping.items():
            content = content.replace(punc, placeholder)
        return content

    text = re.sub(r'No\.\d', replace_in_special_patterns, text)
    text = re.sub(r'd\.\d', replace_in_special_patterns, text)
    # 定义分割句子的正则表达式
    sentence_end_pattern = r'[.;!?]+'
    # 分割句子
    sentences = re.split(sentence_end_pattern, text)
    # 去除空句子
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # 把占位符替换回原来的标点符号
    def revert_placeholders(sentence):
        for placeholder, punc in reverse_mapping.items():
            sentence = sentence.replace(placeholder, punc)
        return sentence

    sentences = [revert_placeholders(sentence) for sentence in sentences]
    return sentences


def remove_leading_non_letters(s):
    while s and not s[0].isalpha():
        s = s[1:]
    return s


def save_txt(content, path):
    try:

        # 使用自定义的句子分割函数
        sentences = custom_sent_tokenize(content)

        # 将分割后的有效句子逐行写入输出文件
        with open(path, 'w', encoding='utf-8') as output_file:
            for sentence in sentences:
                if is_valid_sentence(sentence):
                    output_file.write(sentence + '\n')

        print(f"有效句子已成功写入 {path}。\n")
    except Exception as e:
        print(f"写入文件时出现错误: {e}")


def pdf2txt(fname):
    inpath = "/Users/caotony/PycharmProjects/csg_thesis/stage1_text_collection/origin/" + fname
    outpath = "/Users/caotony/PycharmProjects/csg_thesis/stage1_text_collection/pdf_miner/" + fname[:-4] + ".txt"

    text = extract_text(inpath)

    save_txt(text, outpath)


def main():
    lst = getlist()
    for file in lst:
        pdf2txt(file)


main()
