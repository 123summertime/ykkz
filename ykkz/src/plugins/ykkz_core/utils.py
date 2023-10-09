import os
import re
import sys
import json
import base64
import random
import asyncio
import requests
import edge_tts
import subprocess
from datetime import datetime, timedelta

# --- Global Var ---
URL = "http://127.0.0.1:8000/v1/completions"
PATH = os.path.dirname(__file__)
Context, AIConfig, Multimedia = None, None, None
ContextPATH, AIConfigPATH, MultimediaPATH = (PATH + "/json/Context.json",
                                             PATH + "/json/Config.json",
                                             PATH + "/json/Multi.json")

with open(ContextPATH, "r", encoding='utf-8') as r:
    Context = json.load(r)
with open(AIConfigPATH, "r", encoding='utf-8') as r:
    AIConfig = json.load(r)
with open(MultimediaPATH, "r", encoding='utf-8') as r:
    Multimedia = json.load(r)

Data_user = {
    "prompt": "",
    "model": "rwkv",
    "stream": False,
    "max_tokens": AIConfig["max_tokens"],
    "temperature": AIConfig["Temperature"],
    "top_p": AIConfig["Top_p"],
    "presence_penalty": AIConfig["Presence Penalty"],
    "frequency_penalty": AIConfig["Frequency Penalty"]
}

Data_sys = {
    "prompt": "",
    "model": "rwkv",
    "stream": False,
    "max_tokens": 100,
    "temperature": 0.8,
    "top_p": 0.3,
    "presence_penalty": 0.4,
    "frequency_penalty": 0.4
}


