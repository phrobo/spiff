#!/usr/bin/env python
from spiff import cli
import logging
import yaml
from getpass import getpass

parser = cli.argparser()
parser.add_argument('file', default=None)

api, args = cli.api_from_argv(parser=parser)
print api

structure = yaml.load(open(args.file, 'r'))

for username, user in structure['users'].iteritems():
  u = api.getList('user', username=username)[0]
  for attrName, attrValue in user.iteritems():
    setattr(u, attrName, attrValue)
  u.save()
  print "Updated user", username
for groupname, group in structure['groups'].iteritems():
  g = api.getList('group', name=groupname)[0]
  for attrName, attrValue in group.iteritems():
    setattr(g, groupName, groupValue)
  g.save()
  print "Updated group", groupname
