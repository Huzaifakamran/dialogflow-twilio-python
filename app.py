from flask import Flask, request, jsonify
import google.cloud.dialogflow_v2 as dialogflow
import os
import uuid
from dotenv import load_dotenv
from twilio.rest import Client

#Download the json key file from GCP with Dialogflow API client role And paste in the same directory  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_key.json'                                                                                       
load_dotenv()
app=Flask(__name__)

@app.route('/webhook',methods = ['GET','POST'])
def webhook():
    try:
        incoming_que = request.values.get('Body', '').lower()
        fromNumber = request.values.get('From', '').lower()
        print("Question: ", incoming_que)
        print("From: ", fromNumber)
        session_id = str(uuid.uuid4())

        result = detect_intent(session_id,incoming_que)
        print("Type of Result",type(result))
        print("BOT Answer: ", result)
        SendTwilioSMS(result,fromNumber)

    except Exception as e:
        print(e)
        pass
    return "True"

def detect_intent(session_id, incoming_que):
    session_client = dialogflow.SessionsClient()
    PROJECT_ID = 'lanwebbe-upwork-9rly'
    # session_id = user_id
    session_path = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.types.TextInput(text=incoming_que, language_code='en-US')
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session_path, query_input=query_input)
    # print(response)
    print(response.query_result.fulfillment_text)
    return response.query_result.fulfillment_text


    # Send user message to Dialogflow and get response

def SendTwilioSMS(result,number):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body= str(result),
                        from_='+61482075599',
                        to = number
                    )

    print(message.sid)
    return message

if __name__ == '__main__':
    app.run(debug=True)