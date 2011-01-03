from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
import httplib


class CheckAvailability(webapp.RequestHandler):
    def get(self, check_or_send):
        availability = self.check_availability()
        body = availability
        if(availability != 'That username has been taken. Please choose another.' or
            check_or_send == 'send'):
            self.send_mail(availability)
            body = availability  + '\nMessage send'

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(body)

    def check_availability(self):
        conn = httplib.HTTPConnection('twitter.com')
        conn.request('GET', '/users/username_available?username=thomie')
        data = conn.getresponse().read()
        return data.split(',')[0].split(':')[1].strip('"')

    def send_mail(self, body):
        message = mail.EmailMessage()
        message.sender = 'thomasmiedema@gmail.com'
        message.to = 'thomasmiedema@gmail.com'
        message.subject = body
        message.body = body
        message.send()

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


application = webapp.WSGIApplication(
                                     [('/', MainPage) ,
                                      (r'/tasks/(.*)', CheckAvailability)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
