#!/usr/bin/env python

import fitparse, time

from dumper import TCXDumper
from fusion import Fusion
from parser import parse_file


cardio_activity = parse_file('data/2014-10-23_18-05-54_4_48.fit')
dumper = TCXDumper()
dumper.dump_to_file(cardio_activity, 'lala_fit.tcx')

def date_to_timestamp(date):
    return int(time.mktime(date.timetuple()))

def report(activity, name):
    timestamp_start = date_to_timestamp(activity.started_at)
    timestamp_end = date_to_timestamp(activity.completed_at)

    print('------------- %s -------------' % name)
    print('Total distance: %d meters' % activity.distance)
    print('Started at: %s (%d)' % (activity.started_at, timestamp_start))
    print('Completed at: %s (%d)\n' % (activity.completed_at, timestamp_end))

main_activity = parse_file('data/main.tcx')
cardio_activity = parse_file('data/cardio.tcx')

# print a few info on the two activities
report(main_activity, 'MAIN')
report(cardio_activity, 'CARDIO')

# start the fusion
fusion = Fusion()
fusion.merge_activities(main_activity, cardio_activity)

# and dump the result
dumper = TCXDumper()
dumper.dump_to_file(main_activity, 'lala')
