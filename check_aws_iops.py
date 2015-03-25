#!/usr/bin/env python2.7

"""Check AWS IOPS for Nagios/Icinga.

Usage:
  check_aws_iops.py <accesskey> <secretkey> <volume_id> [<aws_region>]

"""

from docopt import docopt
import boto.ec2.cloudwatch
from datetime import datetime,timedelta

debug = 0 # Set to 1 for additional output

def main(docopt_args):

  # Set variables from command line args
  if docopt_args['<aws_region>']:
    region = docopt_args['<aws_region>']
  else:
    region = 'us-east-1'
  key = docopt_args['<accesskey>']
  secret = docopt_args['<secretkey>']
  volume_id = docopt_args['<volume_id>']

  # Initialize connection to CloudWatch
  c = boto.ec2.cloudwatch.connect_to_region(region,
  aws_access_key_id=key,
  aws_secret_access_key=secret,)
  
  # Set required attributes
  metrics = ['VolumeReadBytes', 'VolumeWriteBytes','VolumeReadOps', 'VolumeWriteOps']
  namespace = 'AWS/EBS'
  statistics = ['Minimum', 'Maximum', 'Average', 'Sum']
  period = 3600
  now = datetime.utcnow()
  start_time = now - timedelta(minutes=60)
  dimensions = {'VolumeId': [volume_id]}
  perf_output = '|';
  
  if debug == 1:
    print "==== Variables ===="
    print "Period: " + str(period)
    print "Start time: " + str(start_time)
    print "End time: " + str(now)
    print "Metrics: " + str(metrics)
    print "Namespace: " + namespace
    print "Dimensions: " + str(dimensions)
    print key
    print secret
    print
    print "==== Output ===="
  # Check metrics and return warning if output is blank
  for metric_name in metrics:
     metric_output = c.get_metric_statistics(period, start_time, now, metric_name, namespace, statistics, dimensions)
     if debug == 1:
       print metric_output
     if metric_output:
       perf_output += metric_name + '=' + str(round(metric_output[0]['Average'])) + ';;;'

  if perf_output == '|':
    print 'WARNING: volume id "' + volume_id + '" or region "' + region + '" is incorrect'
    exit(1)

  if debug == 1:
    print
  print 'AWS IOPS OK for volume ' + volume_id + perf_output

if __name__ == '__main__':
  args = docopt(__doc__)
  main(args)
