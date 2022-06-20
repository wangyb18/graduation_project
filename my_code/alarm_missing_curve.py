import numpy as np
import json
import math
import pandas as pd
import matplotlib.pyplot as plt

'''
    动态规划——字符串的编辑距离
    s1 = "abc", s2 = "def"
    计算公式：
             | 0                                           i = 0, j = 0
             | j                                           i = 0, j > 0
    d[i,j] = | i                                           i > 0, j = 0
             | min(d[i,j-1]+1, d[i-1,j]+1, d[i-1,j-1])    s1(i) = s2(j)
             | min(d[i,j-1]+1, d[i-1,j]+1, d[i-1,j-1]+1)  s1(i) ≠ s2(j)
    定义二维数组[4][4]：
        d e f            d e f
    |x|x|x|x|        |0|1|2|3|
    a |x|x|x|x|  =>  a |1|1|2|3|  => 编辑距离d = [4][4] = 3
    b |x|x|x|x|      b |2|2|2|3|
    c |x|x|x|x|      c |3|3|3|3|
'''


def levenshtein(s1, s2):
    i = 0  # s1字符串中的字符下标
    j = 0  # s2字符串中的字符下标
    m = len(s1)  # s1字符串长度
    n = len(s2)  # s2字符串长度
    if n == 0:
        return m, np.zeros(0)
    if m == 0:
        return n, np.zeros(n)
    # 返回一个表示s2对应位置是否正确的向量
    s2_right_array = np.zeros(n) + 1
    solutionMatrix = [[0 for col in range(n + 1)] for row in range(m + 1)]  # 长为m+1，宽为n+1的矩阵
    '''
             d e f
          |0|x|x|x|
        a |1|x|x|x|
        b |2|x|x|x|
        c |3|x|x|x|
    '''
    for i in range(m + 1):
        solutionMatrix[i][0] = i
    '''
             d e f
          |0|1|2|3|
        a |x|x|x|x|
        b |x|x|x|x|
        c |x|x|x|x|

    '''
    for j in range(n + 1):
        solutionMatrix[0][j] = j
    '''
        上面两个操作后，求解矩阵变为
             d e f
          |0|1|2|3|
        a |1|x|x|x|
        b |2|x|x|x|
        c |3|x|x|x|
        接下来就是填充剩余表格
    '''
    for x in range(1, m + 1):
        s1i = s1[x - 1]
        for y in range(1, n + 1):
            s2j = s2[y - 1]
            flag = 0 if s1i == s2j else 1
            solutionMatrix[x][y], operation = min(solutionMatrix[x - 1][y] + 1, solutionMatrix[x][y - 1] + 1,
                                                  solutionMatrix[x - 1][y - 1] + flag)
            # if (x == 6 and y == 2) or (x == 7 and y == 3):
            #     print('s1i:', s1i, ' s2j:', s2j)
            #     print(flag)
            #     print('solutionMatrix[x - 1][y] + 1 ', solutionMatrix[x - 1][y] + 1)
            #     print('solutionMatrix[x][y - 1] + 1', solutionMatrix[x][y - 1] + 1)
            #     print('solutionMatrix[x - 1][y - 1] + flag', solutionMatrix[x - 1][y - 1] + flag)
            #     print('solutionMatrix[x][y] ', solutionMatrix[x][y], 'operation', operation)
    # 追踪轨迹，得到每个token是否正确的评估
    s1_index, s2_index = m, n
    while solutionMatrix[s1_index][s2_index] != 0:
        if s1_index > 0 and s2_index > 0:
            last_solution, operation = min(solutionMatrix[s1_index - 1][s2_index],
                                           solutionMatrix[s1_index][s2_index - 1],
                                           solutionMatrix[s1_index - 1][s2_index - 1])
            if last_solution == solutionMatrix[s1_index][s2_index] - 1 and (
                    operation == 'delete' or operation == 'edit'):
                s2_right_array[s2_index - 1] = 0
        elif s1_index == 0 and s2_index > 0:
            s2_right_array[0:s2_index - 1] = 0
            return solutionMatrix[m][n], s2_right_array
        elif s1_index > 0 and s2_index == 0:
            return solutionMatrix[m][n], s2_right_array
        else:
            operation = ''
            print('回溯异常')
            print("s1_index:", s1_index, " s2_index:", s2_index)
            # for i in range(m + 1):
            #     for j in range(n + 1):
            #         print(solutionMatrix[i][j], end=' ')
            #     print('\n')
            exit(0)
        s1_index, s2_index = update_index(operation, s1_index, s2_index)
    return solutionMatrix[m][n], s2_right_array


