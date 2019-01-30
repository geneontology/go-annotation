# Proposed specifications for Gene Ontology Consortium GPAD and GPI tabular formats version 2.0

## Abstract
This document specifies the syntax of Gene Product Annotation Data (GPAD) and Gene Product Information (GPI) formats. GPAD describes the relationships between biological entities (such as gene products) and biological descriptors (such as GO terms). GPI describes the biological entities.

## Status
This is a working draft, intended for comment by the community.
Comments should be sent to go-discuss AT geneontology.org

## Summary of changes relative to 1.2
  - columns 1 and 2 are now combined in both GPAD and GPI to form a single column containing an id in CURIE syntax, e.g. UniProtKB:P56704
  - In GPAD, negation is captured in a separate column, column 2, using the text string 'NOT'
  - In GPAD, the gene product-to-term relation captured in column 3 now uses a Relations Ontology (RO) identifier instead of a text string
  - In GPAD, the Reference column, column 5, is now a single value field.
  - In GPAD, the With/From column, column 7, may contain identifiers separated by commas as well as pipes.
  - In GPAD and GPI - anything to change about taxon id, i.e. NCBI:txid6239
  - In GPAD, Annotation_Extensions in column 11 use a Relation_ID, rather than a Relation_Symbol, in the Relational_Expression.
  - GPAD Standard set of properties: ##Still need to agree on these
    annotation_id ("id"), "curator_name" (DC_Author),
    "go_evidence" (shorthand), comment
  - In GPI, the entity type in column 6 is capture using an ID from the Sequence Ontology.  
  - GPI properties:  ##Still need to agree on these
    DB_Subset (swissprot vs tremble),
    Annotation_Complete (Date), slim/subset type of thing
  - file names: *.gpa (also accepted *.gpad) and *.gpi ##Are we just going with .gpad and .gpi?

## GPAD columns

 Each of these columns has its own syntax, as specified below:
 
 Column 	| Content 	| Comments
--------|----------|-----------
 1 | DB_Object_ID ::= ID   |   
 2 | Negation ::= 'NOT'     | 
 3 | Relation ::= OBO_ID        | 
 4 | Ontology_Class_ID ::= OBO_ID     | 
 5 | Reference ::= ID      | 
 6 | Evidence_type ::= OBO_ID     | 
 7 | With_or_From ::= [ID] ('\|' \| ‘,’ ID)*     | 
 8 | Interacting_taxon_ID ::= NCBI:txid[Taxon_ID] | Will this break too many things?
 9 | Date ::= YYYYMMDD     | 
10 | Assigned_by ::= Prefix     | 
11 | Annotation_Extensions ::= [Extension_Conj] ('\|' Extension_Conj)*       |   
12 | Annotation_Properties ::= [Property_Value_Pair] ('\|' Property_Value_Pair)*     | 

Extension_Conj ::= [Relational_Expression] (',' Relational_Expression)*
Relational_Expression ::= Relation_ID '(' ID ')'

Property_Value_Pair ::= Property_Symbol '=' Property_Value
Property_Value  ::= (AnyChar - ('=' | '|' | nl))
    
## Headers 
    
need to be standard
    
# GPI 2.0 Specs 
## Columns
 Column 	| Content 	| Comments
--------|----------|-----------
1 | DB_Object_ID ::= ID      | 
2 | DB_Object_Symbol ::= xxxx     | 
3 | DB_Object_Name ::= xxxx     | 
4 | DB_Object_Synonyms ::= [Label] ('\|' Label)*     | 
5 | DB_Object_Type ::= OBO_ID     | 
6 | DB_Object_Taxon ::= NCBI:txid[Taxon_ID]     |  As for GPAD, will this break too many things?
7 | Parent_ObjectID ::= [ID] ('\|' ID)* .     |  Need to be clear on what is meant by 'parent'.  Also, what is meant by the pipe here?
8 | DB_Xrefs ::= [ID] ('\|' ID)*      |  Also need to be clear on what is required, e.g. MOD gene IDs xref to UniProtKB GCRP.
9 | Properties ::= [Property_Value_Pair] (',' Property_Value_Pair)*     | 

## Headers 
    
need to be standard
    