# --- Classes ---
class Utils:
    @staticmethod
    def chatRequest(Prompt, data=None):
        '''
        发送HTTP请求，获取RWKV的回复
        '''
        global Data_user

        if not data:
            data = Data_user
        data["prompt"] = Prompt
        # print("+++++++++++++++++++++++++++++++++")
        # print(Prompt)
        # print("+++++++++++++++++++++++++++++++++")
        try:
            response = requests.post(URL, headers={"Content-Type": "application/json"}, data=json.dumps(data))
            if response.status_code == 200:
                return response.json()["choices"][0]["text"].split("\n\nUser:")[0]
        except:
            return None

    @staticmethod
    def cutReplys(AIReply):
        '''
        对AI回复的内容进行切片及修改
        '''
        print("Reply: ", AIReply)
        if not AIReply: return (None, None, None)

        AIReply = re.sub(r'(\.{3,}|。{3,}|•{3,}|:|：)', '。', AIReply)
        AIReply = re.sub(r'(?<!其)(他|她)', '你', AIReply)  # 防止被ntr
        emotion = Emotion(AIReply)
        splitted, pic, OriginalResponse, suffix = [], None, "", []
        for sentence in re.split(r'(?<=([.!?。！？]))', AIReply):
            if len(sentence.strip()) < 2 or 'AI' in sentence: continue
            sentenceTrim = sentence.strip('\n')
            OriginalResponse += sentenceTrim
            splitted.append(sentenceTrim)
            suffix.append(emotion.choiceAFace())
        if emotion.choiceAPic():
            pic = Utils.cvt2base64(emotion.choiceAPic())
        return (splitted, pic, OriginalResponse, suffix)

    @staticmethod
    def saveContext(context):
        '''
        保存上下文至本地
        '''
        global Context
        try:
            Context["context"] = context.split('\n\n', 1)[1]
            with open(PATH + "/json/Context.json", "w", encoding='utf-8') as w:
                json.dump(Context, w, indent=2, ensure_ascii=False)
            return True
        except:
            return False

    @staticmethod
    def saveInstruction(instruction):
        '''
        保存指令至本地
        '''
        global Context
        try:
            Context["instruction"] = instruction
            with open(PATH + "/json/Context.json", "w", encoding='utf-8') as w:
                json.dump(Context, w, indent=2, ensure_ascii=False)
            return True
        except:
            return False

    @staticmethod
    def showConfig():
        '''
        打印AI的参数
        :return:
        '''
        global AIConfig, Multimedia
        reply = f"项目: 值 [取值范围]\n" \
                f"Temperature: {AIConfig['Temperature']} [0-2]\n" \
                f"Top_p: {AIConfig['Top_p']} [0-0.8]\n" \
                f"Presence Penalty: {AIConfig['Presence Penalty']} [0-2]\n" \
                f"Frequency Penalty: {AIConfig['Frequency Penalty']} [0-2]\n" \
                f"max_tokens: {AIConfig['max_tokens']} [100-8100]\n" \
                f"FaceProbability: {Multimedia['FaceProbability']} [0-1]\n" \
                f"PicsProbability: {Multimedia['PicsProbability']} [0-1]\n" \
                f"voiceEnable: {Multimedia['voiceEnable']} [0/1]"
        return reply

    @staticmethod
    def editConfig(editItem, editValue):
        '''
        修改AI的参数
        '''
        global AIConfig, Multimedia
        if editItem in AIConfig:
            AIConfig[editItem] = float(editValue)
            with open(PATH + "/json/Config.json", "w", encoding='utf-8') as w:
                json.dump(AIConfig, w, indent=2, ensure_ascii=False)
            return True
        elif editItem in Multimedia:
            if editItem == "voiceEnable":
                Multimedia[editItem] = bool(int(editValue))
            else:
                Multimedia[editItem] = float(editValue)
            with open(PATH + "/json/Multi.json", "w", encoding='utf-8') as w:
                json.dump(Multimedia, w, indent=2, ensure_ascii=False)
            return True
        else:
            return False

    @staticmethod
    def getARandomTime(basicTime, plusOrMinus):
        '''
        在basicTime上下浮动plusOrMinus时间内返回一个随机时间
        '''
        try:
            basicTime = datetime.strptime(basicTime, "%H:%M")
            randomOffset = timedelta(minutes=random.randint(-plusOrMinus, plusOrMinus))
            randomTime = basicTime + randomOffset
            return randomTime.strftime("%H:%M")
        except:
            raise ValueError("Multi.json的Scheduler的key或timePlusOrMinus的参数不正确")

    @staticmethod
    def nekoize(sentence):
        '''
        转换为猫娘语
        '''
        global Data_sys
        Data_sys["temperature"] = 0.5
        Data_sys["top_p"] = 0.5
        prompt = Context["instruction"] + f"\n\nUser:复述以下句子,可以稍微自由发挥:{sentence}\n\nBot:"
        return Utils.chatRequest(prompt, Data_sys)

    @staticmethod
    def cvt2base64(filePath):
        '''
        发送表情包/语音的base64
        '''
        with open(filePath, "rb") as r:
            b64 = base64.b64encode(r.read()).decode('utf-8')
            return b64


