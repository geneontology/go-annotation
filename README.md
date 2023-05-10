# go-annotation

This repository hosts the tracker for issues pertaining to GO annotations. For issues with the EBI GOA tools such as QuickGO, Protein2GO and the GOA database and annotations please email goa@ebi.ac.uk.

# simple-report-system

## Overview

This is an experimental GH Actions-based report runner.

As it stands now (and this still a bit of a mess) what we have is:

* when an issue is opened
* multiple GH workflows are triggered
* if a workflow matches the label on the issue, it continues (otherwise skipped)
* a matching workflow
  * greps out GO terms from the issue _body_.
  * makes annotation TSVs for the matched terms
  * puts them into a reports/ directory for the opened issue number
  * commits the reports back into `main`

## Current reports by label

### direct\_ann\_to\_list\_of\_terms

A set of TSVs of the annotations directly annotated the given GO terms. This report also includes direct mappings to all terms in the list.

### reg\_ann\_to\_list\_of\_terms

A set of TSVs of the direct and indirect annotations over the regulates
closure for the given GO terms. This report also includes mappings (direct and indirect annotations over the regulates
closure) to all terms in the list. 

## Things to ponder

- all sorts of fun triggers and actions can be thought of here
- cleaning/archiving could be ticket closing
- maybe use gist API (pass secret)
  - allow for (easier-to-access?)raw TSVs
  - could append link comments to ticket once produced
- act on locks instead of open
- other APIs, not just cheaping out on GOlr
- remote trigger to bigger machines
- grebe
- more structured runner / delagation
- editing / deleting output with the GH "code" editors; curator workflow control
