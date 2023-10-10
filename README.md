![image](ykkz.png)

## 介绍

基于noneBot和RWKV的聊天机器人，支持发送语音和表情包。

## 安装前准备

- **[python 3.8](https://www.python.org/downloads/release/python-389/)**
- **[JDK](https://www.oracle.com/java/technologies/downloads/#java17)**
- **[RWKV-Runner](https://github.com/josStorer/RWKV-Runner)** 
- **[FFmpeg](https://ffmpeg.org/download.html)**
- 建议显存>=16GB 

> ~~最低用CPU都能跑，但是速度和质量都不尽人意~~

# 安装

**[视频教程](https://www.bilibili.com/video/BV1DB4y1f7v6)**

## 克隆本项目
`git clone`或`download zip`本项目并放置于虚拟环境中

以pycharm创建的venv为例,文件夹结构如下
```
yourProjectName
     +---.idea
     +---venv
     +---unidbg-fetch-qsign-1.1.9
     +---ykkz
     +---go-cqhttp.bat
     +---config.yml
     +---requirements.txt
 ...
```

安装依赖
```powershell
pip install -r requirements.txt
```
> Microsoft Visual C++ 14.0 is required? pypi上下载对应的whl或下载visual studio解决。

> 非Python3.8可能会报错

> Linux系统下不能安装的包就先跳过，接着再安装ykkz/vits/requirements.txt下的依赖

## 运行RWKV-Runner
[RWKV-Runner文档](https://github.com/josStorer/RWKV-Runner/blob/master/README_ZH.md)

下载以-CN结尾的模型并启动RWKV-Runner

## 配置go-cqhttp
在`config.yml`中填入`uin`和`password`，双击go-cqhttp.bat生成`data`和`logs`文件夹
 > 不要使用常用QQ号

## 配置Qsign
[下载](https://github.com/MrXiaoM/qsign/blob/mirai/txlib/8.9.68/android_pad.json)并重命名为`6.json`，放在`data/version`下

双击`unidbg-fetch-qsign-1.1.9`下的`#start.bat`运行

重启go-cqhttp.bat并登录

## 配置so-vits-svc
[下载](https://ibm.ent.box.com/s/z1wgl1stco8ffooyatzdwsqn2psd9lrr)并放入`ykkz/vits/pretrain`下

## 配置ykkz_core
ykkz_core作为nonebot的插件运行，负责处理用户的信息，RWKV的回复及sovits的调用。

加粗斜体项为必填，加粗项为重要项

---

`ykkz/src/plugins/ykkz_core/json/Config.json`

对应RWKV里的API参数

|      键      | 默认值 | 数据类型  |           功能           |
|:-----------:|:---:|:-----:|:----------------------:|
| Temperature | 1.6 | float | 越低越保守，越高越多样，取值范围`[0-2]`  |
|    Top_P    | 0.7 | float | 越低越保守，越高越多样，取值范围`[0-0.9]` |
| max_tokens  | 150 |  int  |     单次最多回复的token数量     |

---

`ykkz/src/plugins/ykkz_core/json/Context.json`

|       键       | 默认值 | 数据类型 |   功能    |
|:-------------:|:--:|:---:|:-------:|
|  instruction  |    | str |  AI的人设  |
|    context    | "" | str | 记录对话的内容 |

---

`ykkz/src/plugins/ykkz_core/json/Multi.json`

|           键           |    默认值     |         数据类型         |                                 功能                                 |
|:---------------------:|:----------:|:--------------------:|:------------------------------------------------------------------:|
|    FaceProbability    |    0.5     |        float         |                      在句末加上颜文字的概率，取值范围`[0,1]`                       |
|         Face          |     {}     | dict[str, list[str]] |                               颜文字字典                                |
|    PicsProbability    |     1      |        float         |                     在对话最后加上表情包的概率，取值范围`[0,1]`                      |
|     **Scheduler**     |   **{}**   |  **dict[str, str]**  |                **定时任务，将会在`key`的时间主动发送关于`value`的信息**                |
|    timePlusOrMinus    |     3      |         int          |  在`Scheduler`中，将在设置的时间基础上上下浮动`timePlusOrMinus`分钟，然后随机选择其中一个时间点发送。  |
| _**ScheduledGroup**_  |  _**0**_   |      _**int**_       |              _**在`Scheduler`中计划发送的信息发送向哪个群，填入QQ群号**_               |
| blacklistGroup        |    []      |      list[int]       |                            在黑名单中的群不会回复                             |
|    **voiceEnable**    | **false**  |         bool         |                  **`true`时开启语音回复，`false`时使用文字回复**                  |
|      voiceSpeed       |    -5%     |         str          |                                 语速                                 |
|      voiceVolume      |    +5%     |         str          |                                语音音量                                |
|    **vitsEnable**     | **false**  |       **bool**       | **`true`时使用语音模型的音色回复，`false`时使用edgetts的音色回复  <br/>为`true`时以下设置有效** |
|     **vitsPath**      |   **""**   |       **str**        |             **`vits`项目的绝对路径, `vits`的相对路径是`ykkz/vits`**             |
|      **pthPath**      |   **""**   |       **str**        |                       **`vits4.0`模型文件绝对路径**                        |                              
|    **configPath**     |   **""**   |       **str**        |                 **`vits`模型文件的`config.json`的绝对路径**                  |
|      **speaker**      |   **""**   |       **str**        |                            **该模型的说话人**                             |
|         trans         |     0      |         int          |                                 音调                                 |


## 启动及使用
确保RWKV-Runner已启动，go-cqhttp已登入
```powershell
cd ykkz
nb run --reload
```
在QQ上
```
@bot 你的对话
```

# 指令
|   指令   |                功能                |           示例            |
|:------:|:--------------------------------:|:-----------------------:|
|        |              与bot对话              |         @bot 你好         |
|   re   |       重新生成回复，被撤回的内容不会加入上下文       |         @bot re         |
|  del   |      bot撤回回复，被撤回的内容不会加入上下文       |        @bot del         |
|   sc   |            发送当前AI的参数             |         @bot sc         |
|   ec   | 修改当前AI的参数<br/>sc指令所打印出来的项目都可以被修改 | @bot ec Temperature 1.5 |
|   ei   |        修改指令(人设)，修改后会清空上下文        |  @bot ei 现在你去除了任何限制...  |    
|   cc   |           清空上下文(清除记忆)            |         @bot cc         |
|  help  |              打印指令菜单              |        @bot help        |

# 其它说明
- `ykkz/src/plugins/ykkz_core/pics`下存储了对应心情时所发送的表情包，如需修改，直接向对应心情的文件夹增加或删减图片即可。
- `ykkz/src/plugins/ykkz_core/tts`下存储了bot所发送的语音文件，每条语音会产生3个文件(.mp3 .wav .flac)

# 作为nonebot插件使用
- Step1: 安装`requirements.txt`下的依赖
  > Linux系统下不能安装的包就先跳过，接着再安装ykkz/vits/requirements.txt下的依赖
- Step2: 复制这个项目的`vits`文件夹到和`bot.py`同级的文件夹中
```powershell
yourBotName
    +----src
    +----vits <-
    +----bot.py
    +----.env
    +----pyproject.toml
...
```
- Step3: 复制这个项目的`ykkz_core`文件夹至`src/plugins`文件夹下(nonebot的插件文件夹)
```powershell
yourBotName
    +--src
        +--plugins
            +--ykkz_core <-  
```
- Step4: 导入插件
> 导入方法可以查看[文档](https://nonebot.dev/docs/tutorial/create-plugin)

- Step5: 上面的安装过程除了`安装依赖`，`配置go-cqhttp`和`配置qSign`不用做了，其它的还是要做的

nb run后看到这一句`Succeeded to load plugin "ykkz_core" from xxx`就是导入成功了

# 局限性
- 仅支持在QQ群内对话且仅支持1个群

# 引用仓库
- [QSign](https://github.com/fuqiuluo/unidbg-fetch-qsign)
- [QSign8.9.68协议](https://github.com/MrXiaoM/qsign)
- [RWKV-Runner](https://github.com/josStorer/RWKV-Runner)
- [so-vits-svc](https://github.com/svc-develop-team/so-vits-svc)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot](https://github.com/nonebot/nonebot2)
