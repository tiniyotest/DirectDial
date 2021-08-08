from flask import Flask, url_for, request
from tiniyo.voice_response import VoiceResponse
from xmlhelp import tiniyoml
from config import *

app = Flask(__name__)


@app.route('/directdial/', methods=['GET', 'POST'])
def directdial():
    response = VoiceResponse()
    to = request.args.get('ForwardTo', None)
    _from = request.args.get('CLID', None)
    is_sip_user = bool
    print ("SIP Route %s" % request.get_json())
    if request.method == "GET":
        print("SIP Route %s" % request.json)
        if not to:
            to = request.args.get('To', None)
        if _from is None:
            _from = request.args.get('From', '')
    if request.method == "POST":
        app.logger("SIP Route %s" % request.json)
        if not to:
            to = request.form.get('To', None)
        if _from is None:
            _from = request.form.get('From', '')
    #response.say("Please wait! While connecting the call.", voice=female, language=uk)

    if not to:
        print("SIP Route identify destination number")
        response.hangup()
        return tiniyoml(response)
    else:
        if to[:4] == 'sip:':
            is_sip_user = True
        else:
            is_sip_user = False
    if is_sip_user:
        response.dial(number=to, caller_id=_from)
    else:
        response.dial(number=to, caller_id=_from)
    return tiniyoml(response)



if __name__ == '__main__':
    app.run()
