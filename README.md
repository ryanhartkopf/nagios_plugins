Nagios Plugins
=====================

check_aws_status_feed
---------------------

Checks http://status.aws.amazon.com/ RSS feeds for outage and performance information.
```
usage: check_aws_status.py [-h] [--region {us-east-1,us-west-1,us-west-2}]
                           {cloudwatch,ec2,elb,rds,route53,vpc,iam,all}

Check current status information from the AWS Service Health Dashboard
(status.aws.amazon.com).

positional arguments:
  {cloudwatch,ec2,elb,rds,route53,vpc,iam,all}

optional arguments:
  -h, --help            show this help message and exit
  --region {us-east-1,us-west-1,us-west-2}
```


check_ldap
----------

```
usage: check_ldap.py [-h] -H SERVER -B BASEDN [-K KEY] [-V VALUE] [-U BINDDN]
                     [-P BINDPW] [-p PORT] [--secure]

Performs a simple LDAP search with filter against a secured or unsecured LDAP
server, and returns OK if any results are returned.

optional arguments:
  -h, --help  show this help message and exit
  -H SERVER   LDAP server on which the query will be run
  -B BASEDN   Base DN for LDAP query
  -K KEY      Filter by a single search key (uid, cn, etc.)
  -V VALUE    Value of the search key ('john', 'sarah', 5011, etc.)
  -U BINDDN   Bind DN for authentication
  -P BINDPW   Bind password for authentication
  -p PORT     Optional port setting
  --secure    Enable secured connection

Usage example: check_ldap -H localhost -B 'dn=example,dn=com' -K 'cn' -V
'john*' -D 'cn=james,o=users,dn=example,dn=com' -P 'passw0rd' -p 8636 --secure
```
