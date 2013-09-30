# -*- coding: utf8 -*-
import re
from datetime import date

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


class MaritechTimeTracking(object):
    def __init__(self):
        self.login_url = settings.maritech_login_url
        self.log_url = settings.maritech_log_url
        self.username = settings.maritech_user
        self.password = settings.maritech_pass
        self.session = None
        self.viewstate = None
        self.event_validation = None

    @wrap_connection_errors
    def login(self):
        self.session = requests.Session()
        try:
            response = self._get(self.login_url)
        except TimeTrackingError:
            self._invalidate_state()
            raise
        data = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.viewstate,
            '__EVENTVALIDATION': self.event_validation,
            'ctl00$ContentPlaceHolderEmpty$edtUsername': self.username,
            'ctl00$ContentPlaceHolderEmpty$edtPassword': self.password,
            'ctl00$ContentPlaceHolderEmpty$Button1': u'Skrá inn',
        }
        try:
            response = self._post(self.login_url, data)
        except TimeTrackingError:
            self._invalidate_state()
            raise
        if response.url == self.login_url:
            self._invalidate_state()
            raise TimeTrackingError('login failed')

    def _validate_state(self):
        if not self.session:
            raise TimeTrackingError('No valid session to to change dates')
        if not self.viewstate:
            raise TimeTrackingError('No valid state to use in requests')
        if not self.event_validation:
            raise TimeTrackingError('No valid state to use in requests')

    def _invalidate_state(self):
        self.session = None
        self.viewstate = None
        self.event_validation = None

    def _update_state(self, response):
        results = re.findall('VIEWSTATE" value="(.*)" />', response.text)
        if not results:
            raise TimeTrackingError("didn't find viewstate")
        self.viewstate = results[0]
        results = re.findall('EVENTVALIDATION" value="(.*)" />', response.text)
        if not results:
            raise TimeTrackingError("didn't find event validation")
        self.event_validation = results[0]

    def _get(self, url):
        response = self.session.get(url)
        if response.status_code != 200:
            raise TimeTrackingError('Get to "%s" failed', url)
        self._update_state(response)
        return response

    def _post(self, url, data):
        response = self.session.post(url, data=data)
        if response.status_code != 200:
            raise TimeTrackingError('Post to "%s" failed', url)
        self._update_state(response)
        return response

    def change_date(self, change_date):
        self._validate_state()
        #don't ask...
        base_date = date(2000, 1, 1)
        diff = change_date - base_date

        #Form data
        data = {
            'ctl00$smMasterWebTime': 'ctl00$ContentPlaceHolderWebTime$' +
                                     'upSaveButton|ctl00$ContentPlaceHolder' +
                                     'WebTime$dgrMinVerk' +
                                     'List$ctl05$btnShowMinVerk',
            'nks_ExpandState': 'ennneennnnnnnennnnen',
            'ctl00_treeLeftLinks_SelectedNode': '',
            'ctl00_treeLeftLinks_PopulateLog': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolderWebTime$Calendar1',
            '__EVENTARGUMENT': str(diff.days),
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.viewstate,
            '__EVENTVALIDATION': self.event_validation,
            'ctl00$ContentPlaceHolderWebTime$txtJobNo': '',
            'ctl00$ContentPlaceHolderWebTime$txtJobDesc': '',
            'ctl00$ContentPlaceHolderWebTime$txtPhase': '',
            'ctl00$ContentPlaceHolderWebTime$txtPhaseDesc': '',
            'ctl00$ContentPlaceHolderWebTime$txtDescription': '',
            'ctl00$ContentPlaceHolderWebTime$txtDescription2': '',
            'ctl00$ContentPlaceHolderWebTime$txtQuantity': '',
            'ctl00$ContentPlaceHolderWebTime$ddlDriveType': '0',
            'ctl00$ContentPlaceHolderWebTime$txtSearchJobNo': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchIncident': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchMyJobs': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim1': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim2': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim3': '',
            'ctl00$ContentPlaceHolderWebTime$txtSearchDim4': '',
        }
        self._post(self.log_url, data)

    @wrap_connection_errors
    def log_hours(self, date, hours, description):
        self._validate_state()
        if date != date.today():
            self.change_date(date)
        time_tracking_job_no = 'VE090054'
        time_tracking_phase = '4100'

        #form data
        data = {
            'ctl00$smMasterWebTime': 'ctl00$ContentPlaceHolderWebTime$' +
                                     'upSaveButton|ctl00$ContentPlaceHolder' +
                                     'WebTime$dgrMinVerk' +
                                     'List$ctl05$btnShowMinVerk',
            'nks_ExpandState': 'ennneennnnnnnennnnen',
            'ctl00_treeLeftLinks_SelectedNode': '',
            'ctl00_treeLeftLinks_PopulateLog': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolderWebTime$dgrMinVerk' +
                             'List$ctl05$btnShowMinVerk',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.viewstate,
            '__EVENTVALIDATION': self.event_validation,
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
        self._post(self.log_url, data)
