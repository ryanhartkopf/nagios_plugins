#!/usr/bin/python

import ldap,argparse

parser = argparse.ArgumentParser(description='Performs a simple LDAP search with filter against a secured or unsecured LDAP server, and returns OK if any results are returned.', epilog="Usage example: check_ldap -H localhost -B 'dn=example,dn=com' -K 'cn' -V 'john*' -D 'cn=james,o=users,dn=example,dn=com' -P 'passw0rd' -p 8636 --secure")
parser.add_argument('-H', dest='server', help="LDAP server on which the query will be run", required=True)
parser.add_argument('-B', dest='basedn', help="Base DN for LDAP query", required=True)
parser.add_argument('-K', dest='key', help="Filter by a single search key (uid, cn, etc.)")
parser.add_argument('-V', dest='value', help="Value of the search key ('john', 'sarah', 5011, etc.)")
parser.add_argument('-U', dest='binddn', help="Bind DN for authentication")
parser.add_argument('-P', dest='bindpw', help="Bind password for authentication")
parser.add_argument('-p', dest='port', help="Optional port setting")
parser.add_argument('--secure', dest='secure', help="Enable secured connection", action="store_true")
args = parser.parse_args()

print args.secure

if args.secure == True:
  full_server = 'ldaps://' + args.server
else:
  full_server = 'ldap://' + args.server
if args.port:
  full_server += ':' + args.port

l = ldap.initialize(full_server)

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
  exit()
else:
  print "CRITICAL: Search failed!"
  exit(2)
