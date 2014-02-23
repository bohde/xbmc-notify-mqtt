XBMC Notify MQTT
=============================

An XBMC addon to display notifications received over mqtt.

Install
-------

Install the zip file through the XBMC add on interface.

Configure
---------

Insert the broker host, port, and the root path on in the configuration.

Topics
------

The root topic is configurable, but defaults to "/house/xbmc".

Status will be published to the root + "/status".

The service will display notifications published to root + "/all/messages".

Play status is published under the topic root + "player/status". It will be json string of with at least a state attribute, with optional type, current, and total time attributes.


Usage
-----

Publish a JSON message to the notification topic with title, text, duration (in seconds), and optional image attributes.

An example `{"title":"Here's a message", "text":"Here's the body", "image":"http://example.com/image.png, "duration":10}`
