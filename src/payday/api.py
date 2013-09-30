import sys
import inspect
from datetime import date
import json

import tornado.web

import settings
from models import WorkLog

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
        all_logs = WorkLog.all()
        self.write(json.dumps(all_logs))


class HoursResource(BaseResource):
    url = r'/api/hours/(\d{4})/(\d{1,2})/(\d{1,2})/?'

    def get(self, year, month, day):
        year, month, day = map(int, (year, month, day))
        logs = WorkLog.get(date(year, month, day))
        if logs:
            self.write(json.dumps(logs))
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
            log = WorkLog.get(id)
            if not log:
                self.set_status(400)
                self.write('400: No log with id %s' % id)
                return
        else:
            log = WorkLog()
        log.date = the_date
        log.hours = hours
        log.description = description
        log.save()
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
        log = WorkLog.get(id)
        log.delete()


def GetRegisteredResources():
    resources = []
    for name, resource in inspect.getmembers(sys.modules[__name__]):
        if name.endswith('Resource') and name != 'BaseResource':
            resources.append((resource.url, resource))
    return resources
