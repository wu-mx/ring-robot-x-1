import traceback
import model.hook
import model.logger as logger
import requests
import model.config
import json
import os

def hook_com(runMode,hookName):
    if runMode=="reg":
        model.hook.register_hook_fast(hookName)
        return "success"
    elif runMode=="run":
        model.hook.runhook_fast(hookName)
        return "success"
    else:
        return "runMode is missing"

def func_com(string,tts="tts"):
    return model.func.run(string,tts)

def tts_com(string):
    model.tts.tts(string)
    return "success"

def asr_com(string):
    model.asr.asr(string)
    return "success"

def help_com(string="all"):
    if string=="all":
        print("已加载命令：")
        for key, value in commands.items():
            print(key,end=" ")
        print()
        for key, value in commands.items():
            try:
                print(key+" : "+helps[key])
            except:
                print(key+" : 没有找到文档。")
    elif string=="list":
        los=[]
        for key, value in commands.items():
            los.append(key)
        return json.dumps(los)
    else:
        try:
            return string + " : " + helps[string]
        except:
            return string + " : 没有找到文档。"
    return "success"

def hello_ringrobotx():
    print("Now playing: Rick Astley - Never Gonna Give You Up")
    return "Hello RingRobotX"

def check_update():
    now=model.config.fastGetConfig("api-version")
    response = requests.get('https://gitee.com/lkteam/ring-robot-x/raw/'+now["branch"]+'/config/api-version.json')
    if float(json.loads(response.text)["RingRobotX"]) > float(now["RingRobotX"]):
        return "OK"
    else:
        return "No"

def update_robotx(yesorno='mita'):
    if yesorno == "mita":
        logger.moduleLoggerMain.info("[CLI] 更新前，程序会将config目录备份。更新后，除了config目录，您对于程序源代码所做出的改动会被覆盖！开发人员不为您数据的损失负责！确认继续请输入 update y")
        return "[CLI] 更新前，程序会将config目录备份。更新后，除了config目录，您对于程序源代码所做出的改动会被覆盖！开发人员不为您数据的损失负责！确认继续请输入 update y"
    else:
        os.system('cp ./config/ ../config')# 摆烂型更新
        os.system('git fetch --all')
        os.system('git reset --hard origin/'+model.config.fastGetConfig("api-version")["branch"])
        os.system("git pull")
        os.system("mv -f ../config/ ./config")
        return "OK"
    # cp ./config/ ../config && git pull && mv ../config/ /config

def config_com(mode,key="all",fileType="json",encode='utf-8',value="000"):
    if mode=="list":# list
        return os.listdir("./config")
    elif mode=="get":# get Turing_RobotChat
        return json.dumps(model.config.fastGetConfig(key,fileType,encode))
    elif mode=="set":# set Turing_RobotChat json utf-8 {"......"}
        pathn = model.config.APPConfig()
        pathn.setModelName(key)
        pathn.setConfig(value,fileType,encode)
        return "OK"

helps={
    "hook":"hook [runmode] [hookname] | runmode可输入reg或run，分别代表初始化hook列表和运行hook",
    "func":"func [string] | 输入你想对RingRobotX说的话。",
    "tts":"tts [string] | 运行tts ===== asr [path] | 运行asr",
    "asr":"tts [string] | 运行tts ===== asr [path] | 运行asr",
    "help":"help (command) 获取（某一指令的）帮助",
    "hello":"彩蛋。",
    "check-update":"check-update | 检查更新",
    "update":"update | 更新程序",
    "config":"config [list/get/set] 配置名 扩展名 解码 值(仅当set时可用) | 列出、获取、设置配置文件。\n 例如：config list（列出） \n config get Turing_RobotChat（获取） \n config set Turing_RobotChat json utf-8 {}（设置）"
}

commands={
    "hook":hook_com,
    "func":func_com,
    "tts":tts_com,
    "asr":asr_com,
    "help":help_com,
    "hello":hello_ringrobotx,
    "check-update":check_update,
    "update":update_robotx,
    "config":config_com
}

def command_registry(command,func):
    global commands
    commands[command]=func

def help_registry(command,string):
    global helps
    helps[command]=string

class console(object):
    def commandRun(self,command,param):
        try:
            logger.moduleLoggerMain.info("[CLI] 运行指令：" + command + " 参数"+str(*param))
            ret=commands[command](*param)
            logger.moduleLoggerMain.info("[CLI] 指令返回：" + str(ret))
            return ret
        except:
            logger.moduleLoggerMain.info("[CLI] 报告！指令" + command + " 无法正确加载")
            logger.moduleLoggerMain.info(traceback.format_exc())
            return "Error,dumped"