def min(insert, delete, edit):
    if insert < delete and insert < edit:
        tmp, operation = insert, 'insert'
    elif delete < edit:
        tmp, operation = delete, 'delete'
    else:
        tmp, operation = edit, 'edit'
    return tmp, operation


def update_index(operation, s1_index, s2_index):
    if operation == 'edit':
        s1_index, s2_index = s1_index - 1, s2_index - 1
    elif operation == 'insert':
        s1_index, s2_index = s1_index - 1, s2_index
    elif operation == 'delete':
        s1_index, s2_index = s1_index, s2_index - 1
    else:
        print('update_index异常')
    return s1_index, s2_index


def classify(P_or_N, prob, TP, FP, TN, FN):
    # 归类至四类中某一类
    # TP
    if P_or_N == 1 and prob > confidence_threshold:
        TP += 1
    # FP
    elif P_or_N == 1 and prob <= confidence_threshold:
        FP += 1
    # TN
    elif P_or_N == 0 and prob <= confidence_threshold:
        TN += 1
    # FN
    elif P_or_N == 0 and prob > confidence_threshold:
        FN += 1
    else:
        print("分类错误！")
    return TP, FP, TN, FN


# 读取json文件内容,返回字典格式
with open('result-ood.json', 'r', encoding='utf8')as fp:
    result = json.load(fp)

# 记录confidence与accuracy的列表
low = 0.9
high = 1
bin_num = 20
confidence_list = [[] for i in range(bin_num)]
accuracy_list = [[] for i in range(bin_num)]
tick_list = [round(low + i * (high - low) / bin_num, 4) for i in range(bin_num)]
confidence_bin_border = pd.DataFrame(tick_list)
print(confidence_bin_border)
T = 1
# 置信度域值
threshold_num = 200
threshold_low = 0
threshold_high = 1

confidence_threshold_list = [threshold_low + i * (threshold_high - threshold_low) / threshold_num for i in
                             range(threshold_num)]
TP_array, FP_array, TN_array, FN_array = np.zeros(len(confidence_threshold_list)), np.zeros(
    len(confidence_threshold_list)), np.zeros(len(confidence_threshold_list)), np.zeros(len(confidence_threshold_list))
for threshold_index, confidence_threshold in enumerate(confidence_threshold_list):
    # 按对话循环,用索引实现
    result_index = 0
    while result_index < len(result):
        turn_index = 1
        while turn_index <= result[result_index]['turn_num']:
            bspn_tokens = result[result_index + turn_index]['bspn_tokens']
            bspn_tokens_gen = result[result_index + turn_index]['bspn_tokens_gen']
            bspn_prob_gen = result[result_index + turn_index]['bspn_prob_2.00']
            bspn_tokens = eval(bspn_tokens)
            bspn_tokens_gen = eval(bspn_tokens_gen)
            bspn_prob_gen = eval(bspn_prob_gen)
            # 消除\u字符
            for i in range(len(bspn_tokens)):
                if "\u0120" in bspn_tokens[i]:
                    bspn_tokens[i] = bspn_tokens[i][1:]
            for i in range(len(bspn_tokens_gen)):
                if "\u0120" in bspn_tokens_gen[i]:
                    bspn_tokens_gen[i] = bspn_tokens_gen[i][1:]
            # 将第一个token及其概率去掉
            bspn_tokens = bspn_tokens[1:-1]
            bspn_tokens_gen = bspn_tokens_gen[1:-1]
            bspn_prob_gen = bspn_prob_gen[1:-1]
            # print(bspn_tokens)
            # print(bspn_tokens_gen)
            # print(bspn_prob_gen)
            # 得到confidence所在区间
            distance, bspn_right_array = levenshtein(bspn_tokens, bspn_tokens_gen)
            # print('distance', distance)
            # print('bspn_right_array', bspn_right_array)
            for i in range(len(bspn_prob_gen)):
                temp_list = confidence_bin_border < bspn_prob_gen[i]
                confidence_bin_position = (temp_list.sum() - 1)[0]

                # 特殊情况处理
                if confidence_bin_position == -1:
                    continue
                if bspn_prob_gen[i] <= confidence_bin_border.iloc[confidence_bin_position, 0]:
                    print(bspn_prob_gen[i])
                    print(confidence_bin_position)
                    exit(0)

                confidence_list[confidence_bin_position].append(bspn_prob_gen[i])
                positive_negative_flag = bspn_right_array[i]
                accuracy_list[confidence_bin_position].append(positive_negative_flag)

                # 归类至四类中某一类
                TP_array[threshold_index], FP_array[threshold_index], TN_array[threshold_index], FN_array[
                    threshold_index] = classify(bspn_right_array[i], bspn_prob_gen[i], TP_array[threshold_index],
                                                FP_array[threshold_index], TN_array[threshold_index],
                                                FN_array[threshold_index])

            turn_index += 1
        result_index += turn_index

