# 健康打卡定时自动脚本（GitHub Actions  版）

**注意**：本 master 分支版本代码使用 GitHub Actions 定时运行，无需部署在服务器。如需在服务器中运行，请使用 service 分支中的代码。

## Description

**特此声明**：项目用于学习交流，仅用于各项无异常时打卡，如有身体不适等情况还请自行如实打卡！

* 可定时，默认为每天 00:06-00:15随机
* 默认每次提交上次所提交的内容 （只有时间部分更新）

##  Usage

## 获取 Cookie

获取 eai-sess 和 UUkey

1. 打开健康打卡页面 [https://wfw.scu.edu.cn/ncov/wap/default/index](https://wfw.scu.edu.cn/ncov/wap/default/index)

2. 若跳转至此页面，输入学工号与统一身份认证密码进行登录![](https://s2.loli.net/2022/08/13/oGUukrQn4F1iJyP.jpg)

3. 登陆后按F12，直接在Cookie中找到 eai-sess 和 UUke，如图

   ![image-20220814004711579](http://c7f49cfdf594b0ba.oss-cn-hangzhou.aliyuncs.com/img/typora/image-20220814004711579.png)

如果以上方法未能找到 Cookie 中的 eai-sess 和 UUke，请尝试按下图方法搜索：

1. 打开 Network 选项，勾选 Preserve log![](https://s2.loli.net/2022/08/13/KWG1ux2m7DI5Hi8.png)

2. 点击放大镜处的搜索按钮![](https://s2.loli.net/2022/08/13/ZPXw5W8AjQn6Jh7.png)

3. 搜索 eai-sess![](https://s2.loli.net/2022/08/13/uMAm2G8Lx5gS7Js.jpg)

4. 搜索 UUkey![](https://s2.loli.net/2022/08/13/th56UXkpxwKZ2PD.jpg)

### 运行方式

1. import 本项目到你的个人账号

    ![](https://s2.loli.net/2022/08/13/cg2Rpn7OqKavzmM.png)

    **注意**：一定勾选 **Private** （私有）

    否则所有 Action 的日志将会公开，包括日志里的**个人信息**

    如下图配置即可：

    ![](https://s2.loli.net/2022/08/13/jAmQkhe9ta7s5vP.jpg)

2. 导入后更改 Actions 设置

    在导入后将 Action 设置中**第一个选项** (Actions permissions) 改为选中**第一个**

    **否则 Actions 将无法运行**

    ![](https://s2.loli.net/2022/08/13/IzprhGtUfyAQdHV.jpg)

3. 设置 Secrets

     从 Github 中进入刚刚导入到你的个人账号下的本项目，打开项目的 Settings->Secrets 页面

![](https://s2.loli.net/2022/08/13/xbuE7Flyn3st1k9.png)

点击 New Secret 按钮新建两个密码：

 EAI_SESS：你的 eai-sess cookie

 UUKEY：你的 UUkey cookie

\* 学工号和统一身份认证密码 (USERNAME 和 PASSWORD) **暂时先不需要**，已经添加的**可以删除**（因为四川大学登录比中南大学复杂一些，有验证码 : | 还没弄出来）

4. 启动定时打卡

    进入 Code 页面，点击修改按钮

    ![](https://s2.loli.net/2022/08/13/jaO4nR5xJ1NtDWY.png)

    在 readme 文件中随意修改任意字符（比如加个空格），然后点击下方的 Commit Changes 即可激活每日定时打卡脚本

    ![](https://s2.loli.net/2022/08/13/z13PKxGfkaQroVd.png)

5. 查看运行情况

    打开 Actions 页面，此时在 workflows 中应该出现了正在运行的工作流。当提交文件时会马上进行一次打卡，以后将会默认在每天的 00:05 进行打卡

    ![](https://s2.loli.net/2022/08/13/7pHABnJcv8Cdhji.png)

    效果图：

    ![](https://s2.loli.net/2022/08/13/LMmujI9Wthx6lcS.png)

    ![](https://s2.loli.net/2022/08/13/3CqFYj1Un28GgQw.png)
## 修改打卡时间

打开项目中的 /.github/workflows/python-package.yml 文件，修改 corn 中的值，注意使用 UTC 零区时间。

例如，当前默认打卡时间是北京时间 (UTC+8) 每天 00:05，换算成 UTC 零区时间为 16:05。

随机时间只需要在 `auto.py` 中修改 `time.sleep()` 中的数字即可。

更多关于时间的具体书写格式请参考 [POSIX cron 语法](https://crontab.guru/) 和 [官方文档](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows#)。

![](https://s2.loli.net/2022/08/13/8TqZ52M4haBjtbP.png)

![](https://s2.loli.net/2022/08/13/nChqYb4vEFesruK.png)

---

如本项目对您有所帮助，请帮忙点一个⭐Star 支持一下作者。如有任何问题欢迎提交 issue 与我联系。

参考开源仓库：

1. [浙大 nCov 健康打卡定时自动脚本](https://github.com/Tishacy/ZJU-nCov-Hitcarder)
2. [北京化工大学 COVID-19 自动填报脚本](https://github.com/W0n9/BUCT_nCoV_Report)
3. [中南大学 nCov 健康打卡定时自动脚本](https://github.com/lxy764139720/Auto_Attendance)
