import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import nltk
import re
from gensim.models import Word2Vec
import os
import pickle



# 训练语料位置
folder_path = 'Data/Training_Data'
# 验证集题目
filepath_development_set = 'Data/development_set.txt'
# 验证集答案
filepath_development_answer = 'Data/development_set_answers.txt'
# 测试集题目
filepath_test_set = 'Data/test_set.txt'
# 数据预处理存放位置
sentence_data_file = 'Data/sentences_binary_1'
# 模型存放位置
word2vec_model_path = 'model/word2vec.model'
# 验证集预测答案
development_set_result = 'result/development_set_result'
# 测试集预测答案
test_set_result = 'result/test_set_result'


# 数据预处理
def splitSentence():
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_data = []
    raw_data = ''
    pathDir = os.listdir(folder_path)
    print('Load data')
    for path in pathDir:
        filepath = folder_path + '/' + path
        with open(filepath, 'r', encoding='iso-8859-1') as file_object:
            raw_data += file_object.read() + '\n\n'

    # 去除部分无用信息
    de_data = re.sub(r'(\[.*?\])', '', raw_data)
    de1_data = re.sub(r'(\(.*?\))', '', de_data)
    de2_data = re.sub(r'(\*.*?\*)', '', de1_data)
    de3_data = ' '.join(de2_data.split())
    print('Tokenize sentences')
    sentences = tokenizer.tokenize(de3_data)
    # 对句子进行处理 小于5个词的句子舍去
    for data in sentences:
        if ('@' in data or '.txt' in data or len(data.split(' ')) < 5):
            continue
        else:
            sentence_data.append(nltk.word_tokenize((data.replace('\n', ' ')).lower()))
    print('Save sentences')
    pickle.dump(sentence_data, open(sentence_data_file, "wb"))


# 训练word2vec_model
def train_word2vec():
    sentence_data = pickle.load(open(sentence_data_file, "rb"))
    print('Training word2vec model')
    word2vec_model = Word2Vec(sentence_data, size=200, window=15, min_count=5, negative=0, hs=1, workers=4)
    word2vec_model.save(word2vec_model_path)
    print('Done')


# 选取得分最大的选项  返回存储要求的字符串
def evaluate(question):
    flag = '_____'
    name = ['a', 'b', 'c', 'd', 'e']
    word2vec_model = Word2Vec.load(word2vec_model_path)
    answers = question['ans']
    num = question['num']
    que = question['que']
    answers_score = dict()
    for answer in answers:
        total = [nltk.word_tokenize(que.replace(flag, answer).lower())]
        score = word2vec_model.score(total)
        answers_score[answer] = score
    final_answer = max(answers_score, key=lambda x: answers_score[x])
    return num + ' ' + name[answers.index(final_answer)] + ' ' + final_answer


# 对完型填空进行预测
def load_test(filepath_input):
    with open(filepath_input, 'r', encoding='iso-8859-1') as file_object:
        raw_data = file_object.read()
    data = raw_data.splitlines()
    question = {'num': '', 'que': '', 'ans': []}
    results = []
    print('Calculate result')
    for d in data:
        if d.strip() != "":
            # 首字符为数字为题号
            if d.strip()[0].isdigit():
                word = d.strip().split(")")
                question['num'] = word[0].strip()
                question['que'] = word[1].strip()
                question['ans'].clear()
            else:
                # 选项
                question['ans'].append(d.strip().split()[1])
                if len(question['ans']) == 5:
                    results.append(evaluate(question))
                    # print(evaluate(question))
    print('Calculate stop')
    return results


# 存储结果
def saveResult(filename, results):
    print('Save result')
    with open(filename, 'a', encoding='utf-8') as f:
        for result in results:
            f.write(result + '\n')


# 读取选项结果
def read_result(filepath):
    with open(filepath, 'r', encoding='iso-8859-1') as file_object:
        data = file_object.read()
    dell_data = re.sub(r'[\[\]\)]', '', data)
    lines = dell_data.splitlines()
    answer = []
    for line in lines:
        if line.strip() != '':
            answer.append(line.split()[1])
    return answer


# 计算正确率
def cal_Accuracy():
    a_answer = read_result(filepath_development_answer)
    t_answer = read_result(development_set_result)
    count = 0
    for i in range(len(a_answer)):
        if a_answer[i] == t_answer[i]:
            count = count + 1
    print(count)
    print("Accuracy: %.4f%%" % (count / len(a_answer) * 100))


	
	
	
if __name__ == '__main__':
    # splitSentence()
    # train_word2vec()
    # 验证集
    # result_development = load_test(filepath_development_set)
    # saveResult(development_set_result, result_development)
    # 测试集
    result_test = load_test(filepath_test_set)
    saveResult(test_set_result, result_test)
    # 计算正确率
    cal_Accuracy()
