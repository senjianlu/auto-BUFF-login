# auto-BUFF-login
使用 selenium 自动化登录 BUFF 的测试 DEMO。（Windows 和 Linux 下均测试通过）  
需要环境：Python3，Chrome 和 chromedirver 版本匹配  
使用方法：  

```bash
git clone https://github.com/senjianlu/auto-BUFF-login.git --recurse
cd auto-BUFF-login
python3 main.py
```

**注意：运行前请修改 main.py 中部分内容**  

```python
...
...
...
# 登录信息
# Buff 用户/店铺名字，用以确认登录成功
buff_user_name_4_check = ""
# Buff 绑定的 Steam 登录用户名
steam_username = ""
# Buff 绑定的 Steam 登录密码
steam_password = ""
# 注意：只支持无令牌的 Steam 账号登录，如需令牌登录请自行修改代码
...
...
...
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
...
...
...
```

