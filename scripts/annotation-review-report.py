####
#### Invocation examples:
####
#### Dump GAF-like direct annotation TSVs into /tmp, scanning geneontology/simple-report-system titles for the last seven days with the label "direct_ann_to_list_of_terms":
####
####   python3.6 ./scripts/annotation-review-report.py geneontology/simple-report-system 7 --number 6 --field annotation_class --label direct_ann_to_list_of_terms --output /tmp --verbose
####

import logging
import sys
import re
import requests
import json
import datetime
import argparse
from pytz import timezone

###
### Global preamble.
###

## Logger basic setup w/killer error.
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('annotation-review-report')
LOG.setLevel(logging.WARNING)
def die_screaming(instr):
    """Make sure we exit in a way that will get Jenkins's attention."""
    LOG.error(instr)
    sys.exit(1)

## Get arge sorted.
parser = argparse.ArgumentParser()
parser.add_argument('repo_name')
parser.add_argument('duration_in_days')
parser.add_argument('-t', '--todays_date', help="Override the date to start 'looking back' from. Date must be in ISO format e.g. '2022-08-16'")
parser.add_argument('-n', '--number',  help='GH issue to filter for')
parser.add_argument('-l', '--label',  help='GH label to filter for')
parser.add_argument('-f', '--field',  help='The filter query to run (e.g. "annotation_class" or "regulates_closure"')
parser.add_argument('-o', '--output',  help='Output directory')
parser.add_argument('-v', '--verbose', action='store_true', help='More verbose output')

args = parser.parse_args()

## Verbose messages or not.
if args.verbose:
    LOG.setLevel(logging.INFO)
LOG.info('Verbose: on')

if not args.output:
    die_screaming('need an output directory')
LOG.info('Will output to: ' + args.output)

if not args.number:
    die_screaming('need an issue number')
LOG.info('Will filter for issue: ' + args.number)

if not args.label:
    die_screaming('need an issue label')
LOG.info('Will filter for issue label: ' + args.label)

if not args.field:
    die_screaming('need a filter query')
LOG.info('Will filter for field: ' + args.field)

## Globals. They were here before I got here--don't judge.
collected_issues = []
new_printed_count = 0
updated_printed_count = 0

## Return fields.
rfields = [
           'assigned_by',
           'bioentity',
           'bioentity_label',
           'reference',
           'qualifier',
           'annotation_class',
           'annotation_class_label',
           'evidence_type',
           'evidence_with',
           'bioentity_isoform',
           'panther_family',
           'date',
           'annotation_extension_class',
           'taxon'
        ]

###
### Helpers.
###

## Append to global variable, including print information.
def collect_issues(issues, number: str, event_type: str, printed_ids: set):

    cis = []

    for issue in issues:
        if (issue['state'] == 'open') and (int(number) == issue['number']):
            has_label_p = False
            if len(issue['labels']) > 0 :
                for label in issue['labels']:
                    if label['name'] == args.label:
                        has_label_p = True
            matches = re.findall("GO:[0-9]+", issue['body'])
            if has_label_p and len(matches) > 0:
                matches = re.findall("GO:[0-9]+", issue['body'])
                for m in matches:
                    cis.append(m)
    ## Dedupe and sort.
    cis = list(dict.fromkeys(cis))
    cis.sort()
    return cis

## Pull issues from GH.
def get_issues(repo: str, event_type: str, start_date: str):
    url = "https://api.github.com/search/issues?q=repo:{}+{}:=>{}+is:issue&type=Issues&per_page=100".format(repo, event_type, start_date)
    #url = "https://api.github.com/repos/{}/issues/{}".format(repo, number)
    resp = requests.get(url)
    if resp.status_code == 200:
        resp_objs = json.loads(resp.content)
        issues = resp_objs.get("items", [])
        #issues = [resp_objs]
        return issues
    else:
        raise Exception("HTTP error status code: {} for url: {}".format(resp.status_code, url))

## Get Annotation TSV from GOlr.
def get_term_annotation_data(fq: str, term: str):
    url = "http://golr-aux.geneontology.io/solr/select?defType=edismax&qt=standard&indent=on&wt=csv&rows=100000&start=0&fl={}&facet=true&facet.mincount=1&facet.sort=count&json.nl=arrarr&facet.limit=25&hl=true&hl.simple.pre=%3Cem%20class=%22hilite%22%3E&hl.snippets=1000&csv.encapsulator=&csv.separator=%09&csv.header=false&csv.mv.separator=%7C&fq={}:%22{}%22&fq=evidence_subset_closure:%22ECO:0000006%22&fq=document_category:%22annotation%22&q=*:*".format(','.join(rfields), fq, term)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("HTTP error status code: {} for url: {}".format(resp.status_code, url))
    else:
        resp_tsv = resp.text.rstrip()

        ## Split and clean references column--PMID first if there.
        resp_list = resp_tsv.split("\n")
        cleaned_list = []
        for r in resp_list:
            cols = r.split("\t")
            ref = cols[3]
            split_ref = ref.split('|')
            if len(split_ref) == 2:
                if 'PMID:' in split_ref[1]:
                    cols[3] = split_ref[1] + '|' + split_ref[0]
            cleaned_list.append("\t".join(cols))
        resp_list = cleaned_list

        ## Alphabetical sort by col4 (reference), then col1 (assigned_by).
        def sorter(line: str):
            ll = line.split("\t")
            ind = ll[3]
            return ind
        resp_list = sorted(resp_list, key=sorter)
        resp_list = sorted(resp_list, key=lambda line: line.split("\t")[0])

        return "\n".join(resp_list)

###
### Main.
###

## Start.
if __name__ == "__main__":

    ## Get date/time for GH interactions/filtering.
    today_time = datetime.datetime.now(tz=timezone('US/Pacific'))
    if args.todays_date:
        try:
            today_time = datetime.datetime.strptime(args.todays_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, todays_date should be YYYY-MM-DD")
    yesterday_time = today_time - datetime.timedelta(int(args.duration_in_days))
    yesterday_time_str = yesterday_time.isoformat()

    ## Get times/dates for display.
    today = today_time.strftime("%Y-%m-%d")
    yesterday = yesterday_time.strftime("%Y-%m-%d")

    ## Pull in created and updated issues.
    new_issues = get_issues(args.repo_name, "created", yesterday_time_str)
    #updated_issues = get_issues(args.repo_name, "updated", yesterday_time_str)

    ## Filter and sort the items in global collected_issues([]).
    repo_name = args.repo_name
    if "/" in repo_name:
        repo_name = repo_name.rsplit("/", maxsplit=1)[-1]
    ids = set()
    collected_issues = collected_issues + collect_issues(new_issues, args.number, "New", ids)

    ## DEBUG:
    #collected_issues = ['GO:0030234', 'GO:0048478', 'GO:0031508']

    ## Check that we got something.
    if len(collected_issues) == 0:
        die_screaming('no terms found in ')

    ## All reports to single file.
    outfile = "-".join(collected_issues)
    outfile = outfile.replace(':','_') + '.tsv'
    outfile = args.output + '/' + outfile
    LOG.info('output to file: ' + outfile)

    ## Final writeout to files of the same name as the term.
    with open(outfile, 'w+') as fhandle:

        ## Single header.
        fhandle.write("\t".join(rfields))
        fhandle.write("\n")

        ## Print out reports.
        for t in collected_issues:
            LOG.info(t)

            ## Print out header line:
            fhandle.write(get_term_annotation_data(args.field, t))
            fhandle.write("\n")
