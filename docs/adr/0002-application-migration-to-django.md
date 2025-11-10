# 0002 - Application migration to Django

Date: November 10, 2025

## Context

The "UMD Handle" application was originally written in Ruby on Rails (see
<https://github.com/umd-lib/umd-handle>).

In November 2025, the Ruby on Rails v6.1.3.1 framework on which the application
was built was beyond its "end-of-life" date, and an upgrade to Ruby on Rail v8.1
was proposed.

In examining the steps needed to upgrade to Ruby on Rails v8.1, it was
determined that extensive work would need to be done to migrate the application.
This was due to:

* Changes in the Rails "asset pipeline" between Rails v6 and Rails v7, as well
  as additional changes in Rails v7 to Rails v8. This made a smooth step-by-step
  upgrade challenging, because work would be done to upgrade the application to
  Rails v7, which would then be "thrown away" to upgrade to Rails v8.

* The "UMD Handle" application used Bootstrap v3 for the application styling.
  While it is not impossible to use Bootstrap v3 with Rails v8 and its
  asset pipeline, the path of least resistance would be to upgrade the
  application to Bootstrap 5, which is more compatible with modern Rails
  development.

Given the challenges of upgrading the application to Ruby of Rails v8.1,
it was proposed that the application be re-written in Django. The stated
rationales were:

* The level of effort needed to upgrade the application to Rails v8.1 and
  Bootstrap v5 seemed roughly comparable to rewriting the application in Django.

* SSDR, as an organization, has been moving away from Ruby/Ruby on Rails
  applications in preference to Python/Django applications

* the stock Django admin interface could replace the custom administrative
  interface in the Rails-based "umd-handle" application, significantly
  simplifying the application.

## Decision

In the November 3, 2025 Digital Collections Sprint Planning meeting, it was
decided to migrate the "UMD Handle" application functionality to Django, and
replace the custom administrative interface with the stock Django admin
interface.

## Consequences

The main consequence of this decision is to continue the move of SSDR
applications from Ruby/Ruby on Rails to Python/Django. This is intended to
provide simpler upgrades and better developer support (as more SSDR developers
have a familiarity with Python than Ruby).

The migration does require a data migration from the Rails-based database schema
to the Django-based database schema, but given the simplicity of the data, this
is not expected to be a major issue.

The main function of the application is as a REST API to other applications,
such as fcrepo, Avalon, and the Handle.net handle server. As the REST API
contract is expected to be maintained, these application should be able to
communicate to the Django-based application without change.
