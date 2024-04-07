"""
Модель бюджета
"""
from dataclasses import dataclass


@dataclass
class Budget:
    """
    Бюджет, хранит срок в атрибуте period, сумму в атрибуте amount и ссылку (id) на
    категорию данного бюджета в атрибуте category
    """
    period: str
    category: int
    amount: int
    pk: int = 0
