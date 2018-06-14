# encoding=utf-8
l1=[]
l2=[]

file = open('result.txt')
for i in file:
    l1.append(i)
file.close()

file1 = open('Test_Data/development_set_answers.txt')
for i in file1:
    l2.append(i)
file1.close()
c = 0
for i in range(len(l1)):
    if l1[i] == l2[i]:
        c += 1
# c 代表正确的数目

print '结果：正确数目：'+str(c)+' 总共题目：'+str(len(l1))+' 正确率：'+str(float(c)/float(len(l1)))

      # a)
      #   saw that             ->   c20
      #   saw that mechanism   ->   c31      ->  p31 = c31/c20
      #   that mechanism in    ->   c32      ->  p32 = c32/c21
      #   that mechanism       ->   c21      ->  p21 = c21/c11
      #   mechanism in         ->   c22      ->  p22 = c22/c12
      #   that                 ->   c11
      #   mechanism            ->   c12
      #
      #   注：c代表出现次数，例如：c21代表that mechanism词组在二元模型中的出现次数
      #       p代表概率，例如：p32代表已知that mechanism出现，下一个词出现in的概率
      #       对于 p21和p22的计算采用了数据平滑技术，如果二元组没有出现，例如c22=0,则记c22=0.5
