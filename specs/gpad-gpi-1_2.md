% GPAD and GPI Tabular Formats version 1.2
% Gene Ontology Consortium
% Revision: $Rev: 7306 $

### Abstract

This document specifies the syntax of Gene Product Annotation Data
(GPAD) and Gene Product Information (GPI) formats. GPAD describes the
relationships between biological entities (such as gene products) and
biological descriptors (such as GO terms). GPI describes the
biological entities.

### Status

This is an working draft, for comment by the community.

 * Date: $Date: 2013-03-22 15:21:43 -0700 (Fri, 22 Mar 2013) $

Comments should be sent to go-discuss AT geneontology.org

## Changes in GPAD and GPI relative to 1.0

  - add column for db in GPI, do not use the header
  - allow a relation in the GPAD interacts_with_taxon (list),
    relation(taxon)
    -> DavidOS: interacts_with_other_organism (RO id?)
  - GPAD Standard set of properties:
    annotation_id ("id"), "curator_name" (DC_Author),
    "go_evidence" (shorthand), comment
  - GPI properties: DB_Subset (swissprot vs tremble),
    Annotation_Complete (Date), slim/subset type of thing
  - JSON: properties is an array with objects
  - file names: *.gpa (also accepted *.gpad) and *.gpi

## Introduction

### Background

