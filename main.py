@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if "勤怠" in event.message.text and "登録" in event.message.text :
        # 登録処理

        replyText = "登録しました"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=replyText))

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))