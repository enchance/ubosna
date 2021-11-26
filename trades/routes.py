from fastapi import APIRouter, Depends, Response




traderouter = APIRouter()


@traderouter.post('/new_trade')
async def new_trade(res: Response, trade_data: dict):
    pass