from flask import Flask, request, jsonify, render_template
import uuid,os
import requests
import json
import dialogflow_v2 as dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:/k/dialogflow/Agent1-61d9da898e91.json"

app = Flask(__name__)
# default route
@app.route('/')
def index():
    return (render_template("index.html"))
# create a route for webhook

	
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text

@app.route('/send_message', methods=['POST'])
def send_message():
    print("inside the print")
    message = request.form['message']
    project_id = str('agent1-9d354')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    print("response_text",response_text)
    return jsonify(response_text)
   
def results():
    # build a request object
    req = request.get_json(force=True)
    # fetch action from json
    action = req.get('queryResult').get('action')
    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}
	
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    result=make_response(jsonify(results()))
    print("result",result)
    return result
	
# run the app
if __name__ == '__main__':
   app.run()