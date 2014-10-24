#!/usr/bin/env python

import pandas, time, math

class Fusion:
    def merge_activities(self, main_activity, cardio_activity):
        complete_cardio = self._interpolate_cardio(main_activity, cardio_activity)

        # and merge it back into the main activity
        for trackpoint in main_activity.trackpoints:
            timestamp = self._date_to_timestamp(trackpoint.time)

            try:
                bpm = float(complete_cardio[timestamp])
                bpm = 0 if math.isnan(bpm) else int(bpm)
            except KeyError:
                bpm = 0

            trackpoint.heart_rate = bpm

    def _interpolate_cardio(self, main_activity, cardio_activity):
        # determine the workout bounds
        main_start = self._date_to_timestamp(main_activity.started_at)
        main_end = self._date_to_timestamp(main_activity.completed_at)

        # interpolate the cardio data
        cardio_map = {self._date_to_timestamp(t.time): t.heart_rate for t in cardio_activity.trackpoints}
        cardio_map_interpolated = pandas.Series(cardio_map, index=range(main_start, main_end + 1))
        cardio_map_interpolated = cardio_map_interpolated.interpolate()

        return cardio_map_interpolated.to_dict()

    def _date_to_timestamp(self, date):
        return int(time.mktime(date.timetuple()))
