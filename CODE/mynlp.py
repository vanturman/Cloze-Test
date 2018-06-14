# encoding=utf-8
from nltk.util import ngrams
from nltk import word_tokenize
from nltk import sent_tokenize
import os

class mynlp:

    training_data_path = 'Data/Training_Data'  # 该文件夹下存储着所有的训练数据
    test_data_path = 'Test_Data/development_set.txt'   # 该文件存储着用于开发的测试文档
    result_file_path = 'result.txt'    # 发送给助教的结果
    #test_data_path = 'Test_Data/test_set.txt'
    training_gram1_res = {}  # 存储一元模型的结果（词频）
    training_gram2_res = {}  # 存储二元模型的结果
    training_gram3_res = {}  # 存储三元模型的结果
    result_list = []         # 存储计算结果

    def __init__(self):
        self.start()

    def start(self):
        # 第一步，读取数据集，将二元模型存储到字典当中，将元组写入一个文件当中，训练一次后可注释掉
        # self.train_data()
        # 第二步，将写好的文件读出来，存到字典当中，（an，apple） :  2
        self.read_from_training()
        # 第三步，针对每一道题，将每个答案放到句子中，计算这个词和前一个词与后一个词分别的2元模型,选取概率最大的那个
        self.select_result()
        # 第四步，将结果写入文件，发给助教
        self.write_result()

    def train_data(self):

        datafiles = os.listdir(self.training_data_path)
        for i in datafiles:
            filename = self.training_data_path+'/'+i
            f = open(filename)
            data = self.clear_string(str(f.readlines()))
            data_sent = sent_tokenize(data)
            for j in data_sent:
                data_words = word_tokenize(j)

                # 训练一元组，求频率
                for t in data_words:
                    # t = self.clear_string(t)
                    if t in self.training_gram1_res:
                        self.training_gram1_res[t] += 1
                    else:
                        self.training_gram1_res[t] = 1

                # 训练二元组
                training_gen = ngrams(data_words, 2)
                for k in training_gen:
                    # k = self.clear_string(k)
                    if k in self.training_gram2_res:
                        self.training_gram2_res[k] += 1
                    else:
                        self.training_gram2_res[k] = 1

                # 训练三元组
                training_gen = ngrams(data_words, 3)
                for b in training_gen:
                    # b = self.clear_string(b)
                    if b in self.training_gram3_res:
                        self.training_gram3_res[b] += 1
                    else:
                        self.training_gram3_res[b] = 1
            f.close()

        result_file1 = open('result_1.txt', 'w')
        for i in self.training_gram1_res:
            result_file1.writelines(str(i)+'  '+str(self.training_gram1_res[i])+'\n')
        result_file1.close()

        result_file2 = open('result_2.txt', 'w')
        for i in self.training_gram2_res:
            result_file2.writelines(str(i)+'  '+str(self.training_gram2_res[i])+'\n')
        result_file2.close()

        result_file3 = open('result_3.txt', 'w')
        for i in self.training_gram3_res:
            result_file3.writelines(str(i)+'  '+str(self.training_gram3_res[i])+'\n')
        result_file3.close()

    def clear_string(self, s):
        if len(s) > 1:
            return s.replace('\\r', '').replace('\\n', '').replace('\\', '').replace("'", "").replace("`", "")
        else:
            return s

    def read_from_training(self):
        read_file1 = open('result_1.txt', 'r')
        for i in read_file1:
            read_gram_key = i.split("  ")[0]
            read_gram_num = int(i.split("  ")[1].replace('\n', ''))
            self.training_gram1_res[read_gram_key] = read_gram_num
        read_file1.close()

        read_file2 = open('result_2.txt', 'r')
        for i in read_file2:
            read_gram_key = i.split("  ")[0]
            read_gram_num = int(i.split("  ")[1].replace('\n', ''))
            self.training_gram2_res[read_gram_key] = read_gram_num
        read_file2.close()

        read_file3 = open('result_3.txt', 'r')
        for i in read_file3:
            read_gram_key = i.split("  ")[0]
            read_gram_num = int(i.split("  ")[1].replace('\n', ''))
            self.training_gram3_res[read_gram_key] = read_gram_num
        read_file3.close()

    def select_result(self):
        test_file = open(self.test_data_path, 'r').readlines()
        index = 0
        while index < len(test_file):
            question = test_file[index]
            choices = {}
            for l in range(5):
                k = test_file[index+l+1].split()[0]
                v = test_file[index+l+1].split()[1]
                choices[k] = v
            result = self.get_best_choice(question, choices)
            # print result
            self.result_list.append(result)
            index += 8

    def get_best_choice(self,question,choices):
        result = []
        q = question.split()
        question_num = q[0]
        space = q.index('_____')
        pre_pre = q[space-2]
        pre = q[space-1]
        nex = q[space+1]

        for c in choices:
            p31 = self.get_p3(pre_pre,pre,choices[c])
            p32 = self.get_p3(pre,choices[c],nex)
            p21 = self.get_p2(pre,choices[c])
            p22 = self.get_p2(choices[c],nex)
            l = [c,p31,p32,p21,p22]
            result.append(l)

        find = False
        # print question_num
        max_choice = ''

        #第一步，选出p32*p31最大的
        max_p32_mul_p31 = float(0)
        for i in range(5):
            if result[i][1] * result[i][2] > max_p32_mul_p31:
                max_p32_mul_p31 = result[i][1] * result[i][2]
                max_choice = result[i][0]
                find = True
                # print 'p32*p31'

        # 第二步，如果第一步没选出来,选出p32最大的
        max_p32 = float(0)
        if not find:
            for i in range(5):
                if result[i][2] > max_p32:
                    max_p32 = result[i][2]
                    max_choice = result[i][0]
                    find = True
                    # print 'p32'
            if max_p32 < 0.0005:
                find = False

        # 第三步，如果第一、二步没选出来,选出p31最大的
        max_p31 = float(0)
        if not find:
            for i in range(5):
                if result[i][1] > max_p31:
                    max_p31 = result[i][1]
                    max_choice = result[i][0]
                    find = True
                    # print 'p31'
            if max_p31 < 0.0005:
                find = False

        # 第四步，如果第一、二、三步没选出来,选出p21*p12最大的
        max_p21_mul_p12 = float(0)
        if not find:
            for i in range(5):
                if result[i][3]*result[i][4] > max_p21_mul_p12:
                    max_p21_mul_p12 = result[i][3]*result[i][4]
                    max_choice = result[i][0]
                    find = True
                    # print 'p2*p1'
        # 第五步，如果第一、二、三、四步没选出来,选出p21最大的
        max_p21 = float(0)
        if not find:
            for i in range(5):
                if result[i][3] > max_p21:
                    max_p21 = result[i][3]
                    max_choice = result[i][0]
                    find = True
                    # print 'p21'
        # 第六步，如果第一、二、三、四、五步没选出来,选出p22最大的
        max_p22 = float(0)
        if not find:
            for i in range(5):
                if result[i][4] > max_p22:
                    max_p22 = result[i][4]
                    max_choice = result[i][0]
                    find = True
                    # print 'p22'
        # 第七步，如果第一、二、三、四、五、六步没选出来,选e
        if not find:
            max_choice = 'e)'
            # print 'e'

        return question_num+' ['+max_choice.replace(')','')+'] '+str(choices[max_choice])

    def get_p3(self, pre, mid, nex):
        c = float(0)
        k3 = "('"+pre+"', '"+mid+"', '"+nex+"')"
        k2 = "('"+pre+"', '"+mid+"')"
        if k3 in self.training_gram3_res:
            c = float(self.training_gram3_res[k3])/float(self.training_gram2_res[k2])
        return c

    def get_p2(self, v1, v2):
        c = float(0)
        k = "('"+v1+"', '"+v2+"')"
        if k in self.training_gram2_res:
            c = float(self.training_gram2_res[k])/float(self.training_gram1_res[v1])
        else:
            if v1 in self.training_gram1_res:
                c = float(1)/float(self.training_gram1_res[v1])
            else:
                pass
        return c

    def write_result(self):
        result_file = open(self.result_file_path, 'w')
        for i in self.result_list:
            result_file.writelines(i+'\n')
        result_file.close()


if __name__ == '__main__':
    mynlp()
