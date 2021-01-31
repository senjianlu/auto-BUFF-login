#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: E:\Github\Buff 爬虫测试\main.py
# @DATE: 2021/01/31 周日
# @TIME: 12:34:09
#
# @DESCRIPTION: 测试 Linux 系统下无头浏览器是否可以正常登录 Buff


import csv
import time
import selenium
from rab_python_packages import rab_chrome


# 登录信息
# Buff 用户/店铺名字，用以确认登录成功
buff_user_name_4_check = ""
# Buff 绑定的 Steam 登录用户名
steam_username = ""
# Buff 绑定的 Steam 登录密码
steam_password = ""
# 注意：只支持无令牌的 Steam 账号登录，如需令牌登录请自行修改代码


"""
@description: 切换至 Steam 登录窗口
-------
@param:
-------
@return:
"""
def switch_to_steam_login_window(driver):
    success_flg = False
    for window_handle in driver.window_handles:
        driver.switch_to.window(window_handle)
        if ("buff" not in str(driver.title).lower()
                and "steam" in str(driver.title).lower()):
            success_flg = True
            break
        else:
            continue
    return success_flg, driver

"""
@description: 切换至 Buff 窗口
-------
@param:
-------
@return:
"""
def switch_to_buff_window(driver):
    success_flg = False
    for window_handle in driver.window_handles:
        driver.switch_to.window(window_handle)
        if ("buff" in str(driver.title).lower()):
            success_flg = True
            break
        else:
            continue
    return success_flg, driver

"""
@description: Steam 登录
-------
@param:
-------
@return:
"""
def do_steam_login(driver):
    try:
        # Steam 用户名输入框
        steam_account_name_input = driver.find_element_by_id("steamAccountName")
        # Steam 密码输入框
        steam_password_input = driver.find_element_by_id("steamPassword")
        # 输入用户名和密码
        steam_account_name_input.send_keys(steam_username)
        steam_password_input.send_keys(steam_password)
        # 点击登录按钮
        driver.find_element_by_id("imageLogin").click()
        # 登录成功
        return True
    except Exception as e:
        # 登录失败
        print(e)
        return False
    
"""
@description: 等待 Steam 登录成功并自动关闭窗口
-------
@param:
-------
@return:
"""
def wait_steam_login_success(driver):
    for i in range(0, 10):
        if (len(driver.window_handles) > 1):
            time.sleep(2)
            continue
        else:
            return True
    return False

"""
@description: 等待 Buff 内置的轮询 Steam 登录生效，即 Steam 登录成功后稍等刷新页面
-------
@param:
-------
@return:
"""
def wait_buff_login_success(driver):
    for i in range(0, 10):
        try:
            login_user_divs = driver.find_elements_by_class_name("login-user")
            # 如果有对应 div 生成则说明已经登录成功。
            if (len(login_user_divs) > 0):
                return True
        except Exception:
            print("等待 Buff 轮询到 Steam 登录结果中...（丢失 driver，可能在刷新）")
        print("等待 Buff 轮询到 Steam 登录结果中...")
        time.sleep(2)
    return False

"""
@description: 验证登录后的用户名字是否正确
-------
@param:
-------
@return:
"""
def check_buff_user_name(driver):
    buff_user_name = driver \
                        .find_element_by_xpath('//*[@id="navbar-user-name"]') \
                        .text
    if (buff_user_name.strip() == buff_user_name_4_check.strip()):
        return True, buff_user_name
    else:
        return False, buff_user_name

"""
@description: Buff 登录
-------
@param:
-------
@return:
"""
def do_buff_login(driver):
    try:
        driver.get("https://buff.163.com")
        print("Buff 页面打开中...")
        # 获取 Buff 登录按钮
        buff_login_a = driver.find_element_by_xpath("/html/body/div[1]" \
                                                    + "/div/div[3]/ul/li/a")
        buff_login_a.click()
        print("Buff 登录按钮点击完毕！")
        time.sleep(2)
        # 获取 Steam 登录按钮
        steam_login_li = driver.find_element_by_class_name("icon_steam_small")
        steam_login_li.click()
        print("Steam 登录按钮点击完毕！")
        time.sleep(3)
        # 切换到 Steam 登录窗口并登录
        success_flg, driver = switch_to_steam_login_window(driver)
        do_steam_login(driver)
        if (wait_steam_login_success(driver)):
            # 切换回 Buff 窗口
            success_flg, driver = switch_to_buff_window(driver)
            wait_buff_login_success(driver)
            time.sleep(2)
        # 验证 Buff 用户名字
        success_flg, buff_user_name = check_buff_user_name(driver)
        if (success_flg):
            print("Buff 登录成功！登录用户：" + buff_user_name)
            return True
        else:
            print("Buff 登录失败！登录用户：" + buff_user_name + "，请检查步骤！")
    except Exception as e:
        print(e)
    return False


"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    # Windows 下需要新建浏览器用以接管
    # rab_chrome.build_chrome(9999)
    driver = rab_chrome.get_driver(9999, True, "socks5://127.0.0.1:1080")
    # 执行 Buff 登录操作
    do_buff_login(driver)
    # 关闭浏览器
    driver.quit()