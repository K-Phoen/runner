#!/usr/bin/env python

import operator, re
from datetime import datetime, timedelta

class EditorNotFoundError(RuntimeError):
    pass

class TimeEditor:
    @classmethod
    def configure_args_parser(cls, parser):
        parser.add_argument(
            '-t', '--time', type=str, required=True,
            help='Amount of time to add/substract',
        )
        parser.set_defaults(editor=lambda: TimeEditor())

    def edit(self, activity, options):
        op, delta = self._parse_time_delta(options.time)

        for lap in activity.laps:
            lap.start_time = op(lap.start_time, delta)

            for trackpoint in lap.trackpoints:
                trackpoint.time = op(trackpoint.time, delta)

    def _parse_time_delta(self, string):
        regex = re.compile(r'(?P<sign>(\+|\-)?)((?P<hours>\d+?)hour)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        parts = regex.match(string)

        if not parts:
            raise RuntimeError('Invalid time delta given: ' + string)

        parts = parts.groupdict()
        sign = operator.sub if parts['sign'] == '-' else operator.add
        del parts['sign']

        #time_params = {name: int(param) for (name, param) in parts.items() if param}
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)

        return sign, timedelta(**time_params)
