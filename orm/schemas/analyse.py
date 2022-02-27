# 分析数据
from pydantic import BaseModel


class CardAnalyse(BaseModel):
    today: int
    all: int
    incr: int  # 新增


class AnalyseModel(BaseModel):
    review: CardAnalyse
    create: CardAnalyse
    categoryCount: int
    completionRate: float  # 今日完成率
    allCompletionRate: float  # 总完成率
