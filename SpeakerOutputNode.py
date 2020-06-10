import threading
import falcon
from wsgiref import simple_server
import os

NODE_IDENTITY = "SpeakerOutputNode"

class SpeakFromText:
    
    def __init__(self):
        self.os_name = os.name
    
    def speak_from_text(self, text):
        if self.os_name == 'posix':
            # Using macOS "say" command
            os.system("say "+str(text))
        else:
            print("Speak on this platform not yet supported")



class SpeakerOutputNode(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        speak = SpeakFromText()

        class MainRoute:
            def on_get(self, req ,res):
                res.content_type = 'plain/text'
                res.body = "SpeakerOutputNode<br>/output_text"

        class OutputText:
            def on_get(self, req, res):
                res.content_type = 'plain/text'
                res.body = "You have to POST a message with 'data' field as params"
            def on_post(self, req , res):
                params = req.params
                if 'data' in params:
                    text = params['data']
                    speak.speak_from_text(text)
                    res.content_type = 'plain/text'
                    res.body = 'ok'
                else:
                    res.content_type = 'plain/text'
                    res.body = "ko: you have to pass text data as 'data' field"

        
        api = falcon.API()
        api.add_route('/', MainRoute())
        api.add_route('/output_text', OutputText())
        self.server = simple_server.make_server('', port, app=api)

    def run(self):
        print("[SpeakerOutputNode:INFO] Server started")
        self.server.serve_forever()


if __name__ == '__main__':
    son = SpeakerOutputNode(8005)
    son.start()