import io
import os
import urllib.request

import requests
from nonebot import on, on_command, on_notice
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, PrivateMessageEvent, NoticeEvent, NotifyEvent, \
    MessageEvent
from nonebot.internal.rule import Rule
from nonebot.rule import to_me, is_type, command
from nonebot.typing import T_State
from paddleocr import PaddleOCR

from .api_ocr import api_paddle_ocr

ocr_start = False

que = []
async def _is_ocr_start_(event:Event) -> bool:
    if event.post_type == 'message' or event.post_type == 'notice':
        return ocr_start and event.user_id in que
    else:
        return False

is_ocr_start = Rule(_is_ocr_start_)


def paddle_ocr_img(url, language):
    ocr = PaddleOCR(lang=language)
    results = ocr.ocr(url)
    resulttext = ''
    for result in results:
        for line in result:
            resulttext += str(line[1][0]) + ' '
    return resulttext


def paddle_ocr_pdf(file, language, pages):
    resulttext = ''
    ocr = PaddleOCR(use_angle_cls=True, lang=language, page_num=pages)
    results = ocr.ocr(file, cls=True)
    for result in results:
        for line in result:
            resulttext += str(line[1][0]) + ' '
    return resulttext


start_ocr = on(rule=to_me() & command('ocr'), priority=2)



language = dict()
@start_ocr.handle()
async def handle_ocr(event: MessageEvent):
    global ocr_start,que,language
    ocr_start = True
    user_id = event.user_id
    que.append(user_id)
    language.update({user_id:'ch'})
    await start_ocr.send("开始本地ocr识别模式,支持中英文(ch)、英文(en)、法语(french)、德语(german)、韩语(korean)、日语(japan),"
                         "默认ch，如需切换请在相应图片或pdf前先输入语言（英文简称），再发送图片或pdf。")


page = 0
enterpage = 0
name = ''
url = ''
ocr = on(rule=is_type(NoticeEvent, MessageEvent) & is_ocr_start, priority=2)


@ocr.handle()
async def get_pic(event: Event):
    global language, ocr_start, page, enterpage, name, url
    userid_ = event.user_id
    if userid_ in que:
        lang = ["ch", "en", "fr", "german", "korean", "japan"]
        if event.post_type == 'message':
            getmsg = event.message
            for segment in getmsg:
                if segment.type == 'image':
                    await start_ocr.send("正在识别~~")
                    url = segment.data['url']
                    resulttext = paddle_ocr_img(url, language[userid_])
                    await start_ocr.send(resulttext)
                elif segment.type == 'text':
                    if getmsg[0].data['text'] == '/结束':
                        que.remove(event.user_id)
                        await start_ocr.send('关闭当前用户ocr模式')
                        if len(que)==0:
                            ocr_start = False
                            await start_ocr.finish('已全部关闭')
                            await ocr.finish()


                    elif getmsg[0].data['text'] in lang:
                        language[userid_] = getmsg[0].data['text']
                        await start_ocr.send(f"切换为{language[userid_]}")
                    elif getmsg[0].data['text'].isdecimal and enterpage == 1:
                        page = int(getmsg[0].data['text'])
                        enterpage += 1
                        await start_ocr.send('正在识别~')
                        resulttext = ''
                        try:
                            response = requests.get(url)  # 发送GET请求
                            with open("file.pdf", "wb") as f:  # 以二进制模式打开本地文件
                                f.write(response.content)  # 将PDF内容写入文件
                            resulttext = paddle_ocr_pdf(file='file.pdf', language=language[userid_], pages=page)
                            os.remove('file.pdf')
                        except  requests.exceptions.RequestException:
                            await start_ocr.send('网络出现错误，下载失败，请重试')
                        finally:
                            enterpage = 0
                            await start_ocr.send(resulttext)

                    else:
                        await  start_ocr.send("请发送纯图片或文件，如要结束，请发送/结束")
        elif event.post_type == 'notice':
            if event.notice_type == 'group_upload':
                name = event.file.name
                url = event.file.url
            else:
                name = event.file['name']
                url = event.file['url']
            if name.split(".")[-1] == 'pdf':
                enterpage += 1
                if enterpage == 1:
                    await start_ocr.send('检测到pdf文件，请输入要识别的页数（纯数字）')
            else:
                resulttext = paddle_ocr_img(url, language[userid_])
                resulttext = str(resulttext)
                await start_ocr.send(resulttext)
                print(1)
ocr_api = on_command("apiocr", rule=to_me())

@ocr_api.handle()
async def handle_ocr(bot: Bot, event: Event, state: T_State):
    await ocr_api.send("开始apiocr识别模式,支持中英文和数字")


@ocr_api.got("pic")
async def get_pic(bot: Bot, event: Event, state: T_State):
    getmsg = event.get_message()
    for segment in getmsg:
        if segment.type == 'image':
            await ocr_api.send("正在识别~~")
            url = segment.data['url']
            response = urllib.request.urlopen(url)
            img = io.BytesIO(response.read())
            resulttext = api_paddle_ocr(img=img)
            await ocr_api.reject(resulttext)
        elif segment.type == 'text':
            if getmsg[0].data['text'] == '/结束':
                await ocr_api.finish("关闭ocr识别模式")
            else:
                await  ocr_api.send("请发送纯图片，如要结束，请发送/结束")
