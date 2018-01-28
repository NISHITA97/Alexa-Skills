{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang16393{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\colortbl ;\red0\green0\blue255;}
{\*\generator Riched20 10.0.16299}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\f0\fs22\lang9 """\par
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.\par
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well\par
as testing instructions are located at {{\field{\*\fldinst{HYPERLINK http://amzn.to/1LzFrj6 }}{\fldrslt{http://amzn.to/1LzFrj6\ul0\cf0}}}}\f0\fs22\par
\par
For additional samples, visit the Alexa Skills Kit Getting Started guide at\par
{{\field{\*\fldinst{HYPERLINK http://amzn.to/1LGWsLG }}{\fldrslt{http://amzn.to/1LGWsLG\ul0\cf0}}}}\f0\fs22\par
"""\par
\par
from __future__ import print_function\par
import urllib2\par
from json import load\par
\par
# --------------- Helpers that build all of the responses ----------------------\par
\par
def build_speechlet_response(title, output, reprompt_text, should_end_session):\par
    return \{\par
        'outputSpeech': \{\par
            'type': 'PlainText',\par
            'text': output\par
        \},\par
        'card': \{\par
            'type': 'Simple',\par
            'title': title,\par
            'content': output\par
        \},\par
        'reprompt': \{\par
            'outputSpeech': \{\par
                'type': 'PlainText',\par
                'text': reprompt_text\par
            \}\par
        \},\par
        'shouldEndSession': should_end_session\par
    \}\par
\par
\par
def build_response(session_attributes, speechlet_response):\par
    return \{\par
        'version': '1.0',\par
        'sessionAttributes': session_attributes,\par
        'response': speechlet_response\par
    \}\par
\par
\par
# --------------- Functions that control the skill's behavior ------------------\par
\par
def get_welcome_response():\par
    """ If we wanted to initialize the session to have some attributes we could\par
    add those here\par
    """\par
\par
    session_attributes = \{\}\par
    card_title = "Welcome"\par
    speech_output = "Welcome to Fuel Info. " \\\par
                    "Please tell me about the fuel and state for which you would like to know prices by saying, " \\\par
                    "Tell me about prices of fuel name in state"\par
    # If the user either does not reply to the welcome message or says something\par
    # that is not understood, they will be prompted again with this text.\par
    reprompt_text = "Please tell me about the fuel and state for which you would like to know prices by saying, " \\\par
                    "Tell me about prices of fuel name in state"\par
    should_end_session = False\par
    return build_response(session_attributes, build_speechlet_response(\par
        card_title, speech_output, reprompt_text, should_end_session))\par
\par
\par
def handle_session_end_request():\par
    card_title = "Session Ended"\par
    speech_output = "Thank you for trying Fuel Info. " \\\par
                    "Have a nice day! "\par
    # Setting this to true ends the session and exits the skill.\par
    should_end_session = True\par
    return build_response(\{\}, build_speechlet_response(\par
        card_title, speech_output, None, should_end_session))\par
\par
\par
\par
\par
def fuel_Info_Intent_handler(intent, session):\par
    card_title = "fuel intent"\par
    session_attributes = \{\}\par
    should_end_session = True\par
    reprompt_text = None\par
    \par
    speech_output = ""\par
    citychk=True\par
    fuelchk=True\par
    if 'city' in intent['slots']:\par
        try:\par
            city = intent['slots']['city']['value']\par
        except Exception:\par
            speech_output="You missed city name"\par
            citychk=False\par
    else:\par
        citychk=False\par
    if 'fuelname' in intent['slots']:\par
        try:\par
            fuelname = intent['slots']['fuelname']['value']\par
        except Exception:\par
            if(citychk):\par
                speech_output= "You missed fuel name"\par
            else:\par
                speech_output+= " and fuel name"\par
            fuelchk=False\par
    else:\par
        fuelchk=False\par
\par
    if(citychk and fuelchk):\par
        base='http://fuelpriceindia.herokuapp.com'\par
        par='/price?city='+city+'&fuel_type='+fuelname\par
        success=True\par
        try: \par
            response = urllib2.urlopen(base+par)\par
        except urllib2.HTTPError, e:\par
            #print str(e.code)\par
            if(str(e.code)=='400'):\par
                speech_output="Data for either of the provided fuel name or state is not available at the momment"\par
            success=False\par
        except urllib2.URLError, e:\par
            print (str(e.reason))\par
            success=False\par
        except httplib.HTTPException, e:\par
            print (HTTPException)\par
            success=False\par
        except Exception:\par
            success=False\par
            import traceback\par
            print (traceback.format_exc())\par
        if(success):\par
            json_obj = load(response)\par
            price = str(json_obj[fuelname])\par
            speech_output="The price of " + fuelname +" in "+ city + " is "+ price+" "\par
        elif(speech_output==""):\par
            speech_output="Something went wrong"\par
    elif(speech_output==""):\par
        speech_output="unindientified input"\par
    \par
    return build_response(session_attributes, build_speechlet_response(\par
        card_title, speech_output, reprompt_text, should_end_session))\par
\par
\par
# --------------- Events ------------------\par
\par
def on_session_started(session_started_request, session):\par
    """ Called when the session starts """\par
\par
    print("on_session_started requestId=" + session_started_request['requestId']\par
          + ", sessionId=" + session['sessionId'])\par
\par
\par
def on_launch(launch_request, session):\par
    """ Called when the user launches the skill without specifying what they\par
    want\par
    """\par
\par
    print("on_launch requestId=" + launch_request['requestId'] +\par
          ", sessionId=" + session['sessionId'])\par
    # Dispatch to your skill's launch\par
    return get_welcome_response()\par
\par
\par
def on_intent(intent_request, session):\par
    """ Called when the user specifies an intent for this skill """\par
\par
    print("on_intent requestId=" + intent_request['requestId'] +\par
          ", sessionId=" + session['sessionId'])\par
\par
    intent = intent_request['intent']\par
    intent_name = intent_request['intent']['name']\par
\par
    # Dispatch to your skill's intent handlers\par
    if intent_name == "fuelInfo":\par
        return fuel_Info_Intent_handler(intent, session)\par
    elif intent_name == "AMAZON.HelpIntent":\par
        return get_welcome_response()\par
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":\par
        return handle_session_end_request()\par
    else:\par
        raise ValueError("Invalid intent")\par
\par
\par
def on_session_ended(session_ended_request, session):\par
    """ Called when the user ends the session.\par
\par
    Is not called when the skill returns should_end_session=true\par
    """\par
    print("on_session_ended requestId=" + session_ended_request['requestId'] +\par
          ", sessionId=" + session['sessionId'])\par
    # add cleanup logic here\par
\par
\par
# --------------- Main handler ------------------\par
\par
def lambda_handler(event, context):\par
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,\par
    etc.) The JSON body of the request is provided in the event parameter.\par
    """\par
    print("event.session.application.applicationId=" +\par
          event['session']['application']['applicationId'])\par
\par
    """\par
    Uncomment this if statement and populate with your skill's application ID to\par
    prevent someone else from configuring a skill that sends requests to this\par
    function.\par
    """\par
    # if (event['session']['application']['applicationId'] !=\par
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):\par
    #     raise ValueError("Invalid Application ID")\par
\par
    if event['session']['new']:\par
        on_session_started(\{'requestId': event['request']['requestId']\},\par
                           event['session'])\par
\par
    if event['request']['type'] == "LaunchRequest":\par
        return on_launch(event['request'], event['session'])\par
    elif event['request']['type'] == "IntentRequest":\par
        return on_intent(event['request'], event['session'])\par
    elif event['request']['type'] == "SessionEndedRequest":\par
        return on_session_ended(event['request'], event['session'])\par
}
 