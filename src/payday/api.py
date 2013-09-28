import sys
import inspect
from datetime import date
import json

import tornado.web

from models import WorkHours
from services import TimeTrackingService

registry = []


class BaseResource(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, *args, **kwargs):
        raise NotImplementedError()


class AllHoursResource(BaseResource):
    url = r'/api/hours/?'

    def get(self):
        all_hours = WorkHours.all()
        self.write(json.dumps(all_hours))


class HoursResource(BaseResource):
    url = r'/api/hours/(\d{4})/(\d{1,2})/(\d{2})/?'

    def get(self, year, month, day):
        year, month, day = map(int, (year, month, day))
        workhours = WorkHours.get(date(year, month, day))
        if workhours:
            self.write(json.dumps(workhours))
        else:
            self.set_status(404)
            self.write('404: not found')

    def post(self, year, month, day):
        year, month, day = map(int, (year, month, day))
        request_body = json.loads(self.request.body)
        hours = request_body['hours']
        description = request_body['description']
        the_date = date(year, month, day)
        workhours = WorkHours.get(the_date)
        if workhours:
            self.set_status(406)  # not acceptable
            self.write('406: date already in use')
        else:
            workhours = WorkHours()
            workhours.date = the_date
            workhours.hours = hours
            workhours.description = description
            workhours.save()
            ttservice = TimeTrackingService()
            try:
                ttservice.login()
                ttservice.log_hours(hours, description)
            except Exception as e:
                print "Unable to sync with time tracking service", e
            self.set_status(201)  # created


def GetRegisteredResources():
    resources = []
    for name, resource in inspect.getmembers(sys.modules[__name__]):
        if name.endswith('Resource') and name != 'BaseResource':
            resources.append((resource.url, resource))
    return resources
