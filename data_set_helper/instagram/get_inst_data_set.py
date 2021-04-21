from bs4 import BeautifulSoup
from data_set_helper.data.message_payload import MessagePayload

filePath = 'D:\\projects\\nlp-chat-bot\\lowa.card_20210411\\messages\\inbox\\alena_kuchko_nvsbrg-p3w\\message_1.html'
file = open(filePath, mode='r', encoding='utf8')
testFile = file.read()

messageClassName = 'pam _3-95 _2ph- _2lej uiBoxWhite noborder'
messageTextClassName = '_3-95 _2let'



def get_data_set(text, currenUserName):
    soup = BeautifulSoup(text, features='lxml')
    messagesDiv = soup.find('div', {'role': 'main'})
    messageDivList = messagesDiv.find_all('div', {'class': messageClassName})
    messagesInfoList = list()
    for message in messageDivList:
        info = getPayloadInfo(message, currenUserName)
        messagesInfoList.append(info)
    messagesInfoList.reverse()
    return messagesInfoList


def getPayloadInfo(message, currentUserName):
    userName = message.find('div').text.strip()
    messageDiv = message.find('div', {'class': messageTextClassName})
    messageText = messageDiv.text.strip() if messageDiv else ''
    isQuestion = currentUserName != userName

    return MessagePayload(userName, messageText, isQuestion)

## getDataSet(testFile, 'ФОТОГРАФ МИНСК')
