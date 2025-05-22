import pandas as pd
import networkx as nx
import numpy as np

class GraphBuilder:
    def __init__(self, data_path, q_matrix_path, d_matrix_path):
        """
        初始化GraphBuilder模块
        :param data_path: 学生答题数据文件路径 (CSV格式)
        :param q_matrix_path: 知识点标签矩阵 (Q矩阵) 文件路径 (CSV格式)
        :param d_matrix_path: 概念先修矩阵 (D矩阵) 文件路径 (CSV格式)
        """
        self.data_path = data_path
        self.q_matrix_path = q_matrix_path
        self.d_matrix_path = d_matrix_path

    def load_data(self):
        """
        加载数据
        :return: 学生答题数据、Q矩阵、D矩阵
        """
        # 加载学生答题数据
        self.data = pd.read_csv(self.data_path)
        # 加载Q矩阵
        self.q_matrix = pd.read_csv(self.q_matrix_path, index_col=0)
        # 加载D矩阵
        self.d_matrix = pd.read_csv(self.d_matrix_path, index_col=0)

    def build_graphs(self):
        """
        构建三个图：GI (学生-题目-知识点交互图)、GR (题目-知识点关系图)、GD (知识点依赖图)
        :return: GI, GR, GD
        """
        # 构建学生-题目-知识点交互图 GI
        GI = nx.DiGraph()
        for index, row in self.data.iterrows():
            student_id = row['student_id']
            question_id = row['question_id']
            correct = row['correct']
            GI.add_node(student_id, type='student')
            GI.add_node(question_id, type='question')
            GI.add_edge(student_id, question_id, correct=correct)

        # 构建题目-知识点关系图 GR
        GR = nx.DiGraph()
        for question_id in self.q_matrix.columns:
            GR.add_node(question_id, type='question')
            for concept_id, value in self.q_matrix[question_id].items():
                if value == 1:
                    GR.add_node(concept_id, type='concept')
                    GR.add_edge(question_id, concept_id)

        # 构建知识点依赖图 GD
        GD = nx.DiGraph()
        for concept_id in self.d_matrix.columns:
            GD.add_node(concept_id, type='concept')
            for prerequisite_id, value in self.d_matrix[concept_id].items():
                if value == 1:
                    GD.add_edge(prerequisite_id, concept_id)

        return GI, GR, GD

    def save_graphs(self, GI, GR, GD, gi_path, gr_path, gd_path):
        """
        保存图到文件
        :param GI: 学生-题目-知识点交互图
        :param GR: 题目-知识点关系图
        :param GD: 知识点依赖图
        :param gi_path: GI图保存路径
        :param gr_path: GR图保存路径
        :param gd_path: GD图保存路径
        """
        nx.write_gpickle(GI, gi_path)
        nx.write_gpickle(GR, gr_path)
        nx.write_gpickle(GD, gd_path)

    def run(self, gi_path, gr_path, gd_path):
        """
        运行GraphBuilder模块
        :param gi_path: GI图保存路径
        :param gr_path: GR图保存路径
        :param gd_path: GD图保存路径
        """
        self.load_data()
        GI, GR, GD = self.build_graphs()
        self.save_graphs(GI, GR, GD, gi_path, gr_path, gd_path)
        print("Graphs have been successfully built and saved.")

if __name__ == "__main__":
    data_path = 'data/student_data.csv'
    q_matrix_path = 'data/q_matrix.csv'
    d_matrix_path = 'data/d_matrix.csv'
    gi_path = 'graphs/GI.gpickle'
    gr_path = 'graphs/GR.gpickle'
    gd_path = 'graphs/GD.gpickle'

    graph_builder = GraphBuilder(data_path, q_matrix_path, d_matrix_path)
    graph_builder.run(gi_path, gr_path, gd_path)