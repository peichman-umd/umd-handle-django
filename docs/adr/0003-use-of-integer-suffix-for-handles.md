# 0003 - Use of integer suffix for handles

Date: November 10, 2025

## Context

A handle has the form "PREFIX/SUFFIX", such as "1903.1/1351".

The prefix ("1903.1") is registered with the "Handle.Net" registry. The suffix
("1351") is an alphanumeric field. Historically, the handle minting service
used by the libraries has generated numerical suffixes. However, according to
the Handle specification, there is nothing that prevents it from being
a string (such as "udhc") or some other combination of letters and numbers.

## Decision

This decision follows the decision made in the Ruby on Rails-based "UMD Handle"
application that used integer-bases suffixes (see
<https://github.com/umd-lib/umd-handle/blob/181388f5f103fdaab74b707c144ab7927b70c7d9/docs/adr/0003-use-of-integer-suffix.md>)
which provided the following rationale:

> In the initial work done for the application, the "suffix" field was
> considered to be numeric, and so in the database schema was given an "integer"
> type. The  "minting" service was able to leverage the "integer" type to create
> unique suffixes for a prefix via the use of the SQL "max" operation.
>
> When it became apparent that the "Handle" specification allowed alphanumeric
> suffixes, there was discussion over whether this was something the application
> needed to support.
>
> Supporting alphanumeric suffixes would increase the complexity of the
> "minting" operation, especially if users were allowed to provide a suffix as
> part of > handle creation.
>
> It was decided that the current known use cases for the application do not
> require supporting alphanumeric suffixes, and that the additional complexity
> is not worth supporting at this time.

Experience with the application since writing the above has not invalidated any
of the rationales, so the decision was retained for this application.

## Consequences

Only supporting numeric suffixes may limit the flexibility of the application
in possible future use cases. However, it is expected that modifying the
application to support alphanumeric suffixes should be reasonably
straightforward, if and when it is determined to be necessary.
