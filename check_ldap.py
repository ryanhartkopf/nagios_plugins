#!/usr/bin/env python

# Copyright 2014 AppliedTrust / Ryan Hartkopf
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ldap,argparse,sys

parser = argparse.ArgumentParser(description='Performs a simple LDAP search with filter against a secured or unsecured LDAP server, and returns OK if any results are returned.', epilog="Usage example: check_ldap -H localhost -B 'dn=example,dn=com' -K 'cn' -V 'john*' -U 'cn=james,o=users,dn=example,dn=com' -P 'passw0rd' -p 8636 --secure")
parser.add_argument('-H', dest='server', help="LDAP server on which the query will be run", required=True)
parser.add_argument('-B', dest='basedn', help="Base DN for LDAP query", required=True)
parser.add_argument('-K', dest='key', help="Filter by a single search key (uid, cn, etc.)", required=True)
parser.add_argument('-V', dest='value', help="Value of the search key ('john', 'sarah', 5011, etc.)", required=True)
parser.add_argument('-U', dest='binddn', help="Bind DN for authentication")
parser.add_argument('-P', dest='bindpw', help="Bind password for authentication")
parser.add_argument('-p', dest='port', help="Optional port setting")
parser.add_argument('--secure', dest='secure', help="Enable secured connection", action="store_true")
args = parser.parse_args()

if args.secure == True:
  full_server = 'ldaps://' + args.server
else:
  full_server = 'ldap://' + args.server
if args.port:
  full_server += ':' + args.port

l = ldap.initialize(full_server)
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

if args.binddn and args.bindpw:
  l.simple_bind_s( args.binddn, args.bindpw )
else:
  l.simple_bind_s()

filter = '(' + args.key + '=' + args.value + ')'
ret = [args.key]
results = l.search_s(args.basedn,ldap.SCOPE_SUBTREE,filter,ret)

if results:
  print "OK: Search for object " + args.value + " was successful!"
  print results
  sys.exit(0)
else:
  print "CRITICAL: Search failed!"
  sys.exit(2)
