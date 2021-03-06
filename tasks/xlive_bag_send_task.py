from BiliClient import asyncbili
from .import_once import now_time
import logging

async def xlive_bag_send_task(biliapi: asyncbili):
    try:
         room_id = (await biliapi.xliveGetRecommendList())["data"]["list"][6]["roomid"]
         uid = (await biliapi.xliveGetRoomInfo(room_id))["data"]["room_info"]["uid"]
         bagList = (await biliapi.xliveGiftBagList())["data"]["list"]
         ishave = False
         for x in bagList:
             if x["expire_at"] - now_time < 172800 and x["expire_at"] - now_time > 0: #礼物到期时间小于2天
                 ishave = True
                 ret = await biliapi.xliveBagSend(room_id, uid, x["bag_id"], x["gift_id"], x["gift_num"])
                 if ret["code"] == 0:
                     logging.info(f'{biliapi.name}: {ret["data"]["send_tips"]} {ret["data"]["gift_name"]} 数量{ret["data"]["gift_num"]}')
         if ishave:
             logging.info(f'{biliapi.name}: 没有2天内过期的直播礼物，跳过赠送')
    except Exception as e:
        logging.warning(f'{biliapi.name}: 直播送出即将过期礼物异常，原因为{str(e)}')
