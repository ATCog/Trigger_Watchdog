
//HOST SCRIPT
var PORTVAR='10000';
dmccSet("TELNET.CUSTOM-PORTS",PORTVAR) //add new custom port to allowed list of ports
dmccSet("NETWORK-CLIENT.CLIENT-PORT", PORTVAR); //add new custom port to allowed list of ports
var reqheart='7';
var dimHandler=null; //declare the dimensioning handler to be null, associates no connection for the dimensioner
registerHandler(Callback.onTrigger, onTriggerHandler);
var allout;

function CommHandler(LocalName)
{
	return { // returns an object full of functions
		onConnect: function (peerName) //either as client or server
		{
			// Disable the handler for this connection:
            if(LocalName.indexOf(':'+PORTVAR)>0)// checls to see if the 'dimensioner' is requresting access 
            {
               // this.expectFramed('\x02','\x0D\x0A',500); 
                //checls to make sure the data is formatted correctly, 
                dimHandler=this; //allows only the connection to the diminesioner 
                dimHandler.send('\x02'+reqheart+'\x03'); //send desired heartbeat period
				
                console.warn( peerName+ ' CONNECTED AS CLIENT '+ LocalName+" local name");
				
				this.expectFramed('\x02','\x03',5000); 
                return true; //allow the connection
            }
            else
            {
                return false; //reject or accept connection, default is to reject
            }
			
		},
		onDisconnect: function ()
		{
            if(this==dimHandler)
            {
                console.error("disconnected");//print to log file that no connection
                dimHandler=null; //need to set back to show no longer connected
            }
		},
		onError: function (errorMsg)
		{
		},
		onExpectedData: function (inputString) {
			if(this==dimHandler)
				{
                try{
                    allout=JSON.parse(inputString);
				    //console.log(objout);

                }
                catch(ex){
                    console.error("parsing failed  "+inputString);
                }
				return true;
				}			
		},
		onUnexpectedData: function (inputString) {
			
			return true;
		},
		onTimer: function () { // heatbeat signal
		},
		onEncoder: function () {
		}
	};
    
}
function onTriggerHandler (trigger, state)
    {
        if(state)
        {
            dimHandler.send('\x02'+trigger.index+'\x03');
            console.log(trigger.index);
        }
    }