The [Gene Ontology project](http://geneontology.org) provides
annotations describing attributes of biological entities such as genes
and gene products.

The Gene Ontology has historically provided annotations via Gene
Association Format (GAF), including
[GAF-1](http://www.geneontology.org/GO.format.gaf-1_0.shtml) and
[GAF-2](http://www.geneontology.org/GO.format.gaf-2_0.shtml). Ontologies
are distributed separately, using an OWL serialization or OBO format.

The use of GAF has some drawbacks:

 * Combined representation of gene/gene product data and annotations leads to redundancy/repetition
 * No way to represent gene/gene product metadata for unannotated genes
 * Requirement to maintain backward compatibility makes it harder to introduce enhancements such as use of an ontology for evidence types

GAF formats will continue to be supported, but the need for a way to
represent genes/gene products separately from annotations, as well as
the need to use the evidence ontology has lead to the creation of the
GPAD (Gene Product Annotation Data) and GPI (Gene Product Information)
formats, defined here.

Whilst GPAD and GPI have been defined for use within the Gene Ontology
Consortium for GO annotation, this specification is designed to be
reusable for analagous ontology-based annotation - for example, gene
phenotype annotation.

*TODO* provide link ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/

### Outline

We first start with some preliminary definitions, including a
description of the notation used in this specification.

The body of the document is split in two - the first part defines GPAD
syntax, the second defined GPI syntax.

## Preliminary Definitions

### UML Notation

his document uses only a very simple form of UML class diagrams that
are expected to be easily understandable by readers familiar with the
basic concepts of object-oriented systems.

*TODO* - move UML elsewhere

### BNF Notation

GPAD and GPI document structures are defined using a standard BNF notation, which is summarized below.

 * terminal symbols are single quoted
 * non-terminal symbols are unquoted
 * zero or more symbols are indicated by following the symbol with a star; e.g. `Annotation*`
 * zero or one symbols are written using square brackets; e.g. `[Qualifier]`
 * alternative symbols are written using vertical bars
 * groupings are written using parentheses
 * complementation is written using minus symbol

GPI and GPAD documents consist of sequences of Unicode characters and are encoded in UTF-8 [RFC 3629].

 * TODO - do we allow UTF-8 or restrict to ASCII? DECIDED: ASCII

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
registry](http://www.geneontology.org/cgi-bin/xrefs.cgi) contains a
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

Dates are written into what is equivalent to the date portion of ISO-8601, omitting hyphens:

    YYYYMMDD ::= Year Month Day_of_month
    Year ::= digit digit digit digit
    Month ::= digit digit
    Day_of_month ::= digit digit

Both months and days count from 1. E.g. Jan=1, first day of month=1.

A Date is equivalent to an
[xsd:date](http://www.w3.org/TR/xmlschema11-2/#date), and inherits the
same semantics and constraints.

## GPAD Syntax

### GPAD Document Structure

A GPAD document consists of a header followed by zero or more
annotations

    GPAD_Doc ::= GPAD_Header Annotation*

This is illustrated in the following UML diagram:

![image](gpad-document-uml.png)


### GPAD Headers


A header consists of an obligatory format version declaration followed
by zero or more metadata lines:

    GPAD_Header ::= '!gpa-version: 1.1' nl
                    GPAD_Header_Line*

Each metadata line starts with an exclamation mark '!'. One mark
indicates a structured tag-value pair, two marks indicates free text.

    GPAD_Header_Line ::=
       '!' Property_Symbol ':' Space* Value nl |
       '!!' (Char - nl)* nl

The list of allowed property symbols is open-ended and outside the
scope of this specification. Different groups may decide on their own
conventions. Examples include:

 * Project_name: E.g. SGD
 * URL: E.g. http://www.yeastgenome.org/
 * Funding: e.g. NHGRI
 * Date: an ISO-8601 formatted date describing when the file was produced

### Annotations

In this specification, an annotation is an association between a
biological entity (such as a gene or gene product) and an ontology
class (term). The association describes some aspect of that entity,
and includes with metadata about the association, such as evidence and
provenance.

![image](gpad-uml.png)

Each annotation is on a separate line of tab separated values:

    Annotation ::= Col_1 tab Col_2 tab ... Col_12 nl

Each of these columns has its own syntax, as specified below:

1. `DB ::= Prefix`
2. `DB_Object_ID ::= Local_ID`
3. `Qualifiers ::= [Qualifier] ('|' Qualifier)*`
4. `Ontology_Class_ID ::= OBO_ID`
5. `References ::= Reference ('|' Reference)*`
6. `Evidence_type ::= OBO_ID`
7. `With_or_From ::= [ID] ('|' ID)*`
8. `Interacting_taxon_ID ::= [Taxon_ID]`
9. `Date ::= YYYYMMDD`
10. `Assigned_by ::= Prefix`
11. `Annotation_Extensions ::= [Extension_Conj] ('|' Extension_Conj)*`
12. `Annotation_Properties ::= [Property_Value_Pair] ('|' Property_Value_Pair)*`

C1 and C2 combine to form a unique reference to the *Entity* being
described. C4 and C11 (and optionally C8) combine to form a
*Description* of a biological attribute. C3 is the relationship
between this entity and the description (for example, "involved
in"). The other columns combine to make metadata about the annotation;
C5, C6 and C7 describe the evidence for the association plus its
provenance.

### Annotation extensions

Documentation on this column is available on the [column
16](http://www.geneontology.org/GO.annotation.col_16.shtml) page (note
that we identify columns by their position in GAF).

The value of this column is a pipe-separated list of zero or more
conjunctive expressions:

    Extension_Conj ::= [Relational_Expression] (',' Relational_Expression)*
    Relation_Expression ::= Relation_Symbol '(' ID ')'

### Property-Value pairs

A property value pair uses an open-ended vocabulary of properties to
association information with the annotation.

    Property_Value_Pair ::= Property_Symbol '=' Property_Value
    Property_Value  ::= (AnyChar - ('=' | '|' | nl))

*TODO* define AnyChar such that escaping is allowed

Properties may include the name or ID of the curator who made the
annotation. Recommendations on the property vocabulary will be
provided separately.

*TODO*

### Qualifiers and Relations

A qualifier is either a logical modifier or a relation

    Qualifier ::= Modifier | Relation_Symbol

The only modifier is logical negation

    Modifier ::= 'NOT'

This specification does not mandate which relations are allowed.  The
full set of relations allowed are specified in a separate GO relations
ontology. This ontology also specifies the domain and range
constraints for these relations.

### GPAD Validation

For GO annotations, all [annotation QC
rules](http://www.geneontology.org/GO.annotation_qc.shtml) apply.

Specifically

 * All Prefixes MUST be registered in GO.xrf_abbs
 * The Ontology_Class_ID MUST be a GO ID and SHOULD correspond to a non-obsolete, non-merged class
 * The Evidence_code MUST be an ECO ID

### GPAD Semantics

Detailed semantics will be provided in future via a mapping to
OWL. For now, consult the main GO documentation for a description of
the columns used here, and recommendations on how to use them. E.g.

 * [GAF-2](http://www.geneontology.org/GO.format.gaf-2_0.shtml).

See also the section on mapping to GAF-2 in this document.

## GPI Syntax


### GPI Document Structure

    GPI_Doc ::= GPI_Header Entity*

### GPI Headers

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


*TODO* - decide whether to support multiple namespaces in one document
(we are leaning towards allowing this for the mega-gpi use case - DECIDED)


### GP Entities

A GP entity is any biological entity that can be annotated using GPAD

![image](gpi-uml.png)

Each entity is written on a separate line of tab separated values:

    Entity ::= Col_1 tab Col_2 tab ... Col_9 nl

Each of these columns has its own syntax, as specified below:

1. `DB ::= Prefix`
2. `DB_Object_ID ::= Local_ID`
3. `DB_Object_Symbol ::= xxxx`
4. `DB_Object_Name ::= xxxx`
5. `DB_Object_Synonyms ::= [Label] ('|' Label)*`
6. `DB_Object_Type ::= Type_Symbol`
7. `DB_Object_Taxon ::= Taxon_ID`
8. `Parent_ObjectID ::= [ID??] ('|' ID)*`
9. `DB_Xrefs ::= [ID??] ('|' ID)*`
10. `Properties ::= [Property_Value] (',' Property_Value)*`

The ID for the entity is formed as follows:

    ID = CONCAT( Namespace ':' Local_ID)

*TODO* describe semantics of other columns


### GPI Validation

 * TODO

### GPI Semantics

 * TODO

## Mapping between GAF-2 and GPI/GPAD

GAF is broadly speaking the relational join of GPAD and GPI. However,
there are subtle differences that require additional operations when
interconverting between the two.

### Column mappings

The following mappings describe how GAF-2 columns map to GPAD/GPI

1. `DB --> GPAD-c1 & GPI-Header`
2. `DB_Object_ID --> GPAD-c2 & GPI-c1`
3. `DB_Object_Symbol --> GPI-c3`
4. `Qualifiers --> GPAD-c3` (see notes below)
5. `Ontology_Class_ID --> GPAD-c4`
6. `References --> GPAD-c5`
7. `Evidence_code --> ECO(GPAD-c6)`
8. `With_or_From ::= GPAD-c7`
9. `Apsect --> derived from GPAD-c4`
10. `DB_Object_Name --> GPI-c3`
11. `DB_Object_Synonym --> GPI-c4`
12. `DB_Object_Type --> GPI-c5`
13. `Taxon --> GPI-c6 (| GPAD-c8)`
14. `Date --> GPAD-c9`
15. `Assigned_by ::= GPAD-c10`
16. `Annotation_Extension ::= GPAD-c11`
17. `Gene-Product-Form-ID ::= see notes`

### Gene Product Form rewrites

One crucial difference between GAF and GPAD/GPI is that in GAF,
associations MUST be made to gene or canonical protein (which
corresponds to a gene). If the intent is to describe some aspect a
particular form (e.g. isoform) of that gene, then this is indicated in
GAF-c17.

In GPAD, associations are made directly to entity being described, as
closely as possible. The mapping must therefore include extra steps.

When converting from an annotation GPAD/GPI to GAF, first check the
Parent field in the GPI for the corresponding entity. If there is no
entry, proceed according to the table above. If there is an entity,
then use this entity *as if* it were in GPAD-c1+c2, and place the
original value of GPAD-c1+c2 in GAF-c17.

*TODO* this is still underspecified - discussed 2012-03-14, decided probably fine

### ECO mapping

The following permanent URL contains a mapping table that specifies
how to generate a specific ECO class ID from (1) a GAF code and (2) a
GO_REF used in the With column of a GAF:

http://purl.obolibrary.org/obo/eco/gaf-eco-mapping.txt

### Default Annotation Relations

GAF has a qualifier column (GAF-c4) which may contain the NOT
modifier, or the contributes_to or colocalized_with relations. There
is no way to indicate any other relationship type.

When translating, if no relation is specified, then the follow
defaults are chosen:

 * part_of (cell component)
 * involved_in (biological process)
 * enables (molecular functon)

If a NOT modifer is present, then this is also included (separated by
'|').

If the following relations are present in the GAF, they are used in
the GPAD document as-is:

 * colocalized_with
 * contributes_to

See [http://www.geneontology.org/GO.annotation.conventions.shtml](conventions)

### Other relations

The list of relations that can be used is open-ended, but these should
come from RO. The following will be in standard usage in GO from 2016
onwards:

 * acts_upstream_of_or_within
 * acts_upstream_of
 * involved_in

## References

*TODO*
