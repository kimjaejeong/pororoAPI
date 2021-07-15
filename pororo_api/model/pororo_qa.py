from pororo import Pororo

def func_qa(question, original_news_data):
    mrc = Pororo(task = "mrc", lang = "ko")

    answer_sentence = mrc(question, original_news_data)[0]
    if answer_sentence == "":
        return "[AI 답변]\nAI가 해석하지 못한 질문입니다. 다시 입력 바랍니다."
    else:
        return answer_sentence
