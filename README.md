#Description
Server which accepts HTTP messages from CrossLineDetection app on Axis security cams

##Usage
To test this program run this command:
<code>
telnet localhost 8888
</code>
This wil start a telnet session on the localhost, port 8888. Then copy past the code below, where "CamX" is the name of the camera.
<code>
GET ?Message=Cam1
</code>
This will sent the message a camera will sent when the CrossLineDetection is triggered
