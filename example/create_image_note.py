'''
Author: liusuxian 382185882@qq.com
Date: 2024-10-22 20:08:36
LastEditors: liusuxian 382185882@qq.com
LastEditTime: 2024-10-23 03:00:46
Description: 

Copyright (c) 2024 by liusuxian email: 382185882@qq.com, All Rights Reserved.
'''
import sys
sys.path.append('/Users/liusuxian/Desktop/project-code/python-project/xhs')  # 导入自定义包的路径（调试用）
from xhs import DataFetchError, XhsClient
import datetime
import requests


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
    cookie = "a1=192b48b4592fo3xy3o2dcus50ycl3cmsvdr73pzdr40000259878; webId=123"
    xhs_client = XhsClient(cookie, sign=sign)
    print("当前时间：", datetime.datetime.now())
    phone = "18458212428"
    send_code_res = xhs_client.send_code(phone)
    print("验证码发送成功~")
    code = input("请输入验证码：")
    mobile_token = ""
    while True:
        try:
            check_code_res = xhs_client.check_code(phone, code)
            mobile_token = check_code_res["mobile_token"]
            print("check_code_res", check_code_res)
            break
        except DataFetchError as e:
            print("验证码校验失败", e)
            code = input("请输入验证码：")
    login_res = xhs_client.login_code(phone, mobile_token)
    print("login_res：", login_res)
    user_info_res = xhs_client.get_self_info2()
    print("luser_info_res：", user_info_res)
    title = "测试标题"
    desc = "测试描述"
    files = ["test1.jpg", "test2.jpg"]
    note_result = xhs_client.create_image_note(title, desc, files)
    print("note_result：", note_result)
