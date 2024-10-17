'''
@Project ：GhStockAnalysis 
@File    ：data_load.py
@IDE     ：PyCharm 
@Author  ：Gaogz
@Date    ：2024/10/16 10:09 
@Desc    ：
'''

from schema import schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from server import  dataload_server
from utils.token_utils import get_current_user
from loguru import logger

router = APIRouter(
    prefix="/dataload",
    tags=['DataLoad']
)

@router.post('/search', response_model=List[schemas.Stock])
def get_stocks(stock_req:schemas.StockReq,current_user: int = Depends(get_current_user)):#current_user: int = Depends(get_current_user)
    result = dataload_server.data_search(stock_req.code,stock_req.start_date,stock_req.end_date)
    result_format = [schemas.Stock(**item) for item in result]
    return result_format


@router.post('/all', status_code=status.HTTP_201_CREATED, response_model=List[schemas.Stock])
def all_stocks(stock_req: schemas.StockReqAll,current_user: int = Depends(get_current_user)):
    result = dataload_server.data_search_all(stock_req.code)
    result_format = [schemas.Stock(**item) for item in result]
    return result_format

