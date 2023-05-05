####
#### Invocation examples:
####
#### Dump a TSV of terms found in all of the mapping files in snapshot, scanning geneontology/go-annotation issue contents for the last seven days with the label "mapping_hits_to_list_of_terms":
####
####   python3.6 ./scripts/mapping-report.py geneontology/go-annotation 7 --number 4564 --label mapping_hits_to_list_of_terms --input /tmp/snapshot.geneontology.org/ontology/external2go/ --output /tmp --verbose
####


import logging
import sys
import re
import requests
import json
import datetime
import argparse
import os
from pytz import timezone

###
### Global preamble.
###

## Logger basic setup w/killer error.
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('mapping-report')
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
parser.add_argument('-i', '--input',  help='Input directory')
parser.add_argument('-o', '--output',  help='Output directory')
parser.add_argument('-v', '--verbose', action='store_true', help='More verbose output')

args = parser.parse_args()

## Verbose messages or not.
if args.verbose:
    LOG.setLevel(logging.INFO)
LOG.info('Verbose: on')

if not args.input:
    die_screaming('need an input directory')
LOG.info('Will input to: ' + args.input)

if not args.output:
    die_screaming('need an output directory')
LOG.info('Will output to: ' + args.output)

if not args.number:
    die_screaming('need an issue number')
LOG.info('Will filter for issue: ' + args.number)

if not args.label:
    die_screaming('need an issue label')
LOG.info('Will filter for issue label: ' + args.label)

## Global. This was here before I got here--don't judge.
collected_terms = []

###
### Helpers.
###

## Append to global variable, including print information.
def collect_terms(issues, number: str, event_type: str, printed_ids: set):

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

    ## Filter and sort the items in global collected_terms([]).
    repo_name = args.repo_name
    if "/" in repo_name:
        repo_name = repo_name.rsplit("/", maxsplit=1)[-1]
    ids = set()
    collected_terms = collected_terms + collect_terms(new_issues, args.number, "New", ids)

    ## DEBUG:
    #collected_terms = ['GO:0030234', 'GO:0048478', 'GO:0031508']

    ## Check that we got something.
    if len(collected_terms) == 0:
        die_screaming('no terms found in collected_terms')

    ## All reports to single file.
    outfile = "-".join(collected_terms)

    ## Truncate length if too long:
    ## https://github.com/geneontology/go-annotation/issues/4495
    if len(outfile) > 100:
        outfile = outfile[0:98]
        outfile = outfile + '_etc'
        LOG.info('output list truncation: ' + outfile)

    ## Continue assembly.
    outfile = outfile.replace(':','_') + '.tsv'
    outfile = args.output + '/' + outfile
    LOG.info('output to file: ' + outfile)

    ## Define TSV headers.
    rfields = ["term",
               "file",
               "line"]

    ## Final writeout to files of the same name as the terms.
    mapping_directory = os.fsencode(args.input)
    mapping_files = os.listdir(mapping_directory)
    with open(outfile, 'w+') as fhandle:

        ## Print out header line.
        fhandle.write("\t".join(rfields))
        fhandle.write("\n")

        ## Print out reports.
        ## Iterate over terms.
        for term in collected_terms:
            LOG.info("term: " + term)

            ## Iterate over files.
            for map_file in mapping_files:
                filename = os.path.join(mapping_directory.decode("utf-8"),
                                        map_file.decode("utf-8"))
                #LOG.info("fullpath: " + filename)

                ## Iterate through file.
                with open(filename, "r") as infile:
                    for raw_line in infile:
                        line = raw_line.rstrip()
                        #LOG.info(line)

                        ## Print matching term lines.
                        if term in line:
                            #LOG.info(term + "\t" + filename + "\t" + line)
                            fhandle.write(term + "\t" + map_file.decode("utf-8") + "\t" + line)
                            fhandle.write("\n")
