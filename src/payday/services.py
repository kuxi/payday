# -*- coding: utf8 -*-
import re

import requests

import settings


class TimeTrackingError(requests.ConnectionError):
    pass


def wrap_connection_errors(func):
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as e:
            raise TimeTrackingError(e)
    return decorated


class TimeTrackingService(object):
    def __init__(self):
        self.session = None

    @wrap_connection_errors
    def login(self):
        session = requests.Session()
        response = session.get(settings.time_tracking_login_url)
        if response.status_code != 200:
            raise TimeTrackingError('Unable to get time_tracking_login_url')
        results = re.findall('VIEWSTATE" value="(.*)" />', response.text)
        if not results:
            raise TimeTrackingError("didn't find event viewstate")
        viewstate = results[0]
        results = re.findall('EVENTVALIDATION" value="(.*)" />', response.text)
        if not results:
            raise TimeTrackingError("didn't find event validation")
        event_validation = results[0]
        data = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': event_validation,
            'ctl00$ContentPlaceHolderEmpty$edtUsername': settings.time_tracking_user,
            'ctl00$ContentPlaceHolderEmpty$edtPassword': settings.time_tracking_pass,
            'ctl00$ContentPlaceHolderEmpty$Button1': u'Skrá inn',
        }
        response = session.post(
            settings.time_tracking_login_url, data=data)
        if response.status_code != 200 or response.url == settings.time_tracking_login_url:
            raise TimeTrackingError('login failed')
        self.session = session

    @wrap_connection_errors
    def log_hours(self, hours, description):
        if not self.session:
            raise TimeTrackingError('No valid session to log hours')
        time_tracking_job_no = 'VE090054'
        time_tracking_phase = '4100'

        response = self.session.get(settings.time_tracking_hours_url)
        if response.status_code != 200:
            raise TimeTrackingError('failed to retrieve time_tracking_hours url')
        results = re.findall('VIEWSTATE" value="(.*)" />', response.text)
        if not results:
            raise TimeTrackingError("didn't find viewstate")
        viewstate = results[0]
        results = re.findall('EVENTVALIDATION" value="(.*)" />', response.text)
        if not results:
            raise TimeTrackingError("didn't find eventvalidation")
        event_validation = results[0]
        data = {
            'ctl00$smMasterWebTime': 'ctl00$ContentPlaceHolderWebTime$' +
                                     'upSaveButton|ctl00$ContentPlaceHolder' +
                                     'WebTime$dgrMinVerk' +
                                     'List$ctl05$btnShowMinVerk',
            'nks_ExpandState': 'ennneennnnnnnennnnen',
            'ctl00_treeLeftLinks_SelectedNode': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolderWebTime$dgrMinVerk' +
                             'List$ctl05$btnShowMinVerk',
            '__EVENTARGUMENT': '',
            'ctl00_treeLeftLinks_PopulateLog': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': event_validation,
            'ctl00$ContentPlaceHolderWebTime$txtJobNo': time_tracking_job_no,
            'ctl00$ContentPlaceHolderWebTime$txtJobDesc': '',
            'ctl00$ContentPlaceHolderWebTime$txtPhase': time_tracking_phase,
            'ctl00$ContentPlaceHolderWebTime$txtPhaseDesc': '',
            'ctl00$ContentPlaceHolderWebTime$txtDescription': description,
            'ctl00$ContentPlaceHolderWebTime$txtDescription2': '',
            'ctl00$ContentPlaceHolderWebTime$txtQuantity': str(hours),
            'ctl00$ContentPlaceHolderWebTime$ddlDriveType': '0',
            'ctl00$ContentPlaceHolderWebTime$btnSave': 'Vista',
            'ctl00$ContentPlaceHolderWebTime$txtSearchJobNo': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchIncident': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchMyJobs': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim1': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim2': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim3': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim4': '',
        }
        response = self.session.post(
            settings.time_tracking_hours_url, data=data)
        if response.status_code != 200:
            raise TimeTrackingError('posting hours failed')
