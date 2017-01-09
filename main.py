# Copyright 2016 Google Inc.
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

import webapp2

from google.appengine.ext import ndb
from google.appengine.api import search

from six import iteritems

# The same model is used if it is a company or private customer
class CustomerModel(ndb.Model):
    # First and last name are not required if the customer is a company
    first_name = ndb.StringProperty(required=False)
    last_name = ndb.StringProperty(required=False)
 
    # Only filled in if the customer is a company
    company_name = ndb.StringProperty(required=False)
 
    def _post_put_hook(self, future):
        ndb.Model._post_put_hook(self, future)
 
        self.make_customer_search_index()
 
    def make_customer_search_index(self):
 
        customer_fields = list()
 
        if self.first_name:
            customer_fields.append(
                search.TextField(name="first_name", value=self.first_name),
            )
 
        if self.last_name:
            customer_fields.append(
                search.TextField(name="last_name", value=self.last_name),
            )
 
        if self.company_name:
            customer_fields.append(
                search.TextField(name="company_name", value=self.company_name),
            )
 
        index = search.Index(name="customers_test")
        document = search.Document(
            doc_id=self.key.urlsafe(),
            fields=customer_fields
        )
        index.put(document)
 
    @staticmethod
    def list(query):
        sort_company = search.SortExpression(
            expression='company_name',
            direction=search.SortExpression.ASCENDING,
            default_value='ZZZZZZZZZZ')
        sort_surname = search.SortExpression(
            expression='last_name',
            direction=search.SortExpression.ASCENDING,
            default_value="")
        sort_options = search.SortOptions(expressions=[sort_company, sort_surname])
 
        query_options = search.QueryOptions(
            sort_options=sort_options,
            limit=1000
        )
 
        query = search.Query(query_string=query, options=query_options)
 
        index = search.Index(name="customers_test")
        found_documents = index.search(query)
 
        return found_documents
 
 
def insert_test_customers():
    customers_test = [
        {"first_name": "Josep",    "last_name": "Mic", "company_name": "Hollywood"},
        {"first_name": "Jacob Mic",    "last_name": "Moc", "company_name": None},
        {"first_name": "Julia",    "last_name": "Muc", "company_name": "Zync Mic"},
        {"first_name": "Jessy",    "last_name": "Mac", "company_name": "Alphabet Mic"},
        {"first_name": "Julia Mic",    "last_name": "Mac", "company_name": None},
        {"first_name": "Jessy Mic",    "last_name": "Mac", "company_name": "Alphabet Mic"},
    ]
 
    for customer_data in customers_test:
        customer = CustomerModel()
 
        for key, value in iteritems(customer_data):
            setattr(customer, key, value)
 
        customer.put()


class MainPage(webapp2.RequestHandler):
    def get(self):
        list_customers = CustomerModel.list("Mic")
        self.response.write(list_customers)

class Insert(webapp2.RequestHandler):
    def get(self):
        insert_test_customers()
        self.response.write("Insertion Done!")

app = webapp2.WSGIApplication([
    ('/', MainPage),('/insert', Insert),
], debug=True)
