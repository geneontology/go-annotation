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
We use labels to organize the work in this repo. These are useful for housekeeping; ie checking the status of old tickets, closing tickets that have been done, that are out-of-date, and reminding people of works that needs to be done. 

## label:annotation review
Query for tickets that were opened for ontology work: 
* `is:open label:"annotation review" label:"direct_ann_to_list_of_terms","reg_ann_to_list_of_terms"` (the comma is an OR).
### Tickets will fall into a few broad categories
#### A. The ticket requested a review for a term obsoletion:
 1. If the [go-ontology](https://github.com/geneontology/go-ontology/issues) ticket is **closed**:
   * Open the associated Google spreadsheet, and if every annotation has been addressed, change the title to add `DONE` at the begining of the file name; otherwise, put `CLOSED`
   * Add a comment to the ticket `This term was obsoleted; remaining annotations will appear in GORULES error reports`.
   *  _Example:_ [issue-4639](https://github.com/geneontology/go-annotation/issues/4639)
 2. If the [go-ontology](https://github.com/geneontology/go-ontology/issues) ticket is still **open**:
   * Check the corresponding Google spreadsheet to see whether all reviewed have been done.
     * 2.1. If all annotations have been reviewed:
       * Change the title of the Google spreadsheet to add `DONE`at the begining of the file name
       * Close the go-annotation ticket
       * Add a comment to the [go-ontology](https://github.com/geneontology/go-ontology/issues) ticket: `All annotations have been fixed` and add the label `ready`.
     * 2.2 If some annotations have been not been reviewed:
       * 2.1.1 If the annotation review is > 6 months old: Change the title of the Google spreadsheet to add `CLOSED`at the begining of the file name  
       * 2.1.2 Close the annotation ticket, and add a comment to the [go-ontology](https://github.com/geneontology/go-ontology/issues) ticket `Annotation Review is out-of-date and was closed`.
       * 2.1.2 If the review is < 6 months old, ping the assignees that still need to review annotations. (People should not be pinged more than 2-3 times; after we assume that they will not get to the work).
       * _Example:_ [issue-4639](https://github.com/geneontology/go-annotation/issues/4639)
  3. If the [go-ontology](https://github.com/geneontology/go-ontology/issues) ticket is not linked in the go-annotation, search the [go-ontology](https://github.com/geneontology/go-ontology/issues) repo with the term ID or label. If there is no results, close the ticket with the comment that `The corresponing go-ontology ticket does not exist`.
     * _Example:_ [issue-4583](https://github.com/geneontology/go-annotation/issues/4583)
#### B. The ticket requested a review, without requesting an obsoletion:
* Check the corresponding Google spreadsheet to see whether all reviewed have been done.
 1. If all annotations have been reviewed:
    * Change the title of the Google spreadsheet to add `DONE`at the begining of the file name
    * Close the go-annotation ticket
 2. If some annotations have been not been reviewed:
     * Ping the assignees that still need to review annotations. (People should not be pinged more than 2-3 times; after we assume that they will not get to the work).
     * Ping the `author` of the ticket to see if the review is still valid.
  * _Example:_ [issue-4583](https://github.com/geneontology/go-annotation/issues/4583)
#### C. The ticket doesn't formulate a clear request: 
  * Ping the author of the ticket. This can be done 2-3 times, at > 2-3 months intevals. If there is no reply, close as `not planned`.
  * * _Examples:_ [issue-4497](https://github.com/geneontology/go-annotation/issues/4497),[issue-4598](https://github.com/geneontology/go-annotation/issues/4598)
## label:PAINT annotation and label:PAINT - waiting for primary annotation 
* Monitored by the PAINT annotation team.
* If there has not been any comment on a ticket in > 1 year, ping the assignee(s) or close the ticket if it is out-of-date.