class Emotion:
    def __init__(self, sentence):
        '''
        分析情绪
        '''
        global Data_sys, Multimedia

        self.emotion = "other"
        Data_sys["prompt"] = "Instruction:你将分析以下字符串的情绪，从['开心', '不高兴', '激动', '喜欢']中挑选最符合的一项，你只能回复一个单词，不要说明原因。"
        Data_sys["prompt"] += "\n\nUser:分析以下内容情绪。" + sentence + "\n\nBot:"
        Data_sys["temperature"] = 0.8
        Data_sys["top_p"] = 0.3
        try:
            Response = requests.post(URL, headers={"Content-Type": "application/json"}, data=json.dumps(Data_sys))
            if Response.status_code == 200:
                AIReply = Response.json()["choices"][0]["text"].split("\n\nUser:")[0]
                if "不高兴" in AIReply:
                    self.emotion = "unhappy"
                elif "开心" in AIReply:
                    self.emotion = "happy"
                elif "激动" in AIReply:
                    self.emotion = "excited"
                elif "喜欢" in AIReply:
                    self.emotion = "love"
        except:
            pass

    def choiceAFace(self):
        '''
        根据设置的概率和对应的情绪修改语句
        '''
        if random.random() < Multimedia["FaceProbability"]:
            return random.choice(Multimedia["Face"][self.emotion])
        else:
            return ""

    def choiceAPic(self):
        '''
        根据设置的概率和对应的情绪返回一张图片的路径
        '''
        if random.random() < Multimedia["PicsProbability"]:
            imageDirectory = PATH + "/pics/" + self.emotion
            imageFiles = [f for f in os.listdir(imageDirectory) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            imagePath = os.path.join(imageDirectory, random.choice(imageFiles))
            return imagePath
        else:
            return None


class Scheduled:
    def __init__(self, topic):
        '''
        定时任务
        '''
        global Data_user, Context
        prompt = f"Instruction:{Context['instruction']}\n\nUser:(你突然得知主人要{topic})(直接你想说的话)\n\nBot:"
        Data_sys["temperature"] = 0.5
        Data_sys["top_p"] = 0.3
        self.AIReply, self.pic, self.OriginalResponse, self.suffix = Utils.cutReplys(Utils.chatRequest(prompt, Data_sys))
    def sender(self):
        return (self.AIReply, self.pic, self.OriginalResponse, self.suffix)


class Voice:
    @staticmethod
    async def listIter(sentenceList):
        for sentence in sentenceList:
            yield sentence

    @staticmethod
    async def text2voice(sentenceList):
        '''
        调用degeTTS,把文字转换为语音,记录文件名
        '''
        nameList = []
        async for sentence in Voice.listIter(sentenceList):
            sentence = re.sub(r'\（[^)]*\）|【[^】]*】|\{[^}]*}|\([^)]*\)|(?=~)', "，", sentence)
            if len(sentence) <= 1:
                continue
            try:
                fileName = await Voice.edgeTTS(sentence)
                filePath = os.path.join(PATH + '/tts', fileName)
                if Multimedia["vitsEnable"]:
                    filePath = await Voice.customVoice(filePath, fileName)
                    await asyncio.sleep(1)
                nameList.append(filePath)
            except:
                pass
        for i in range(len(nameList)):
            nameList[i] = Utils.cvt2base64(nameList[i])
        return nameList

    @staticmethod
    async def edgeTTS(sentence):
        '''
        转换语音并保存
        '''
        voiceFileName = str(datetime.now().timestamp()).replace('.', '') + ".mp3"
        tts = edge_tts.Communicate(text=sentence,
                                   voice='zh-CN-XiaoyiNeural',
                                   rate=Multimedia['voiceSpeed'],
                                   volume=Multimedia['voiceVolume'])
        await tts.save(PATH + "/tts/" + voiceFileName)
        return voiceFileName

    @staticmethod
    async def customVoice(filePath, fileName):
        pthPath = Multimedia["pthPath"]
        vitsPath = Multimedia["vitsPath"]
        configPath = Multimedia["configPath"]
        speaker = Multimedia["speaker"]
        trans = Multimedia["trans"]

        originalDir = os.getcwd()
        ttsDir = os.path.join(PATH, "tts")
        try:
            os.chdir(vitsPath)
            command =   f'python inference_main.py ' \
                        f'-m "{pthPath}" ' \
                        f'-c "{configPath}" ' \
                        f'-n "{filePath}" ' \
                        f'-t "{trans}" ' \
                        f'-s "{speaker}" ' \
                        f'-a ' \
                        f'-sp "{ttsDir}" ' \
                        f'-fn "{fileName}"'
            process = subprocess.Popen(command, shell=True)
            process.wait()
        finally:
            os.chdir(originalDir)
        return os.path.join(ttsDir, fileName + '.flac')