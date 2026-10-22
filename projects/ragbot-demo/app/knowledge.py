"""内置示例知识库：几段课程相关的说明文本。"""
from .retriever import KnowledgeBase


def build_kb() -> KnowledgeBase:
    kb = KnowledgeBase(threshold=0.1)
    docs = [
        "数据结构课程主要讲授线性表、栈、队列、树和图等基本结构，以及它们的存储与算法实现。",
        "栈是一种后进先出的数据结构，常见操作有入栈 push 和出栈 pop，可用于表达式求值。",
        "队列是一种先进先出的数据结构，常见操作有入队和出队，可用于任务调度和广度优先搜索。",
        "数据库原理课程涵盖关系模型、SQL 查询、事务与索引，是后端开发的基础。",
        "二叉树的遍历方式有前序、中序和后序三种，其中中序遍历有序二叉树可得到升序序列。",
    ]
    for d in docs:
        kb.add(d)
    return kb
