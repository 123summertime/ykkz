<h1 align="center">ykkz</h1>

## 介绍



## 安装前准备

- **[python 3.8](https://www.python.org/downloads/release/python-389/)**
- **[JDK](https://www.oracle.com/java/technologies/downloads/#java17)**
- **[RWKV-Runner](https://github.com/josStorer/RWKV-Runner)**
- **[FFmpeg](https://ffmpeg.org/download.html)**

## 安装

### 克隆本项目
`git clone`本项目并放置于你的python虚拟环境中

安装依赖
```powershell
pip install -r requirements.txt
```
> 提示Microsoft Visual C++ 14.0 is required?
> 在pypi上下载对应的whl安装或下载visual studio解决。

### 运行RWKV-Runner
[RWKV-Runner文档](https://github.com/josStorer/RWKV-Runner/blob/master/README_ZH.md)


### 配置go-cqhttp
在`config.yml`中填入`uin`和`password`

### 配置ykkz_core
ykkz_core作为nonebot的插件运行，负责处理用户的信息，RWKV的回复及sovits的调用。

---

`ykkz/ykkz/src/plugins/ykkz_core/json/Config.json`

对应RWKV里的API参数

| 键           | 默认值 | 数据类型  | 功能 |
|-------------|-----|-------|----|
| Temperature | 1.6 | float |    |
| Top_P       | 0.7 | float |    |
| max_tokens  | 150 | int   |    |

---

`ykkz/ykkz/src/plugins/ykkz_core/json/Context.json`

| 键             | 默认值 | 数据类型 | 功能      |
|---------------|----|-----|---------|
| instruction   |    | str | AI的人设   |
| context       | "" | str | 记录对话的内容 |

---

`ykkz/ykkz/src/plugins/ykkz_core/json/Multi.json`

| 键                    | 默认值  | 数据类型                 | 功能                                                               |
|----------------------|-------|----------------------|------------------------------------------------------------------|
| FaceProbability      | 0.5   | float                | 在句末加上颜文字的概率，取值范围`[0,1]`                                          |
| Face                 | {}    | dict[str, list[str]] | 颜文字字典                                                            |
| PicsProbability      | 1     | float                | 在对话最后加上表情包的概率，取值范围`[0,1]`                                        |
| **Scheduler**        | {}    | dict[str, list[str]] | 定时任务，将会在`key`的时间主动发送关于`value`的信息                                 |
| timePlusOrMinus      | 3     | int                  | 在`Scheduler`中，将在设置的时间基础上上下浮动`timePlusOrMinus`分钟，然后随机选择其中一个时间点发送。 |
| _**ScheduledGroup**_ | 0     | int                  | 在`Scheduler`中计划发送的信息发送向哪个群                                       |
| **voiceEnable**      | false | bool                 | `true`时开启语音回复，`false`时使用文字回复                                     |
| voiceSpeed           | -5%   | str                  | 语速                                                               |
| voiceVolume          | +5%   | str                  | 语音音量                                                             |
| **vitsEnable**       | false | bool                 | `true`时使用语音模型的音色回复，`false`时使用edgetts的音色回复  <br/>为`true`时以下设置有效   |
| **vitsPath**         | ""    | str                  | `vits`项目的绝对路径, `vits`的相对路径是`ykkz/ykkz/vits`                      |
| **pthPath**          | ""    | str                  | `vits4.0`模型文件绝对路径  |                              
| **configPath**       | ""    | str                  | `vits`模型文件的`config.json`的绝对路径                                    |
| **speaker**          | ""    | str                  | 该模型的说话人                                                          |
| trans                | 0     | int                  | 音调变化 +8为提高8度                                                     |
