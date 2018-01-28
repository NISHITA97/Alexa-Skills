
'use strict';

const Alexa = require('alexa-sdk');

const APP_ID = 'amzn1.ask.skill.af2e1c29-f58d-40ac-bec8-60bb1553c96f';

var anglesInfo = [
    " Two angles that sum to one full circle (360°) are called explementary angles or conjugate angles. ",
    " An angle equal to half turn (180° or π radians) is called a straight angle. ",
    " A right angle is an angle with a measurement of 90 degrees. Planes (flat surfaces) can also meet at right angles."+
        " In a building, a wall and a floor are said to be perpendicular to each other, and they have a right angle. ",
    " An acute angle (acute meaning sharp) is an angle smaller than a right angle (it is less than 90 degrees). ",
    " An obtuse angle is a form of angle that measures wider than 90° and less than 180°. It is bigger than an acute angle. ",
    "Two angles that sum to one right angle (90°) are called complementary angles.",
    " An angle equal to 1 turn (360° or 2π radians) is called a full angle, complete angle, or a perigon. ",
    " A Reflex Angle is more than 180° but less than 360°. "
];

function ansgi(ang){
    var ans = "";
    if(ang == 0)
        {
            ans = "Zero";
        }
        else if(ang < 90)
        {
            ans = "Acute";
        }
        else if(ang == 90)
        {
           ans = "Right";
        }
        else if(ang<180)
        {
            ans = "Obtuse";
        }
        else if(ang == 180)
        {
            ans = "Straight";
        }
    return ans;
}
const HELP_MESSAGE= 'You can say tell me an angle and i can provide you its information, or, you can say exit... What can I help you with?';
const HELP_REPROMPT='What can I help you with?';
var STOP_MESSAGE= "Goodbye!";

function ansgiexended(ang)
{
    var ans3 = "";
    var ans1 = 0;
    var speech = ang + " degrees is a " +ans3 + " angle. ";
    if(ang<=180)
    {
        ans3 = ansgi(ang);
        speech = ang + " degrees is a " +ans3 + " angle. ";
        //chk = true;
    }
    else if(ang == 360)
    {
        ans3 = "Complete";
        speech = ang + " degrees is a " +ans3 + " angle. ";
    }
    else if(ang < 360)
    {
        ans3 = "Reflex";
        ans1 = 360-ang;
        speech = ang + " degrees is a " +ans3 + " angle whose conjugate is " + ans1 + " degrees. ";
    }
    else{
           var temp = ang;
            var cnt = 0;
            if(temp>=360)
            {
                cnt = temp % 360;
                temp = temp/360;
            }
            temp = Math.floor(temp);
            var ans = ansgi(cnt);
            if(cnt > 180){
                ans = "Reflex";
            }
            var ans11 = "After completing " + temp + " roatations, we come at " + cnt + " degrees which is a "+ ans
            + " angle";
            if(cnt > 180){
             ans11 += " whose conjugate is " + (360-cnt) + " degrees";
            }
            ans11 += ". ";
            speech = ang + " degrees is greater than 360 degrees that is its greater than a complete angle. "+ans11;
    }
    return speech;
}

