import os

from services import TimeTrackingService


port = 8000
static_path = os.path.join(os.path.dirname(__file__), 'static')
favicon_path = os.path.join(static_path, 'img')


time_tracking_login_url = 'your_url'
time_tracking_hours_url = 'your_url'
time_tracking_user = 'user'
time_tracking_pass = 'pass'

try:
    import settings_local
    time_tracking_login_url = settings_local.time_tracking_login_url
    time_tracking_hours_url = settings_local.time_tracking_hours_url
    time_tracking_user = settings_local.time_tracking_user
    time_tracking_pass = settings_local.time_tracking_pass
except ImportError:
    pass

print "Initializing time trackers"
time_trackers = []
all_time_trackers = [
    time_trackers.append(TimeTrackingService(
        time_tracking_login_url,
        time_tracking_hours_url,
        time_tracking_user,
        time_tracking_pass))
]
for time_tracker in time_trackers:
    try:
        time_tracker.login()
        time_trackers.append(time_tracker)
    except:
        #make sure not to halt if services fail to startup
        pass
print "Initialization done"
