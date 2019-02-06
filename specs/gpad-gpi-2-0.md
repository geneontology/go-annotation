
# Proposed specifications for Gene Ontology Consortium GPAD and GPI tabular formats version 2.0

Table of contents
  * [Abstract](#abstract)
  * [Status](#status)
  * [Summary of changes relative to 1.2](#summary-of-changes-relative-to-12)
- [Outline](#outline)
  * [Preliminary Definitions](#preliminary-definitions)
    + [UML Notation](#uml-notation)
    + [BNF Notation](#bnf-notation)
    + [Basic Characters](#basic-characters)
    + [Spacing Characters](#spacing-characters)
    + [Identifiers](#identifiers)
    + [GO database registry](#go-database-registry)
    + [Property Symbols](#property-symbols)
    + [Dates](#dates)
- [GPAD Syntax](#gpad-syntax)
    + [GPAD Document Structure](#gpad-document-structure)
    + [GPAD Headers](#gpad-headers)
    + [Annotations](#annotations)
  * [GPAD columns](#gpad-columns)
- [GPI 2.0 Specs](#gpi-20-specs)
  * [GPI Headers](#gpi-headers)
  * [GP Entities](#gp-entities)
  * [GPI Columns](#gpi-columns)
  
## Abstract
This document specifies the syntax of Gene Product Annotation Data (GPAD) and Gene Product Information (GPI) formats. GPAD describes the relationships between biological entities (such as gene products) and biological descriptors (such as GO terms). GPI describes the biological entities.

## Status
This is a working draft, intended for comment by the community.
Comments should be sent to go-discuss AT geneontology.org

## Summary of changes relative to 1.2
  ### - columns 1 and 2 are now combined in both GPAD and GPI to form a single column containing an id in CURIE syntax, e.g. UniProtKB:P56704
  ### - In GPAD, negation is captured in a separate column, column 2, using the text string 'NOT'
  ### - In GPAD, the gene product-to-term relation captured in column 3 now uses a Relations Ontology (RO) identifier instead of a text string
  ### - In GPAD, the Reference column, column 5, is now a single value field.
  ### - In GPAD, the With/From column, column 7, may contain identifiers separated by commas as well as pipes.
  ### - In GPAD and GPI, NCBI taxon ids are prefixed with 'NCBITaxon:' to indicate the source of the id, e.g. NCBITaxon:6239
  ### - In GPAD, Annotation_Extensions in column 11 use a Relation_ID, rather than a Relation_Symbol, in the Relational_Expression.
  ### - In GPAD, the date is now in the format: YYYY-MM-DD (i.e. dashes between year, month, and day)
  ### - In GPI, the entity type in column 6 is captured using an ID from the Molecular Sequence Ontology.  
  ### - Extensions in file names are: \*.gpad and \*.gpi 
  
# Outline

We first start with some preliminary definitions, including a
description of the notation used in this specification.

The body of the document is split in two - the first part defines GPAD
syntax, the second defines GPI syntax.

## Preliminary Definitions

### UML Notation

This document uses only a very simple form of UML class diagrams that
are expected to be easily understandable by readers familiar with the
basic concepts of object-oriented systems.

### BNF Notation

GPAD and GPI document structures are defined using a standard BNF notation, which is summarized below.

 * terminal symbols are single quoted
 * non-terminal symbols are unquoted
 * zero or more symbols are indicated by following the symbol with a star; e.g. `Annotation*`
 * zero or one symbols are written using square brackets; e.g. `[Extension_Conj]`
 * alternative symbols are written using vertical bars
 * groupings are written using parentheses
 * complementation is written using minus symbol

GPI and GPAD documents consist of sequences of Unicode characters and are encoded in ASCII.

### Basic Characters

    Alpha_Char ::= a |b |c |d |e |f |g |h |i |j |k |l |m |n |o |p |q |r |s |t |u |v |w |x |y |z
       | A |B |C |D |E |F |G |H |I |J |K |L |M |N |O |P |Q |R |S |T |U |V |W |X |Y |Z
    Digit ::= 0 |1 |2 |3 |4 |5 |6 |7 |8 |9
    Alphanumeric_Char ::= Alpha_Char | Digit

### Spacing Characters

There is a single space character allowed

    Space ::= ' '

### Identifiers

An identifier consists of a prefix and a local identifier separated by a colon symbol

    ID ::= Prefix ':' Local_ID

A Prefix must not contain special characters such as ':'s

    Prefix ::= Alphanumeric | '_' | '-'

A local identifier can consist of any non-whitespace character

    Local_ID ::= (Any_ASCII_Character - ws)

An OBO ID is a type of identifier

    OBO_ID ::= ID

OBO identifiers (which include GO identifiers) SHOULD follow the [OBO identifier policy](http://www.obofoundry.org/id-policy.shtml)

References are also types of identifier

    Reference ::= ID

### GO database registry

The [GO database
registry](https://github.com/geneontology/go-site/blob/master/metadata/db-xrefs.yaml) contains a
list of valid prefixes that can be used in GPAD or GPI files. Every
identifier used in a GPAD or GPI file SHOULD have an entry in the
registry.

The combination of prefix plus Local_ID (see previous section)
describes how an identifier should be mapped to a URI.

### Property Symbols

Open-ended property-value pairs are allowed at different points
throughout a document. The property symbol or "tag" is a shorthand way
of specifying a URI that denotes the actual property used.

    Property_Symbol ::= ID | Alphanumeric

### Dates

Dates are written into what is equivalent to the date portion of ISO-8601, keeping hyphens:

    YYYY-MM-DD ::= Year - Month - Day_of_month
    Year ::= digit digit digit digit
    Month ::= digit digit
    Day_of_month ::= digit digit

Both months and days count from 1. E.g. Jan=1, first day of month=1.

A Date is equivalent to an
[xsd:date](http://www.w3.org/TR/xmlschema11-2/#date), and inherits the
same semantics and constraints.

# GPAD Syntax

### GPAD Document Structure

A GPAD document consists of a header followed by zero or more
annotations

    GPAD_Doc ::= GPAD_Header Annotation*

This is illustrated in the following UML diagram:

![image](gpad-document-uml.png)


### GPAD Headers

A header consists of an obligatory format version declaration followed
by zero or more metadata lines:

    GPAD_Header ::= '!gpa-version: 2.0' nl
                    GPAD_Header_Line*

Each metadata line starts with an exclamation mark '!'. One mark
indicates a structured tag-value pair, two marks indicates free text.

    GPAD_Header_Line ::=
       '!' Property_Symbol ':' Space* Value nl |
       '!!' (Char - nl)* nl

The list of allowed property symbols is open-ended, however several
properties are required:

 * go_version: PURL
 * ro_version: PURL
 * gorel_version: PURL
 * eco_version: PURL
 * gpad_date: YYYY-MM-DD (but see below)

Groups may decide to include additional information. Examples include:

 * Project_name: E.g. SGD
 * URL: E.g. http://www.yeastgenome.org/
 * Project_release: e.g. WS275
 * Funding: e.g. NHGRI
 * Columns: file format written out
 * Date: an ISO-8601 formatted date describing when the file was produced
 (Generated: YYYY-MM-DD 00:00 has also been used here; need to standardize)

### Annotations

In this specification, an annotation is an association between a
biological entity (such as a gene or gene product) and an ontology
class (term). The association describes some aspect of that entity,
and includes with metadata about the association, such as evidence and
provenance.

![image](gpad-uml.png)

Each annotation is on a separate line of tab separated values:

    Annotation ::= Col_1 tab Col_2 tab ... Col_12 nl

## GPAD columns

 Each of these columns has its own syntax, as specified below:
 
 Column 	| Content 	| Ontology  | Cardinality | Example ID
--------|----------|----------- | -------------- | ----------|
 1 | DB_Object_ID ::= ID | | 1 | UniProtKB:P11678 |
 2 | Negation ::= 'NOT' | | 0 or 1 | NOT |
 3 | Relation ::= OBO_ID | Relations Ontology | 1 | RO:0002263 |
 4 | Ontology_Class_ID ::= OBO_ID | Gene Ontology | 1 | GO:0050803 |
 5 | Reference ::= ID | | 1 | PMID:30695063 |
 6 | Evidence_type ::= OBO_ID | Evidence and Conclusion Ontology | 1 | ECO:0000315 |  
 7 | With_or_From ::= [ID] ('\|' \| ‘,’ ID)* | | 0 or greater | WB:WBVar00000510 |
 8 | Interacting_taxon_ID ::= NCBITaxon:[Taxon_ID] | | 0 or greater | NCBITaxon:5476 |
 9 | Date ::= YYYY-MM-DD | | 1 | 2019-01-30 |  
10 | Assigned_by ::= Prefix | | 1 | MGI |
11 | Annotation_Extensions ::= [Extension_Conj] ('\|' Extension_Conj)* | | 0 or greater | BFO:0000066 |   
12 | Annotation_Properties ::= [Property_Value_Pair] ('\|' Property_Value_Pair)* | | 0 or greater | contributor=https://orcid.org/0000-0002-1478-7671 |

Extension_Conj ::= [Relational_Expression] (',' Relational_Expression)*

Relational_Expression ::= Relation_ID '(' ID ')'

Property_Value_Pair ::= Property_Symbol '=' Property_Value

Property_Value  ::= (AnyChar - ('=' | '|' | nl))

### GPAD Annotation Properties (Proposed)

Annotation_Property_Symbol | Property_Value | Cardinality (if used) | Example | Semantics 
---------------------------|----------------|------------ | ------- | --------- |
 id | unique database identifier | 1 | 2113482942 | id=2113482942 | |
 go_evidence | three-letter GO code | 1 | go_evidence=IMP | |
 model-state | GO-CAM model state | 1 | model-state=production | |
 noctua-model-id | unique GO-CAM model id | 1 | noctua-model-id=gomodel:5a7e68a100001078 | |
 curator_name | text | 1 | Kimberly Van Auken | Used by UniProtKB to indicate name of curator who last changed an annotation 
 curator_uri (curator_id ?) | ORCID | 1 | curator_uri=https://orcid.org/0000-0002-1706-4196 | Used by UniProtKB to indicate ORCID of curator who last changed an annotation
 contributor (contributor_id ?) | ORCID | 1 | contributor=https://orcid.org/0000-0002-1706-4196 | Used by GOC to indicate ORCID of curator or user who entered or changed an annotation (SynGO lists multiple ORCIDs - what is the intended meaning?)
 reviewer (reviewer_id ?) | ORCID | 1 | reviewer=http://orcid.org/0000-0001-7476-6306 | Used by GOC to indicate ORCID of curator or user who last reviewed an annotation
 creation_date | YYYY-MM-DD | 1 | 2019-02-05 | The date on which the annotation was created.
 modification_date | YYYY-MM-DD | 1 | 2019-02-06 | The date(s) on which an annotation was modified.
 reviewed_date | YYYY-MM-DD | 1 | 2019-02-06 | The date(s) on which the annotation was reviewed.
 annotation_note | text | 1 | Confirmed species by checking PMID:nnnnnnnn. | Free-text field that allows curators or users to enter notes about a specific annotation.  

    
# GPI 2.0 Specs 

## GPI Headers

A header consists of an obligatory format version declaration followed
by an obligator database declaration then zero or more lines starting
with an exclamation point:

    GPI_Header ::= '!gpi-version: 1.1' nl
                   '!namespace: ' Prefix nl
                   Header_Line*

Each metadata line starts with an exclamation mark '!'. One mark
indicates a structured tag-value pair, two marks indicates free text.

    GPI_Header_Line ::=
       '!' Property_Symbol ':' Space* Value nl |
       '!!' (Char - nl)* nl
      
The list of allowed property symbols is open-ended, however several
properties are required:

 * mso_version: PURL
 * gpi_date: YYYY-MM-DD (but see below)

Groups may decide to include additional information. Examples include:

 * Project_name: E.g. SGD
 * URL: E.g. http://www.yeastgenome.org/
 * Project_release: e.g. WS275
 * Funding: e.g. NHGRI
 * Columns: file format written out
 * DB_Object_Type information, e.g. DB_Object_Type = "gene", DB = "MGI", DB_Object_ID = "MGI:xxxx"
 * Date: an ISO-8601 formatted date describing when the file was produced
 (Generated: YYYY-MM-DD 00:00 has also been used here; need to standardize)
       
## GP Entities

A GP entity is any biological entity that can be annotated using GPAD

![image](gpi-uml.png)

Each entity is written on a separate line of tab separated values:

    Entity ::= Col_1 tab Col_2 tab ... Col_9 nl
    
    
## GPI Columns

 Column 	| Content 	| Ontology  | Cardinality | Example ID | Comments
--------|----------|-----------|-----------|-----------|-----------|
1 | DB_Object_ID ::= ID      | | 1 | UniProtKB:Q4VCS5 | |
2 | DB_Object_Symbol ::= xxxx      | | 1 | AMOT | |
3 | DB_Object_Name ::= xxxx      | | 0 or greater | Angiomotin | | 
4 | DB_Object_Synonyms ::= [Label] ('\|' Label)*     | | 0 or greater | AMOT\|KIAA1071 | | 
5 | DB_Object_Type ::= OBO_ID      | Molecular Sequence Ontology | 1 | MSO:3100254 | | 
6 | DB_Object_Taxon ::= NCBITaxon:[Taxon_ID] || 1 |  NCBITaxon:9606 | |  
7 | Parent_ObjectID ::= [ID] ('\|' ID)* | | 1 |  | Need to be clear on what is meant by 'parent'.  Also, what is intended by the pipe here?|
8 | DB_Xrefs ::= [ID] ('\|' ID)* | | 0 or greater | |  Also need to be clear on what is required, e.g. MOD gene IDs xref to UniProtKB GCRP.| 
9 | Gene_Product_Properties ::= [Property_Value_Pair] ('\|' Property_Value_Pair)* |  | 0 or greater | db_subset=Swiss-Prot  | |

Property_Value_Pair ::= Property_Symbol '=' Property_Value

Property_Value  ::= (AnyChar - ('=' | '|' | nl))


### GPI Gene Product Properties (Proposed)

Annotation_Property_Symbol | Property_Value | Cardinality (if used) | Example | Semantics 
---------------------------|----------------|------------ | ------- | --------- |
db_subset | TrEMBL or Swiss-Prot | 1 | db_subset=TrEMBL | The status of a UniProtKB accession with respect to curator review.
uniprot_proteome | identifier  | 1 | uniprot_proteome=UP000001940 | A unique UniProtKB identifier for the set of proteins that constitute an organism's proteome.
go_annotation_complete | YYYY-MM-DD | 1| 2019-02-05 | Indicates the date on which a curator determined that the set of GO annotations for a given entity is complete with respect to GO annotation.  Complete means that all information about a gene has been captured as a GO term, but not necessarily that all possible supporting evidence is annotated.
go_annotation_summary | text | 1 | go_annotation_summary=Sterol binding protein with a role in intracellular sterol transport; localizes to mitochondria and the cortical ER | A textual gene or gene product description.