##
TP_array2, FP_array2, TN_array2, FN_array2 = TP_array, FP_array, TN_array, FN_array

##
figure_num = 10


def plot_alarm_missing_curve(word_type, FN_array, FP_array, TN_array, TP_array):
    # 计算missing_alarm与false_alarm
    global figure_num
    plt.figure(figure_num)
    MA_array = FN_array / (TP_array + FN_array)
    FA_array = FP_array / (TP_array + FP_array)
    plt.plot(MA_array, FA_array)
    plt.xlabel('MA')
    plt.ylabel('FA')
    # plt.title(word_type, 'FA-MA figure')
    plt.show()


plot_alarm_missing_curve('OOD', FN_array2, FP_array2, TN_array2, TP_array2)
plot_alarm_missing_curve('OOD', FN_array, FP_array, TN_array, TP_array)
##
# 计算missing_alarm与false_alarm
word_type = 'OOD'
MA_array = FN_array / (TP_array + FN_array)
FA_array = FP_array / (TP_array + FP_array)
plt.plot(MA_array, FA_array)
plt.xlabel('MA')
plt.ylabel('FA')
plt.title(word_type, 'FA-MA figure')
plt.show()

##
# 计算ECE
accuracy_array = np.array([sum(accuracy_list[i]) / len(accuracy_list[i]) if len(accuracy_list[i]) != 0 else 0 for i in
                           range(bin_num)]).squeeze()
accuracy_num_array = np.array([len(accuracy_list[i]) for i in range(bin_num)]).squeeze()
confidence_array = np.array(
    [sum(confidence_list[i]) / len(confidence_list[i]) if len(confidence_list[i]) != 0 else 0 for i in
     range(bin_num)]).squeeze()
bin_sum = [len(confidence_list[i]) for i in range(bin_num)]
print(accuracy_array)
print(confidence_array)
ECE = sum(abs(confidence_array - accuracy_array) * accuracy_num_array) / sum(accuracy_num_array)
print("ECE:", ECE)

##
import openpyxl

# 写出数据
data = pd.DataFrame()
data['confidence_array'] = confidence_array
data['accuracy_array'] = accuracy_array
data['bin_sum'] = bin_sum
data.to_excel('data1.xlsx')
##
import matplotlib.pyplot as plt

# 绘制图像
tick_list = [round(low + i * (high - low) / bin_num, 4) for i in range(bin_num)]
plt.bar(range(len(confidence_array)), confidence_array, label='confidence', fc='r', tick_label=tick_list)
plt.bar(range(len(accuracy_array)), accuracy_array, label='accuracy', fc='b', tick_label=tick_list)
plt.xlabel('bin')
plt.title('The comparison of accuracy and confidence')
plt.legend()
plt.show()

##
import torch

a = torch.torch.tensor([[[1.0, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
b = torch.torch.tensor([[0, 2], [1, 2]])
# b = torch.torch.tensor([[[b.numpy().tolist()[i][j]] for j in range(b.size(1))] for i in range(b.size(0))])
# print(b)
b = b.unsqueeze(-1)
energy_a = a.max(dim=2)
print(energy_a.values)
##

energy = (energy_a.sum(dim=1) / energy_a.size(1)).squeeze()

print("energy_a:", energy_a.squeeze())
print(energy)
prob_a = torch.softmax(a, dim=2)
print(prob_a)

##
import random
a = [50312, 5875, 345, 329, 534, 1037, 764, 326, 318, 3446, 644, 1312, 2622, 1909, 764, 24829, 764, 50306]

def mask_replace(self, sentence_ids):
    ratio = torch.tensor(0.4)
    length = len(sentence_ids)
    mask_num = int(torch.ceil(ratio * length))
    mask_index_list = torch.randint(low=1, high=length - 1, size=(mask_num,))
    for mask_index in mask_index_list:
        sentence_ids[mask_index] = random.randint(1000, 50000)