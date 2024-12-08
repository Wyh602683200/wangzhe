import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://api.zxki.cn/api/wangzhe?"

@plugins.register(name="wangzhe",
                  desc="获取王者英雄人物情况",
                  version="1.0",
                  author="wyh",
                  desire_priority=100)
class wangzhe(Plugin):
    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【王者/王者荣耀 + 英雄名称】获取王者英雄人物情况"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        
        if self.content.startswith("王者"):
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.wangzhe()
            if result != None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS

    def wangzhe(self):
        url = BASE_URL_DM
        params = {"msg":self.content.replace("王者 ", "").replace("王者荣耀 ", "")}            
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        
        logger.info(f"url:{url}")
        logger.info(f"params:{params}")
        
        try:
            response = requests.get(url, params=params,headers=headers)
            if response.status_code == 200:
                json_data = response.text
                logger.info(json_data)
                return json_data
            else:
                logger.info(response.status_code)
                logger.info(f"接口异常：{response.status_code}")
        except Exception as e:
            logger.error(f"接口异常：{e}")
                
        logger.error("所有接口都挂了,无法获取")
        return None
