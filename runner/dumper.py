#!/usr/bin/env python

import os

class DumperNotFoundError(RuntimeError):
    pass

class TCXDumper:
    TAB = '  '

    def dump(self, activity):
        buffer = []

        buffer.append('<?xml version="1.0" encoding="UTF-8"?>')
        buffer.append(self._dump_training_database(activity))

        return ''.join(buffer)

    def dump_to_file(self, activity, filename):
        open(filename, 'w').write(self.dump(activity))

    def _dump_training_database(self, activity):
        buffer = []

        buffer.append("""<TrainingCenterDatabase version="1.0"
    xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"
    xmlns:ns5="http://www.garmin.com/xmlschemas/ActivityGoals/v1"
    xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2"
    xmlns:ns2="http://www.garmin.com/xmlschemas/UserProfile/v2"
    xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:ns4="http://www.garmin.com/xmlschemas/ProfileExtension/v1">
""")

        buffer.append(self._dump_activities(activity))
        buffer.append('</TrainingCenterDatabase>')

        return ''.join(buffer)

    def _dump_activities(self, activity):
        buffer = []

        buffer.append(self.TAB + '<Activities>\n')

        buffer.append(self._dump_activity(activity))

        buffer.append(self.TAB + '</Activities>\n')

        return ''.join(buffer)

    def _dump_activity(self, activity):
        buffer = []

        buffer.append(2*self.TAB + '<Activity Sport="%s">\n' % activity.type)
        buffer.append(3*self.TAB + '<Id>%s</Id>\n' % activity.identifier)
        for lap in activity.laps:
            buffer.append(self._dump_lap(lap))
        buffer.append(2*self.TAB + '</Activity>\n')

        return ''.join(buffer)

    def _dump_lap(self, lap):
        buffer = []

        buffer.append(3*self.TAB + '<Lap StartTime="%s">\n' % self._dump_date(lap.start_time))
        buffer.append(4*self.TAB + '<TotalTimeSeconds>%d</TotalTimeSeconds>\n' % lap.duration)
        buffer.append(4*self.TAB + '<DistanceMeters>%d</DistanceMeters>\n' % lap.distance)
        buffer.append(4*self.TAB + '<Calories>%d</Calories>\n' % lap.calories)
        buffer.append(4*self.TAB + '<MaximumSpeed>%f</MaximumSpeed>\n' % lap.max_speed)
        buffer.append(4*self.TAB + '<AverageHeartRateBpm><Value>%d</Value></AverageHeartRateBpm>\n' % lap.avg_heart_rate)
        buffer.append(4*self.TAB + '<MaximumHeartRateBpm><Value>%d</Value></MaximumHeartRateBpm>\n' % lap.max_heart_rate)
        if lap.trigger_method is not None:
            buffer.append(4*self.TAB + '<TriggerMethod>%s</TriggerMethod>\n' % lap.trigger_method)

        buffer.append(4*self.TAB + '<Track>\n')
        for trackpoint in lap.trackpoints:
            buffer.append(self._dump_trackpoint(trackpoint))
        buffer.append(4*self.TAB + '</Track>\n')

        buffer.append(3*self.TAB + '</Lap>\n')

        return ''.join(buffer)

    def _dump_trackpoint(self, trackpoint):
        buffer = []

        buffer.append(5*self.TAB + '<Trackpoint>\n')
        buffer.append(6*self.TAB + '<Time>%s</Time>\n' % self._dump_date(trackpoint.time))
        buffer.append(6*self.TAB + '<DistanceMeters>%d</DistanceMeters>\n' % trackpoint.distance)
        buffer.append(6*self.TAB + '<AltitudeMeters>%d</AltitudeMeters>\n' % trackpoint.altitude)
        buffer.append(6*self.TAB + '<HeartRateBpm><Value>%d</Value></HeartRateBpm>\n' % trackpoint.heart_rate)

        if trackpoint.position is not None:
            buffer.append(self._dump_position(trackpoint.position))

        buffer.append(5*self.TAB + '</Trackpoint>\n')

        return ''.join(buffer)

    def _dump_position(self, position):
        buffer = []

        buffer.append(6*self.TAB + '<Position>\n')
        buffer.append(7*self.TAB + '<LatitudeDegrees>%.16f</LatitudeDegrees>\n' % position.latitude)
        buffer.append(7*self.TAB + '<LongitudeDegrees>%.16f</LongitudeDegrees>\n' % position.longitude)
        buffer.append(6*self.TAB + '</Position>\n')

        return ''.join(buffer)

    def _dump_date(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def dumper_for_file(filename):
    parsers_map = {
        'tcx': TCXDumper
    }

    _, extension = os.path.splitext(filename)
    extension = extension[1:] # remove the leading '.'

    try:
        return parsers_map[extension]()
    except KeyError:
        raise DumperNotFoundError('Not dumper for extension: ' + extension)

def dump_to_file(activity, filename):
    dumper = dumper_for_file(filename)

    return dumper.dump_to_file(activity, filename)
