#!/usr/bin/env python

import operator, re
from datetime import timedelta

class TimeEditor:
    TIME_REGEX = r'(?P<sign>(\+|\-)?)((?P<hours>\d+?)hour)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?'

    @classmethod
    def configure_args_parser(cls, parser):
        parser.add_argument(
            '-t', '--time', type=str, required=True,
            help='Amount of time to add/substract',
        )
        parser.set_defaults(editor=lambda: TimeEditor())

    def edit(self, activity, options):
        operator, delta = self._parse_time_delta(options.time)

        for lap in activity.laps:
            lap.start_time = operator(lap.start_time, delta)

            for trackpoint in lap.trackpoints:
                trackpoint.time = operator(trackpoint.time, delta)

    def _parse_time_delta(self, string):
        regex = re.compile(TimeEditor.TIME_REGEX)
        parts = regex.match(string)

        if not parts:
            raise RuntimeError('Invalid time delta given: ' + string)

        parts = parts.groupdict()
        sign = operator.sub if parts['sign'] == '-' else operator.add
        del parts['sign']

        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)

        return sign, timedelta(**time_params)
