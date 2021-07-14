from pororo import Pororo

def func_qa(question, original_news_data):
    mrc = Pororo(task = "mrc", lang = "ko")

    print(mrc(question, original_news_data))

    return mrc(question, original_news_data)
