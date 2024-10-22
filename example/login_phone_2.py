'''
Author: liusuxian 382185882@qq.com
Date: 2024-10-22 20:08:36
LastEditors: liusuxian 382185882@qq.com
LastEditTime: 2024-10-23 02:13:00
Description: 

Copyright (c) 2024 by liusuxian email: 382185882@qq.com, All Rights Reserved.
'''
import sys
sys.path.append('/Users/liusuxian/Desktop/project-code/python-project/xhs')  # 导入自定义包的路径（调试用）
import requests
import datetime
from xhs import DataFetchError, XhsClient


def sign(uri, data=None, a1="", web_session=""):
    # 填写自己的 flask 签名服务端口地址
    res = requests.post("http://localhost:5005/sign",
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    print("sign：", uri, a1, web_session, signs)
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }


if __name__ == '__main__':
    cookie = "a1=192b48b4592fo3xy3o2dcus50ycl3cmsvdr73pzdr40000259878; webId=ba57f42593b9e55840a289fa0b755374"
    xhs_client = XhsClient(cookie, sign=sign)
    print("当前时间：", datetime.datetime.now())
    phone = "17364814710"
    send_code_res = xhs_client.web_verify_code(phone)
    print("验证码发送成功~")
    code = input("请输入验证码：")
    while True:
        try:
            ticket_res = xhs_client.web_service_ticket(phone, code)
            print("ticket_res", ticket_res)
            break
        except DataFetchError as e:
            print("验证码校验失败", e)
            code = input("请输入验证码：")
    user_info_res = xhs_client.user_info_from_creator()
    print("user_info_res：", user_info_res)
    note_info = xhs_client.datacenter_note_base("67177a9500000000260361b6")
    print("note_info：", note_info)
    title = "测试标题"
    desc = "测试描述"
    files = ["test1.jpg", "test2.jpg"]
    xhs_client.create_image_note(title, desc, files, is_private=True)
