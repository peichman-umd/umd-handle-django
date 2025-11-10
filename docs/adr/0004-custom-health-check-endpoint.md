# 0004 - Custom Health Check Endpoint

Date: November 10, 2025

## Context

In Kubernetes, containers are monitored using startup, liveness, and readiness
probes (see ["Liveness, Readiness, and Startup Probes"][kube-probes] in
the Kubernetes documentation).

This application should provide a "health check" endpoint, to support the
Kubernetes pod probes, and enable Kubernetes to restart the container if
necessary. For simplicity in implementing the pod probes, this endpoint should
not require any authentication.

In Grove, the root URL ("/") endpoint is used for the Kubernetes pod probes.
This solution is not applicable to this application because the root URL
redirects to CAS, and all of the stock Django admin interface views are
CAS-protected.

Similarly, it is planned that the "/api" REST endpoints will required a JSON Web
Token (JWT) for access.

Multiple Django "health check" packages exist that could be used, such as:

* [django-health-check](https://github.com/revsys/django-health-check)
* [django-watchman](https://github.com/mwarkentin/django-watchman)

Writing a custom "health check" endpoint is also feasible, and would reduce
the number of dependencies the project has.

## Decision

It was decided that a simple, custom "/health-check" endpoint that simply
returns an HTTP status 200 response and an "OK" message was all that was
required for the application at this time.

The default "health check" endpoints provided by "django-health-check" and
"django-watchman" packages not only check for an application response, but
also whether there is a database connection. There has been past debate
over whether the database connection should be verified as part of an
application health check.

In the end, it was decided that both of the packages included much more
functionality than was needed for the application, and would bring in additional
dependencies which were not required.

## Consequences

Having a health check only verifies that an HTTP response is received may be
too simplistic. However, it should straightforward to upgrade to a more
robust health check (possibly using one of the packages mentioned above)
if it becomes necessary.

---
[kube-probes]: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