function comb(num1, num2)
{
    var ans = "";
    var sum = num1 + num2;
    if(sum == 90)
    {
        ans = 'Complementary';
    }
    else if(sum == 180)
    {
        ans = 'Supplementary';
    }
    else if(sum == 360)
    {
        ans = 'Explementary';
    }
    //var speech = "Together they form " + ans + " angles";
    return ans;
}
const handlers = {
    'LaunchRequest': function () {
        this.response.speak("Welcome to Angle Info. We are pleased to help you. Plese tell me the angle about which you"+
        " want information").listen(" Please Repeat. ");
        this.emit(':responseReady');
    },
    'AMAZON.HelpIntent': function () {
        const speechOutput = HELP_MESSAGE;
        const reprompt = HELP_REPROMPT;
        this.emit(':ask', speechOutput, reprompt);
    },
    'AMAZON.CancelIntent': function () {
        this.emit(':tell', 'Goodbye!');
    },
    'AMAZON.StopIntent': function () {
        this.response.speak(STOP_MESSAGE);
        this.emit(':responseReady');
    },
    'EndIntent': function(){
        this.response.speak("Hope we were able to help you!");
         this.emit(':responseReady');
    },
    'AngleInfoIntent': function(){
      var type =    this.event.request.intent.slots.anglename.value;
      var ans2 = " I haven't heard of that angle before. Please try another one. ";
      switch(type){
        case "straight":
              ans2 = anglesInfo[1];
              break;
        case "explementary":
        case "conjugate":
            ans2 = anglesInfo[0];
            break;
        case "complete":
              ans2 = anglesInfo[6];
              break;
        case "right":
            ans2 = anglesInfo[2];
            break;
        case "acute":
              ans2 = anglesInfo[3];
              break;
        case "obtuse":
            ans2 = anglesInfo[4];
            break;
        case "complementary":
              ans2 = anglesInfo[5];
              break;
        case "reflex":
            ans2 = anglesInfo[7];
            
      }
      this.response.speak(ans2);
      this.emit(':responseReady');
    },
    'TellTypeIntent': function () {
        this.attributes.currentAngle = this.event.request.intent.slots.valueone.value;
        var ang = this.attributes.currentAngle;
        var ans="";
        var ans1 = "";
        var chk = false;
        if(ang<=180)
        {
            ans = ansgi(ang);
            chk = true;
        }
        else if(ang == 360)
        {
            chk = true;
            ans = "Complete";
        }
        else if (ang < 360){
            ans = "Reflex";
            ans1 = 360-ang;
        }
      
        if(chk){
            this.response.speak(ang + " degrees is a " + ans + " angle. ");
        }
        else if(ang<360)
        {
            this.response.speak(ang + " degrees is a " + ans + " angle whose conjugate is " + ans1 + " degrees. ");
        }
        else if(ang>360)
        {
            var nor = ang;
            var leftangle1 = 0;
            if(ang>=360)
            {
                leftangle1 = ang % 360;
                nor = ang/360;
            }
            nor = Math.floor(nor);
            if(leftangle1 <= 180){
                ans = ansgi(leftangle1);
            }
            else{
                ans = "reflex";
            }
            ans1 = " After completing " + nor + " roatations, we come at " + leftangle1 + " degrees which is a "+ ans 
            + " angle. ";
            this.response.speak(ang + " degrees is greater than 360 degrees that is its greater than a complete angle. "
            +ans1);
        }
        this.emit(':responseReady');
    },
    'TellTypeIntentII': function(){
        var ang1 = this.event.request.intent.slots.val.value;
        var ang2 = this.event.request.intent.slots.valtwo.value;
        var ans1 = ansgiexended(ang1);
        var ans2;
        if(ang2 == ang1)
        {
            ans2 = " The second angle is same as the first one. ";
        }
        else
        {
            ans2 = ansgiexended(ang2);  
        }
       
        var speech3 = "";
        var red1 = 0;
        var anscomb = comb(ang1%360, ang2%360);
        if(anscomb != '' && anscomb != ""){
            if(ang1 <= 360 && ang2 <= 360 )
            {
                speech3 += " the two angles are ";
            }
            else if(ang1 > 360 && ang2 <= 360)
            {
                red1 = ang1%360;
                speech3 += ang2 + " degrees and ";
                speech3 += red1 + " degrees form ";
            }
            else if(ang1 <= 360 && ang2 > 360)
            {
                red1 = ang2%360;
                speech3 += ang1 + " degrees and ";
                speech3 += red1 + " degrees form ";
            }
            else
            {
                speech3 +=  ang1%360 + " degrees and " + ang2%360 +
                " degrees form ";
            }
            speech3 += anscomb + " angles. ";
        }
        this.response.speak(ans1 + ans2 + speech3);
        this.emit(':responseReady');
    },
     Unhandled() {
    this.emit(':ask',
      'I\'m sorry, but I\'m not sure what you asked me.');
    }
};

exports.handler = function (event, context) {
    const alexa = Alexa.handler(event, context);
    alexa.APP_ID = APP_ID;
    // To enable string internationalization (i18n) features, set a resources object.
    //alexa.resources = languageStrings;
    alexa.registerHandlers(handlers);
    alexa.execute();
};
