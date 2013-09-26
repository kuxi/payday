# -*- coding: utf8 -*-
import re

import requests

import settings


class TimeTrackingService(object):
    def __init__(self):
        self.session = None

    def login(self):
        self.session = requests.Session()
        response = self.session.get(settings.time_tracking_login_url)
        if response.status_code != 200:
            #TODO: error handling
            print 'Unable to get time_tracking_login_url'
            self.session = None
            return
        results = re.findall('VIEWSTATE" value="(.*)" />', response.text)
        if not results:
            #TODO: error handling
            print "didn't find event viewstate"
            return
        viewstate = results[0]
        results = re.findall('EVENTVALIDATION" value="(.*)" />', response.text)
        if not results:
            #TODO: error handling
            print "didn't find event validation"
            return
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
        response = self.session.post(
            settings.time_tracking_login_url, data=data)
        if response.status_code != 200 or response.url == settings.time_tracking_login_url:
            #TODO: error handling
            print 'login failed'
            self.session = None
            return

    def log_hours(self, hours, description):
        if not self.session:
            #TODO: error handling
            print 'No valid session to log hours'
            return
        time_tracking_job_no = 'VE090054'
        time_tracking_phase = '4100'

        response = self.session.get(settings.time_tracking_hours_url)
        if response.status_code != 200:
            #TODO: error handling
            print 'failed to retrieve time_tracking_hours url'
            return
        results = re.findall('VIEWSTATE" value="(.*)" />', response.text)
        if not results:
            #TODO: error handling
            print "didn't find viewstate"
            return
        viewstate = results[0]
        results = re.findall('EVENTVALIDATION" value="(.*)" />', response.text)
        if not results:
            #TODO: error handling
            print "didn't find eventvalidation"
            return
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
            print 'posting hours failed'
