import sys
import inspect
from datetime import date
import json

import tornado.web

import settings
from models import WorkHours

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
    url = r'/api/hours/(\d{4})/(\d{1,2})/(\d{1,2})/?'

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
        the_date = date(year, month, day)
        request_body = json.loads(self.request.body)
        if any(x not in request_body for x in ['hours', 'description']):
            self.set_status(400)
            self.write('400: Required parameter missing')
            return
        id = request_body.get('id', None)
        hours = request_body['hours']
        description = request_body['description']

        if id:
            workhours = WorkHours.get(id)
            if not workhours:
                self.set_status(400)
                self.write('400: No log with id %s' % id)
                return
        else:
            workhours = WorkHours()
        workhours.date = the_date
        workhours.hours = hours
        workhours.description = description
        workhours.save()
        for time_tracker in settings.time_trackers:
            try:
                time_tracker.log_hours(the_date, hours, description)
            except Exception as e:
                print "Unable to sync with time tracking service", e
        if id:
            self.set_status(201)  # created

    def delete(self, year, month, day):
        year, month, day = map(int, (year, month, day))
        the_date = date(year, month, day)
        id = self.get_argument('id')
        workHours = WorkHours.get(id)
        workHours.delete()


def GetRegisteredResources():
    resources = []
    for name, resource in inspect.getmembers(sys.modules[__name__]):
        if name.endswith('Resource') and name != 'BaseResource':
            resources.append((resource.url, resource))
    return resources
