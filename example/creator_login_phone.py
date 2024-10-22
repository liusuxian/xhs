'''
Author: liusuxian 382185882@qq.com
Date: 2024-10-22 20:08:36
LastEditors: liusuxian 382185882@qq.com
LastEditTime: 2024-10-22 20:26:18
Description: 

Copyright (c) 2024 by liusuxian email: 382185882@qq.com, All Rights Reserved.
'''
import datetime
import json
from time import sleep
from playwright.sync_api import sync_playwright
from xhs import DataFetchError, XhsClient


def sign(uri, data=None, a1="", web_session=""):
    print("sign: ", uri, data, a1, web_session)
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = "/Users/liusuxian/Desktop/project-code/python-project/xhs/stealth.min.js"
                chromium = playwright.chromium
                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)
                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://creator.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")


if __name__ == '__main__':
    xhs_client = XhsClient(sign=sign)
    print("当前时间：", datetime.datetime.now())
    phone = "17364814710"
    send_code_res = xhs_client.customer_send_code(phone)
    print("验证码发送成功：", send_code_res)
    code = input("请输入验证码：")
    ticket = ""
    while True:
        try:
            check_res = xhs_client.login_with_verify_code(phone, code)
            print("check_res", check_res)
            ticket = check_res["data"]
            break
        except DataFetchError as e:
            print(e)
            code = input("请输入验证码：")
    customer_login_res = xhs_client.customer_login(ticket)
    print("customer_login_res", customer_login_res)
    login_from_creator_res = xhs_client.login_from_creator()
    print("login_from_creator_res", login_from_creator_res)
    user_info_res = xhs_client.user_info_from_creator()
    print("user_info_res", json.dumps(user_info_res, indent=4))
    # print(json.dumps(login_res, indent=4))
    # print("当前 cookie：" + xhs_client.cookie)
    # print(xhs_client.get_self_info())
