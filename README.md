#Description
Server which accepts HTTP messages from CrossLineDetection app on Axis security cams

##Usage
To test this program run this command:<br>
<code>
telnet localhost 8888
</code><br>
This wil start a telnet session on the localhost, port 8888. <br>
Then copy paste the code below, where "Cam1" is the name of the camera.<br>
<code>
GET ?Message=Cam1
</code><br>
This will sent the message a camera will sent when the CrossLineDetection is triggered
