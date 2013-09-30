import os

from services import MaritechTimeTracking


port = 8000
static_path = os.path.join(os.path.dirname(__file__), 'static')
favicon_path = os.path.join(static_path, 'img')


maritech_login_url = 'your_url'
maritech_log_url = 'your_url'
maritech_user = 'user'
maritech_pass = 'pass'

try:
    import settings_local
    maritech_login_url = settings_local.maritech_login_url
    maritech_log_url = settings_local.maritech_log_url
    maritech_user = settings_local.maritech_user
    maritech_pass = settings_local.maritech_pass
except ImportError:
    pass

print "Initializing time trackers"
time_trackers = []
all_time_trackers = [
    MaritechTimeTracking(),
]
for time_tracker in all_time_trackers:
    try:
        time_tracker.login()
        time_trackers.append(time_tracker)
    except Exception as e:
        #make sure not to halt if services fail to startup
        print "Unable to initialize", time_tracker
        print e
print "Initialization done"
