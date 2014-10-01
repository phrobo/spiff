What is Spiff?
==============

Spiff is a hackerspace management tool that helps hackers manage a hackerspace.

Management of a hackerspace includes several topics:


- Membership
- Documentation
- Communication
- Infrastructure
- Governance

Spiff was originally written as part of SYNHAK, the Akron Hackerspace until its
untimely demise. However, Spiff was designed to be used by any other group on
the planet. Correspondingly, Spiff can be somewhat complicated at first blush.

This section aims to describe Spiff's expressiveness in reasonably
comprehendable terms.

Data Model
----------

In its simplest form, Spiff is a REST API on top of a relational database with a
small number of hooks that are activated when other objects in the database are
modified. Spiff itself does not provide any sort of user interface or website,
though a standalone web UI is included.

Each object type has a small set of related operations:

- list - Retrieve a list of objects that match a query
- get - Fetch a single object by its unique ID
- update - Modify properties of an object
- create - Create a new object
- delete - Delete an existing object

Permissions
-----------

Spiff contains an extensive set of permissions, allowing for the finest
precision of control on most data values. The map closely to the list of
operations permitted, possibly with other conditions involved. Examples:

- sensors.create_sensor: Can create a sensor
- sensors.delete_sensor: Can delete a sensor
- subscription.create_own_subscription: Can create a subscription, when owned by
  self
- subscription.update_others_subscription: Can update another user's
  subscription
- membership.read_private_fieldvalue: Can read field value, when field is
  private

For a full list, see the list of 'permission' objects via the API.

REST API
--------

All objects in spiff have a unique URI composed of the API version, object type,
and a unique ID. For example:

- /v1/member/1/
- /v1/resource/38/
- /v1/subscription/12/

This can also be used to reference objects across hackerspaces by including the
full URL:

- https://auth.hackerbots.net/v1/member/1/
- https://ratchet.noisebridge.net/v1/resource/8/

Querying the database is accomplished through simple URL syntax:

- /v1/member/?username=tdfischer
- /v1/resource/?metadata__name=stock&metadata__value__lte=10

There are a few rules to build queries:

- FOO=BAR -  Matches where the property 'FOO' equals exactly 'BAR'
- RELATION__FOO=BAR - Matches where the related RELATION object's FOO property
  equals exactly BAR
- FOO__isnull=1 - Matches where FOO is null in the database

The full set of operators are those available via tastypie. `Check the
django-tastypie documentation for details
<http://django-tastypie.readthedocs.org/en/latest/fields.html>`_
