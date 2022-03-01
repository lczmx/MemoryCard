"""
初始化帮助文档

"""
import logging

from orm import SessionLocal
from orm.models import Doc
from orm.crud import save_all_to_db, query_all_doc_title
from orm.schemas.other import ReadDocModel


def crate_docs():
    logging.info("初始化帮助文档数据中...")
    # 没有uid
    data = [
        {
            "title": "添加类别",
            "tag": "类别,入门",
            "content": r'在类别页面点击"+"号。\n根据提示输入:\n1. 类别名\n2. 类别颜色\n3. 类别图标' +
                       r'\n4. 该类别的复习曲线\n\n这样你就可以创建卡片了',
        }, {
            "title": "添加卡片",
            "tag": "卡片,入门",
            "content": r'在卡片页面点击"+"号。\n根据提示输入:\n1. 卡片名称\n2. 类别所属类别\n3. 概要信息' +
                       r'\n4. 卡片的详细信息\n\n等到复习时间一到, 你就可以进行复习了',
        }, {
            "title": "完成复习",
            "tag": "卡片,入门",
            "content": r'在复习页面点击要复习的卡片\n进入复习模式\n在复习模式中你可以上下左右滑动执行不同的操作：' +
                       r'右滑：上一张卡片\n左滑：下一张卡片\n上滑：完成本张卡片复习\n下滑：本次复习跳过此卡片\n\n' +
                       r'当全部复习完后会自动跳出复习模式',
        }, {
            "title": "星标卡片/类别",
            "tag": "卡片,类别,进阶",
            "content": r'在卡片/类别/复习模式页面，都可以对卡片和类别进行星标\n星标之后你可以对其进行筛选，从而能够只看星标的数据'
        }, {
            "title": "批量操作数据",
            "tag": "卡片,类别,进阶",
            "content": r'在卡片/类别/复习模式页面\n点击右上角的"..."，点击"选择卡片"或"选择类别"，进入多选操作模式\n你可以对数据进行批量操作'
        }, {
            "title": "对数据排序",
            "tag": "卡片,类别,进阶",
            "content": r'在类别/复习模式页面\n点击右上角的"..."，点击"排序"\n你可根据选择排序依据, 从而得到自己想要的数据'
        }, {
            "title": "重置复习",
            "tag": "卡片,类别,进阶",
            "content": r'当你修改复习曲线的复习区间/类别的复习曲线的时候，会重置复习\n也就是说卡片会处于刚开始创建的时刻。' +
                       r'除此之外，你还可以主动重置卡片复习，具体操作如下：\n1. 卡片页面左滑卡片，点击重置按钮，重置单个卡片' +
                       r'或进入卡片的选择模式进行批量重置\n2. 类别页面长按类别，点击"重置复习"即可重置给类别的全部卡片'
        }, {
            "title": "编辑卡片数据",
            "tag": "卡片,进阶",
            "content": r'在卡片页面左滑卡片，点击编辑按钮即可编辑对应的卡片数据。除此之外，在复习模式页面中在复习时编辑卡片的数据'
        }, {
            "title": "编辑类别数据",
            "tag": "类别,进阶",
            "content": r'类别页面长按类别，点击"编辑"即可编辑类别'
        }, {
            "title": "删除数据",
            "tag": "卡片,类别,进阶",
            "content": r'在卡片页面，左滑卡片，点击删除按钮即可删除卡片，进入选择模式可以删除多个卡片数据\n' +
                       r'在类别页面，长按类别，点击删除，即可删除类别，删除类别后，该卡片下的全部类别也将被删除'
        }, {
            "title": "自定义复习曲线",
            "tag": "复习曲线,进阶",
            "content": r'在设置页面，点击"复习曲线"，然后点击"+"，即可添加复习曲线\n' +
                       r'复习曲线的时间可以任意编辑，随意组合，以自定义自己需要的复习曲线'
        }, {
            "title": "更多帮助",
            "tag": "其它,进阶",
            "content": r'更多操作可以自行摸索'
        }
    ]

    with SessionLocal() as session:
        # 跳过已经有的
        exists_docs = query_all_doc_title(session=session)
        docs = [ReadDocModel(**d) for d in data if d.get("title") not in exists_docs]
        if docs:
            # 正式初始化
            save_all_to_db(session=session, model_class=Doc, data_list=docs)
            logging.info("初始化完毕")
        else:
            # 已经初始化过了
            logging.info("已经初始化了")
