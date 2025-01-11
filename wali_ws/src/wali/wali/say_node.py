#!/usr/bin/env python3

# FILE: say_node.py


#    Uses espeak-ng TTS to speak string phrases sent to /say service request

#    wali_interfaces.srv.Say.srv
#        string saystring
#        ---
#        bool spoken

#    CLI:   ros2 service call /say wali_interfaces/srv/Say "saystring: 'hello'"


from wali_interfaces.srv import Say

import rclpy
from rclpy.node import Node
import sys
import logging
import wave
import os
# from piper.voice import PiperVoice

import subprocess


class SayService(Node):

    def __init__(self):
        super().__init__('say')
        self.srv = self.create_service(Say, 'say', self.say_cb)
        # create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.loghandler = logging.FileHandler('/home/ubuntu/TB5-WaLI/logs/say.log')

        logformatter = logging.Formatter('%(asctime)s|%(message)s',"%Y-%m-%d %H:%M")
        self.loghandler.setFormatter(logformatter)
        self.logger.addHandler(self.loghandler)





    def say_cb(self, request, response):
        text = request.saystring
        vol = 50
        self.get_logger().info('Say request:"{}"'.format(text))
        subprocess.check_output(['espeak-ng -s150 -a'+str(vol)+' "%s"' % text], stderr=subprocess.STDOUT, shell=True)
        response.spoken = True
        self.logger.info(text + " - spoken: " + str(response.spoken) )

        return response


def main():
    rclpy.init()

    say_svc = SayService()

    try:
        rclpy.spin(say_svc)
    except KeyboardInterrupt:
        pass



if __name__ == '__main__':
    main()




