<p align="center">
  <a href="https://github.com/your_username/nonebot_paddle_ocr"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot_paddle_ocr"></a>
</p>
<div align="center">

# nonebot_paddle_ocr

✨*基于Nonebot的插件，能够将Paddle OCR接入QQ使用*✨
  
<div align="left">
  
## 功能

- 支持在群聊和私聊中使用
- 支持图片和PDF格式
- 支持连续对话

## 安装

目前未上架，可自行下载/git后放到nonebot2的plugin/site_pacages下使用
需要安装依赖，在本项目目录下pip install -r requirements即可
## 使用方法

1. 本地识别：私聊或发送 `/ocr` 即可开始识别，后可连续发送照片或pdf，发送pdf后会提示输入识别页数，0代表全部（页数太多会导致识别并回复很慢，且字数超长可能发送失败）。发送对应的语言英文缩写可以切换语言（持续生效），发送 `/结束` 即可结束当前用户对话，用户互不影响。
2. 网页api识别：发送 `/apiocr`，仅支持中英文和数字标点的照片，不可切换语言，其余用法同上。

## 示例

// 在这里添加示例图片或代码
