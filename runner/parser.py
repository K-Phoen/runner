#!/usr/bin/env python

import fitparse, os
from lxml import objectify

import runner.model as model

class ParserNotFoundError(RuntimeError):
    pass

class GPXParser:
    def parse(self, gpx_file):
        tree = objectify.parse(gpx_file)
        root = tree.getroot()

        return self._parse_activity(root)

    def _parse_activity(self, activity_xml):
        activity = model.Activity()

        for track in activity_xml.trk:
            activity.laps.append(self._parse_track(track))

        return activity

    def _parse_track(self, track_xml):
        track = model.Lap()

        for segment in track_xml.trkseg:
            for trackpoint in segment.trkpt:
                track.trackpoints.append(self._parse_trackpoint(trackpoint))

        track.duration = (track.end_time - track.start_time).total_seconds()

        return track

    def _parse_trackpoint(self, trackpoint_xml):
        trackpoint = model.Trackpoint(trackpoint_xml.time.pyval)

        trackpoint.altitude = self._get_or_else(trackpoint_xml, 'ele', 0)

        if trackpoint_xml.get('lat') is not None and trackpoint_xml.get('lon') is not None:
            trackpoint.position = model.Position(
                float(trackpoint_xml.get('lat')),
                float(trackpoint_xml.get('lon'))
            )

        return trackpoint

    def _get_or_else(self, node, key, default = None):
        try:
            return node[key].pyval
        except AttributeError:
            return default

class TCXParser:
    def parse(self, tcx_file):
        tree = objectify.parse(tcx_file)
        root = tree.getroot()

        return self._parse_activity(root.Activities.Activity)

    def _parse_activity(self, activity_xml):
        #activity = model.Activity(activity_xml.Id.pyval)
        activity = model.Activity()

        # try to retrieve the activity type
        activity.type = activity_xml.get('Sport')

        for lap in activity_xml.Lap:
            activity.laps.append(self._parse_lap(lap))

        return activity

    def _parse_lap(self, lap_xml):
        lap = model.Lap(lap_xml.get('StartTime'))

        lap.duration       = self._get_or_else(lap_xml, 'TotalTimeSeconds', 0) # in seconds
        lap.distance       = self._get_or_else(lap_xml, 'DistanceMeters', 0)  # in meters
        lap.calories       = self._get_or_else(lap_xml, 'Calories', 0)
        lap.max_speed      = self._get_or_else(lap_xml, 'MaximumSpeed', 0) # in meters per second
        lap.trigger_method = self._get_or_else(lap_xml, 'TriggerMethod', None)

        lap.avg_heart_rate = self._parse_heart_rate_bpm(lap_xml, 'AverageHeartRateBpm')
        lap.max_heart_rate = self._parse_heart_rate_bpm(lap_xml, 'MaximumHeartRateBpm')

        for trackpoint in lap_xml.Track.Trackpoint:
            lap.trackpoints.append(self._parse_trackpoint(trackpoint))

        return lap

    def _parse_trackpoint(self, trackpoint_xml):
        trackpoint = model.Trackpoint(trackpoint_xml.Time.pyval)

        trackpoint.distance   = self._get_or_else(trackpoint_xml, 'DistanceMeters', 0)
        trackpoint.altitude   = self._get_or_else(trackpoint_xml, 'AltitudeMeters', 0)
        trackpoint.heart_rate = self._parse_heart_rate_bpm(trackpoint_xml, 'HeartRateBpm')

        try:
            trackpoint.position = self._parse_position(trackpoint_xml.Position)
        except AttributeError:
            pass

        return trackpoint

    def _parse_position(self, position_xml):
        return model.Position(
            self._get_or_else(position_xml, 'LatitudeDegrees', 0),
            self._get_or_else(position_xml, 'LongitudeDegrees', 0)
        )

    def _parse_heart_rate_bpm(self, node, key, default = 0):
        try:
            return node[key].Value.pyval
        except AttributeError:
            return default

    def _get_or_else(self, node, key, default = None):
        try:
            return node[key].pyval
        except AttributeError:
            return default

class FITParser:
    def parse(self, fit_file):
        fitfile = fitparse.FitFile(
            fit_file,
            data_processor=fitparse.StandardUnitsDataProcessor(),
        )
        activity = model.Activity()
        data = {}

        for message in fitfile.get_messages():
            self._handle_message(message, activity, data)

        return activity

    def _handle_message(self, message, activity, data):
        if message.name == 'activity':
            data['trigger_method'] = message.get('type').value
        elif message.name == 'lap':
            self._handle_lap(message, activity, data)
        elif message.name == 'record':
            self._handle_record(message, activity, data)

    def _handle_lap(self, message, activity, data):
        lap = model.Lap(message.get('start_time').value)

        lap.trigger_method = data['trigger_method']
        lap.duration = int(self._get_or_else(message, 'total_elapsed_time', 0))
        lap.distance = int(self._get_or_else(message, 'total_distance', 0))
        lap.calories = int(self._get_or_else(message, 'total_calories', 0))
        lap.max_speed = float(self._get_or_else(message, 'max_speed', 0))
        lap.avg_heart_rate = int(self._get_or_else(message, 'avg_heart_rate', 0))
        lap.max_heart_rate = int(self._get_or_else(message, 'max_heart_rate', 0))

        activity.type = message.get('sport').value
        activity.laps.append(lap)

    def _handle_record(self, message, activity, data):
        trackpoint = model.Trackpoint(message.get('timestamp').value)

        trackpoint.heart_rate = int(self._get_or_else(message, 'heart_rate', 0))

        activity.laps[-1].trackpoints.append(trackpoint)

    def _get_or_else(self, message, key, default=None):
        value = message.get(key)

        return value.value if value is not None and value.value is not None else default

def parser_for_file(filename):
    parsers_map = {
        'fit': FITParser,
        'gpx': GPXParser,
        'tcx': TCXParser
    }

    _, extension = os.path.splitext(filename)
    extension = extension[1:] # remove the leading '.'

    try:
        return parsers_map[extension]()
    except KeyError:
        raise ParserNotFoundError('Not parser for extension: ' + extension)

def parse_from_file(filename):
    parser = parser_for_file(filename)

    return parser.parse(filename)
