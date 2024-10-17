'''
@Project ：GhStockAnalysis 
@File    ：ai_chat.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 21:53 
@Desc    ：智慧问数功能
'''

from fastapi import Response, status, Depends, APIRouter

from server import  dataload_server
from schema.schemas import Chat
from utils.token_utils import get_current_user
from loguru import logger

router = APIRouter(
    prefix="/chat",
    tags=['DataLoad']
)

@router.post('/chat')
def get_stocks(chat:Chat,current_user: int = Depends(get_current_user)):#
    if chat.user_input == '':
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content='请输入查询条件')
    else:
        #   TODO 解析要查询的股票代码
        #  TODO 解析要查询的开始和截止日期
        #  TODO 解析要查询的指标
        #  TODO 解析要展示的图形类别
        result = dataload_server.data_search("NIO","2023-01-01","2024-05-01")

        # chart_type:line,pie,bar,table
        if "折线" in chat.user_input or "趋势" in chat.user_input:
            return {"chart_type":"line","data":result}
        elif "饼图" in chat.user_input:
            return {"chart_type":"pie","data":result}
        elif "柱状图" in chat.user_input or "直方图" in chat.user_input or "条形图" in chat.user_input:
            return {"chart_type":"bar","data":result}
        elif "表格" in chat.user_input:
            return {"chart_type":"table","data":result}
