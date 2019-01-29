# GPAD 2.0 Specs 
## Abstract
This document specifies the syntax of Gene Product Annotation Data (GPAD) and Gene Product Information (GPI) formats. GPAD describes the relationships between biological entities (such as gene products) and biological descriptors (such as GO terms). GPI describes the biological entities.
## Status
This is a working draft, that will be for comment by the community.

Date: 2019-01-29 (GoogleDoc from Montreal 2019)

Comments should be sent to go-discuss@geneontology.org

## GPAD Columns

 Each of these columns has its own syntax, as specified below:
1. ID ::= DB Prefix ':' Local_ID    
2. Negation ::= 'NOT' | ''
3. Relations ::= OBO_ID 
4. Ontology_Class_ID ::= OBO_ID
5. References ::= Reference 
6. Evidence_type ::= OBO_ID
7. With_or_From ::= [ID] ('|' | ‘,’ ID)*
8. Interacting_taxon_ID ::= NCBI:txid[Taxon_ID]
9. Date ::= YYYYMMDD
10. Assigned_by ::= DB Prefix
11. Annotation_Extensions ::= [Extension_Conj] ('|' Extension_Conj)*

    Extension_Conj ::= [Relational_Expression] (',' Relational_Expression)*
    
    Relational_Expression ::= Relation_ID '(' ID ')'
12. Annotation_Properties ::= [Property_Value_Pair] ('|' Property_Value_Pair)*

    Property_Value_Pair ::= Property_Symbol '=' Property_Value

    Property_Value  ::= (AnyChar - ('=' | '|' | nl))
    
## Headers 
    
need to be standard
    
# GPI 2.0 Specs 
## Columns

1. ID ::= DB Prefix ':' Local_ID 
2. DB_Object_Symbol ::= xxxx
3. DB_Object_Name ::= xxxx
4. DB_Object_Synonyms ::= [Label] ('|' Label)*
5. DB_Object_Type ::= OBO_ID
6. DB_Object_Taxon ::= NCBI:txid[Taxon_ID]
7. Parent_ObjectID ::= [ID??] ('|' ID)*
8. DB_Xrefs ::= [ID??] ('|' ID)*
9. Properties ::= [Property_Value] (',' Property_Value)*

## Headers 
    
need to be standard
    
