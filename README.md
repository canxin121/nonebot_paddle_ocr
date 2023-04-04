<p align="center">
  <a href="https://github.com/your_username/nonebot_paddle_ocr"><img src="https://github.com/canxin121/nonebot_paddle_ocr/blob/main/demo/logo_transparent.png" width="200" height="200" alt="nonebot_paddle_ocr"></a>
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
# nb安装
```
nb plugin install nonebot-paddle-ocr
```
# pip安装并把本插件添加到pyproject.toml中  
```
pip install nonebot-paddle-ocr
```
# 手动安装
下载/git后放到nonebot2的plugin/site_pacages下使用
需要安装依赖，在本项目目录下pip install -r requirements即可
## 使用方法

1. 本地识别：私聊或发送 `/ocr` 即可开始识别，后可连续发送照片或pdf，发送pdf后会提示输入识别页数，0代表全部（页数太多会导致识别并回复很慢，且字数超长可能发送失败）。发送对应的语言英文缩写可以切换语言（持续生效），发送 `/结束` 即可结束当前用户对话，用户互不影响。
2. 网页api识别：发送 `/apiocr`，仅支持中英文和数字标点的照片，不可切换语言，其余用法同上。

## 示例
  
| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img src="https://github.com/canxin121/nonebot_paddle_ocr/blob/main/demo/demo%20(1).jpg" width="200"> | <img src="https://github.com/canxin121/nonebot_paddle_ocr/blob/main/demo/demo%20(2).jpg" width="200"> | <img src="https://github.com/canxin121/nonebot_paddle_ocr/blob/main/demo/demo%20(3).jpg" width="200">|

## 开源协议

本项目使用了Paddle OCR，并遵守了Apache License 2.0开源协议。
