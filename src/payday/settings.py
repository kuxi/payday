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

time_trackers = [
    TimeTrackingService(
        time_tracking_login_url,
        time_tracking_hours_url,
        time_tracking_user,
        time_tracking_pass),
]

time_trackers = []
