#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.api import users

import webapp2

# For datastore
import cgi
import urllib
from google.appengine.ext import ndb

class UserId(ndb.Model):
  content = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_user(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)

# ************** MainHandler ************* #
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


# ************** GetUser ************* #
class GetUser(webapp2.RequestHandler):

    def get(self):
        self.response.out.write('<html><body>')
        client_id = self.request.get('client_id')
        ancestor_key = ndb.Key("ID", client_id or "*no_id*")
        userids = UserId.query_user(ancestor_key).fetch(20)
        self.response.out.write('her er eitthvad')
        for userid in userids:
            self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(userid.content))
        # Checks for active Google account session
        # user = users.get_current_user()

        # if user:
        #     self.response.headers['Content-Type'] = 'text/plain'
        #     self.response.write('Hello, ' + user.nickname())
        # else:
        #     self.redirect(users.create_login_url(self.request.uri))
        self.response.out.write('</body></html>')
    def post(self):
        pass

# ************** HasData ************* #
class HasData(webapp2.RequestHandler):
  def get(self):
    pass
    #TODO does user have data

class PostData(webapp2.RequestHandler):
  def post(self):
    client_id = self.request.get('client_id')
    chrome_user = UserId(parent=ndb.Key("ID", client_id or "*no_id*"),
                        content = self.request.get('client_id'))
    chrome_user.put()
    #TODO recieve data from client

class GetSyncData(object):
  """docstring for GetSyncData"""
  def __init__(self, arg):
    super(GetSyncData, self).__init__()
    self.arg = arg

    #implement get data for user
    # property user.email() or user.user_id()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/GetUser/', GetUser),
    ('/HasData/', HasData),
    ('/chrome-sync/command/', PostData),
    ('/GetSyncData/', GetSyncData)
], debug=True)

