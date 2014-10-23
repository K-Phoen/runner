#!/usr/bin/env python

from datetime import datetime

class Activity:
    def __init__(self, identifier = None):
        self.identifier = identifier
        self.laps = []
        self._type = None

    @property
    def started_at(self):
        return min(lap.start_time for lap in self.laps)

    @property
    def completed_at(self):
        return max(lap.end_time for lap in self.laps)

    @property
    def total_time(self):
        return sum(lap.total_time for lap in self.laps)

    @property
    def calories(self):
        return sum(lap.calories for lap in self.laps)

    @property
    def distance(self):
        return sum(lap.distance for lap in self.laps)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value.title()

    @property
    def trackpoints(self):
        for lap in self.laps:
            for trackpoint in lap.trackpoints:
                yield trackpoint

    def __repr__(self):
        return '<Activity: id "%s" of type "%s" (%d laps)>' % (
            self.identifier,
            self.type,
            len(self.laps)
        )

class Lap:
    def __init__(self, start_time = None):
        self.start_time = start_time if type(start_time) is datetime else datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.trackpoints = []

        self.duration = 0 # in seconds
        self.distance = 0 # in meters
        self.calories = 0
        self.max_speed = 0 # in meters per second
        self.trigger_method = None

        self._avg_heart_rate = 0 # in bpm
        self._max_heart_rate = 0 # in bpm

    @property
    def max_heart_rate(self):
        return self._max_heart_rate if self._max_heart_rate is not 0 else \
               max(trackpoint.heart_rate for trackpoint in self.trackpoints)

    @max_heart_rate.setter
    def max_heart_rate(self, value):
        self._max_heart_rate = value

    @property
    def avg_heart_rate(self):
        return self._avg_heart_rate if self._avg_heart_rate is not 0 else \
               sum(trackpoint.heart_rate for trackpoint in self.trackpoints) / float(len(self.trackpoints))

    @avg_heart_rate.setter
    def avg_heart_rate(self, value):
        self._avg_heart_rate = value

    @property
    def end_time(self):
        return max(trackpoint.time for trackpoint in self.trackpoints)

    def __repr__(self):
        return '<Lap: started at %s; duration %d sec; %d meters>' % (
            self.start_time,
            self.duration,
            self.distance
        )

class Trackpoint:
    def __init__(self, time = None):
        self.time = time if type(time) is datetime else datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.distance = 0 # in meters
        self.altitude = 0 # in meters
        self.heart_rate = 0 # in bpm
        self.position = None

    def __repr__(self):
        return '<Trackpoint: %s; distance %d; heart rate %d>' % (
            self.time,
            self.distance,
            self.heart_rate
        )

class Position:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Position: lat = %f ; long = %f>' % (
            self.latitude,
            self.longitude
        )
