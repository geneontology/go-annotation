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


# SOP for housekeeping of this repo
We use labels to organize the work in this repo. 

## annotation review
Query for tickets opened for ontology work: 
- is:open label:"annotation review" label:"direct_ann_to_list_of_terms","reg_ann_to_list_of_terms" (the comma is an OR).
- Tickets fall into some broad categories:
* The ticket requested a review for a term obsoletion:
* * check if the corresponding [go-ontology](https://github.com/geneontology/go-ontology/issues) ticket has been closed (it should be linked in the ticket).
  * If the ticket is closed:
  * * open the associated spreadsheet, and change the title to add DONE (if every annotation has a curator comment); otherwise, put  CLOSED
  * * Add a comment to the ticket "This term was obsoleted; remaining annotations will appear in GORULES error reports".
* * If the go-ontology](https://github.com/geneontology/go-ontology/issues) ticket is not linked in the go-annotation, search the go-ontology](https://github.com/geneontology/go-ontology/issues) repo with the term ID or label. If there is no results, close the ticket with the comment that 'the corresponing go-ontology ticket does not exist'. 

## PAINT annotation and PAINT - waiting for primary annotation 
- Monitored by the PAINT annotation team.
- If there has not been any comment on a ticket in > 1 year, ping the assignee(s) or close the ticket if it is out-of-date.
