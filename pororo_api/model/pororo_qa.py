from pororo import Pororo

def func_qa(question, original_news_data):
    mrc = Pororo(task = "mrc", lang = "ko")

    return mrc(question, original_news_data)
