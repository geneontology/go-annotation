# Specifications for Gene Ontology Consortium GPAD and GPI tabular formats version 2.0

This document specifies the syntax of Gene Product Annotation Data (GPAD) and Gene Product Information (GPI) formats. GPAD describes the relationships between biological entities (such as gene products) and biological descriptors (such as GO terms). GPI describes the biological entities.

## Status

This is specification has been approved as version 2.0.

## Summary of changes relative to 1.1

- GPAD and GPI: columns 1 and 2 are now combined in a single column containing an id in CURIE syntax, e.g. UniProtKB:P56704.
- GPAD: negation is captured in a separate column, column 2, using the text string 'NOT'.
- GPAD: gene product-to-term relations captured in column 3 use a Relations Ontology (RO) identifier instead of a text string.
- GPAD: the With/From column, column 7, may contain identifiers separated by commas as well as pipes.
- GPAD and GPI: NCBI taxon ids are prefixed with 'NCBITaxon:' to indicate the source of the id, e.g. NCBITaxon:6239
- GPAD: Annotation Extensions in column 11 will use a Relation_ID, rather than a Relation_Symbol, in the Relational_Expression, e.g. RO:0002233(UniProtKB:Q00362)
- GPAD and GPI: dates follow the ISO-8601 format, e.g. YYYY-MM-DD; time may be included as YYYY-MM-DDTHH:MM:SS
- GPI: the entity type in column 5 is captured using an ID from the Sequence Ontology, Protein Ontology, or Gene Ontology.
- GPI: the parent object id in column 7 refers to the gene-centric parent, e.g. the UniProtKB Gene-Centric Reference Proteome accession or a Model Organism Database gene identifier
- Characters allowed in all fields have been explicitly specified
- Extensions in file names are: *.gpad and *.gpi

## BNF Notation

GPAD and GPI document structures are defined using a BNF notation similar to [W3C specs](https://www.w3.org/TR/2004/REC-xml11-20040204/#sec-notation), which is summarized below.

 * terminal symbols are single quoted
 * non-terminal symbols are unquoted
 * zero or more symbols are indicated by following the symbol with a star; e.g. `Annotation*`
 * one or more symbols are indicated by following the symbol with a plus; e.g. `Digit+`
 * zero or one symbols are indicated by following the symbol with a question mark; e.g. `Extension_Conj?`
 * alternative symbols are written using vertical bars
 * groupings are written using parentheses

GPI and GPAD documents consist of sequences of ASCII characters.

## GPAD-GPI Full Grammar

### Document structure

| Production | Grammar | Comments |
| ------ | ------ | ------ |
| <code><a name="Doc">Doc</a></code> | <code>[GPAD_Doc](#GPAD_Doc) \| [GPI_Doc](#GPI_Doc)</code>| |
| <code><a name="GPAD_Doc">GPAD_Doc</a></code> | <code>[GPAD_Header](#GPAD_Header) [Annotation](#Annotation)*</code>| |
| <code><a name="GPI_Doc">GPI_Doc<a></code> | <code>[GPI_Header](#GPI_Header) [Entity](#Entity)*</code>| |
| <code><a name="GPAD_Header">GPAD_Header</a></code> | <code>'!gpad-version: 2.0' \n '!generated-by: ' [Prefix](#Prefix) \n '!date-generated: ' [Date_Or_Date_Time](#Date_Or_Date_Time) \n [Header_Line](#Header_Line)*</code>| Groups may include optional additional [header properties](#header-properties) |
| <code><a name="GPI_Header">GPI_Header</a></code> | <code>'!gpi-version: 2.0' \n '!generated-by: ' [Prefix](#Prefix) \n '!date-generated: ' [Date_Or_Date_Time](#Date_Or_Date_Time) \n [Header_Line](#Header_Line)*</code>| Groups may include optional additional [header properties](#header-properties) |
| <code><a name="Annotation">Annotation</a></code> | <code>[DB_Object_ID](#DB_Object_ID) \t [Negation](#Negation) \t [Relation](#Relation) \t [Ontology_Class_ID](#Ontology_Class_ID) \t [Reference](#Reference) \t [Evidence_Type](#Evidence_Type) \t [With_Or_From](#With_Or_From) \t [Interacting_Taxon_ID](#Interacting_Taxon_ID) \t [Annotation_Date](#Annotation_Date) \t [Assigned_By](#Assigned_By) \t [Annotation_Extensions](#Annotation_Extensions) \t [Annotation_Properties](#Annotation_Properties) \n</code>| |
| <code><a name="Entity">Entity</a></code> | <code>[DB_Object_ID](#DB_Object_ID) \t [DB_Object_Symbol](#DB_Object_Symbol) \t [DB_Object_Name](#DB_Object_Name) \t [DB_Object_Synonyms](#DB_Object_Synonyms) \t [DB_Object_Type](#DB_Object_Type) \t [DB_Object_Taxon](#DB_Object_Taxon) \t [Encoded_By](#Encoded_By) \t [Parent_Protein](#Parent_Protein) \t [Protein_Containing_Complex_Members](#Protein_Containing_Complex_Members) \t [DB_Xrefs](#DB_Xrefs) [Gene_Product_Properties](#Gene_Product_Properties) \n</code>| |

### Header properties

In addition to the three required header properties specified in the grammars for [GPAD](#GPAD_Header) and [GPI](#GPI_Header), groups may decide to include optional
additional information in [header lines](#Header_Line), either [unstructured](#Unstructured_Value_Header) or using custom [header properties](#Tag_Value_Header). Examples include:

Header property | Example value | Comment 
-----------------------|---------------|--------|
`url` | `http://www.yeastgenome.org/` | 
`project-release` | `WS275` |
`funding` | `NHGRI` |
`columns` | file format written out |
`go-version` | `http://purl.obolibrary.org/obo/go/releases/2023-10-09/go.owl` |
`ro-version` | `http://purl.obolibrary.org/obo/ro/releases/2023-08-18/ro.owl` |

### GPAD columns

| Column | Production | Grammar | Example | Comments |
| ------ | ------ | ------ | ------ | ------ |
| 1 | <code><a name="DB_Object_ID">DB_Object_ID</a></code> | <code>[ID](#ID)</code>| `UniProtKB:P11678` | |
| 2 | <code><a name="Negation">Negation</a></code> | <code>'NOT'?</code>| `NOT` | |
| 3 | <code><a name="Relation">Relation</a></code> | <code>[ID](#ID)</code>| `RO:0002263` | The relation used MUST come from the [allowed gene-product-to-term relations](#allowed-gene-product-to-go-term-relations) |
| 4 | <code><a name="Ontology_Class_ID">Ontology_Class_ID</a></code> | <code>[ID](#ID)</code>| `GO:0050803` | The identifier MUST be a term from the GO ontology |
| 5 | <code><a name="Reference">Reference</a></code> | <code>[ID](#ID) ( '\|' [ID](#ID) )*</code>| `PMID:30695063` | Different IDs, e.g. PMID and MOD paper ID, MUST correspond to the same publication or reference |
| 6 | <code><a name="Evidence_Type">Evidence_Type</a></code> | <code>[ID](#ID)</code>| `ECO:0000315` | The evidence identifier MUST be a term from the ECO ontology. Mapping file in progress: https://github.com/evidenceontology/evidenceontology#249 |
| 7 | <code><a name="With_Or_From">With_Or_From</a></code> | <code>( [ID](#ID) ( [\|,] [ID](#ID) )* )?</code>| `WB:WBVar00000510` | Pipe-separated entries represent independent evidence; comma-separated entries represent grouped evidence, e.g. two of three genes in a triply mutant organism |
| 8 | <code><a name="Interacting_Taxon_ID">Interacting_Taxon_ID</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| `NCBITaxon:5476` | The taxon MUST be a term from the NCBITaxon ontology |
| 9 | <code><a name="Annotation_Date">Annotation_Date</a></code> | <code>[Date_Or_Date_Time](#Date_Or_Date_Time)</code>| `2019-01-30` | |
| 10 | <code><a name="Assigned_By">Assigned_By</a></code> | <code>[Prefix](#Prefix)</code>| `MGI` | |
| 11 | <code><a name="Annotation_Extensions">Annotation_Extensions</a></code> | <code>( [Extension_Conj](#Extension_Conj) ( '\|' [Extension_Conj](#Extension_Conj) )* )?</code>| `BFO:0000066(GO:0005829)` | |
| 12 | <code><a name="Annotation_Properties">Annotation_Properties</a></code> | <code>( [Property_Value_Pair](#Property_Value_Pair) ( '\|' [Property_Value_Pair](#Property_Value_Pair) )* )?</code>| `contributor-id=orcid:0000-0002-1478-7671` | Properties and values MUST come conform to the list in [GPAD annotation properties](#gpad-annotation-properties) |

### GPI columns

| Column | Production | Grammar | Example | Comments |
| ------ | ------ | ------ | ------ | ------ |
| 1 | <code><a name="DB_Object_ID">DB_Object_ID</a></code> | <code>[ID](#ID)</code>| `UniProtKB:Q4VCS5` | |
| 2 | <code><a name="DB_Object_Symbol">DB_Object_Symbol</a></code> | <code>[Text_No_Spaces](#Text_No_Spaces)</code>| `AMOT` | |
| 3 | <code><a name="DB_Object_Name">DB_Object_Name</a></code> | <code>[Text](#Text)</code>| `Angiomotin` | |
| 4 | <code><a name="DB_Object_Synonyms">DB_Object_Synonyms</a></code> | <code>([Text](#Text) ( '\|' [Text](#Text) )* )?</code>| `E230009N18Rik\|KIAA1071` | |
| 5 | <code><a name="DB_Object_Type">DB_Object_Type</a></code> | <code>[ID](#ID) ( '\|' [ID](#ID) )*</code>| `PR:000000001` | Identifier used MUST conform to the list in [GPI entity types](#gpi-entity-types) |
| 6 | <code><a name="DB_Object_Taxon">DB_Object_Taxon</a></code> | <code>[ID](#ID)</code>| `NCBITaxon:9606` | The taxon MUST be a term from the NCBITaxon ontology |
| 7 | <code><a name="Encoded_By">Encoded_By</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| `HGNC:17810` | For proteins and transcripts, this refers to the gene id that encodes those entities. |
| 8 | <code><a name="Parent_Protein">Parent_Protein</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| | When column 1 refers to a protein isoform or modified protein, this column refers to the gene-centric reference protein accession of the column 1 entry. |
| 9 | <code><a name="Protein_Containing_Complex_Members">Protein_Containing_Complex_Members</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| `UniProtKB:Q15021\|UniProtKB:Q15003` | |
| 10 | <code><a name="DB_Xrefs">DB_Xrefs</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| `HGNC:17810` | Identifiers used MUST include the [required DB xref values](#required-and-optional-db-xrefs) |
| 11 | <code><a name="Gene_Product_Properties">Gene_Product_Properties</a></code> | <code>( [Property_Value_Pair](#Property_Value_Pair) ( '\|' [Property_Value_Pair](#Property_Value_Pair) )* )?</code>| `db-subset=Swiss-Prot` | Properties and values MUST conform to the list in [GPI gene product properties](#gpi-gene-product-properties) |

### Values

| Production | Grammar | Comments |
| ------ | ------ | ------ |
| <code><a name="Header_Line">Header_Line</a></code> | <code>( [Tag_Value_Header](#Tag_Value_Header) \| [Unstructured_Value_Header](#Unstructured_Value_Header) ) \n</code>| |
| <code><a name="Tag_Value_Header">Tag_Value_Header</a></code> | <code>'!' [Property](#Property) ':' [Space](#Space)* [Header_Value](#Header_Value)</code>| |
| <code><a name="Unstructured_Value_Header">Unstructured_Value_Header</a></code> | <code>'!!' [Header_Value](#Header_Value)</code>| |
| <code><a name="Header_Value">Header_Value</a></code> | <code>[Text](#Text)</code>| |
| <code><a name="Extension_Conj">Extension_Conj</a></code> | <code>[Relational_Expression](#Relational_Expression) ( ',' [Relational_Expression](Relational_Expression) )*</code>| |
| <code><a name="Relational_Expression">Relational_Expression</a></code> | <code>[Relation_ID](#Relation_ID) '(' [Target_ID](#Target_ID) ')'</code>| |
| <code><a name="Relation_ID">Relation_ID</a></code> | <code>[ID](#ID)</code>| The identifier MUST be a term in the OBO relations ontology |
| <code><a name="Target_ID">Target_ID</a></code> | <code>[ID](#ID)</code>| |
| <code><a name="Property_Value_Pair">Property_Value_Pair</a></code> | <code>[Property](#Property) '=' [Property_Value](#Property_Value)</code>| |
| <code><a name="Property">Property</a></code> | <code>([Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| '-')+</code>| |
| <code><a name="Property_Value">Property_Value</a></code> | <code>[Text](#Text)</code>| |
| <code><a name="ID">ID</a></code> | <code>[Prefix](#Prefix) ':' [Local_ID](#Local_ID)</code>| |
| <code><a name="Prefix">Prefix</a></code> | <code>[Alpha_Char](#Alpha_Char) [ID_Char](#ID_Char)*</code>| The [GO database registry](https://github.com/geneontology/go-site/blob/master/metadata/db-xrefs.yaml) contains a list of valid prefixes that can be used in GPAD or GPI files. Every identifier prefix used in a GPAD or GPI file MUST have an entry in the registry. |
| <code><a name="Local_ID">Local_ID</a></code> | <code>( [ID_Char](#ID_Char) \| ':' )+</code>| |
| <code><a name="ID_Char">ID_Char</a></code> | <code>[Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| '_' \| '-' \| '.'</code>| |
| <code><a name="Date_Or_Date_Time">Date_Or_Date_Time</a></code> | <code>[Date](#Date) \| [Date_Time](#Date_Time)</code>| |
| <code><a name="Date">Date</a></code> | <code>YYYY-MM-DD</code>| Corresponds to [xsd:date](https://www.w3.org/TR/xmlschema-2/#date) without optional timezone (a subset of the ISO 8601 standard) |
| <code><a name="Date_Time">Date_Time</a></code> | <code>YYYY-MM-DDTHH:MM:SS('.' s+)?((('+' \| '-') hh ':' mm) \| 'Z')?</code>| Corresponds to [xsd:dateTime](https://www.w3.org/TR/xmlschema-2/#dateTime) (a subset of the ISO 8601 standard) |
| <code><a name="Text">Text</a></code> | <code>[Text_Char](#Text_Char)+</code>| |
| <code><a name="Text_No_Spaces">Text_No_Spaces</a></code> | <code>[Nonspace_Text_Char](#Nonspace_Text_Char)+</code>| |
| <code><a name="Text_Char">Text_Char</a></code> | <code>[Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| [Symbol_Char](#Symbol_Char) \| [Space](#Space)</code>| |
| <code><a name="Nonspace_Text_Char">Nonspace_Text_Char</a></code> | <code>[Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| [Symbol_Char](#Symbol_Char)</code>| |
| <code><a name="Alpha_Char">Alpha_Char</a></code> | <code>[A-Z] \| [a-z]</code>| |
| <code><a name="Digit">Digit</a></code> | <code>[0-9]</code>| |
| <code><a name="Symbol_Char">Symbol_Char</a></code> | <code>'!' \| '"' \| '#' \| '$' \| '%' \| '&' \| ''' \| '(' \| ')' \| '*' \| '+' \| ',' \| '-' \| '.' \| '/' \| ':' \| ';' \| '<' \| '=' \| '>' \| '?' \| '@' \| '[' \| '\\' \| ']' \| '^' \| '_' \| '`' \| '{' \| '}' \| '~'</code>| ASCII symbols minus `\|` |
| <code><a name="Space">Space</a></code> | <code>' '</code>| |

### Allowed Gene Product to GO Term Relations

Default usage is indicated for MF and CC.  Groups may choose which relation to use for BP annotations according to their curation practice.  'acts upstream of or within' is the parent Relations Ontology term for the BP relations listed below.  A full view of the BP relation hierarchy can be found at http://www.ontobee.org/ or https://www.ebi.ac.uk/ols/index. Note: the RO term labels and IDs listed below are current as of 2020-06-09.  However, to ensure accurate use of RO, groups should always derive mappings between RO term labels and IDs from the RO source file available here: https://github.com/oborel/obo-relations

GO Aspect 	| Relations Ontology Label  | Relations Ontology ID | Usage Guidelines
-----------|---------------------------|----------------------| ------------------ |
Molecular Function | enables | `RO:0002327` | Default for MF
Molecular Function | contributes to | `RO:0002326` |
Biological Process | involved in | `RO:0002331` |
Biological Process | acts upstream of | `RO:0002263` |
Biological Process | acts upstream of positive effect | `RO:0004034` |
Biological Process | acts upstream of negative effect | `RO:0004035` |
Biological Process | acts upstream of or within | `RO:0002264` | Default for BP (GO:0008150) and child terms
Biological Process | acts upstream of or within positive effect | `RO:0004032` |
Biological Process | acts upstream of or within negative effect | `RO:0004033` |
Cellular Component | part of	| `BFO:0000050` | Default for protein-containing complex (GO:0032991) and child terms
Cellular Component | located in | `RO:0001025` | Default for non-protein-containing complex CC terms
Cellular Component | is active in | `RO:0002432` | Used to indicate where a gene product enables its MF
Cellular Component | colocalizes with | `RO:0002325` |

### GPAD Annotation Properties

All properties are single valued as shown.

Property | Allowed usages per annotation | Value Grammar | Example | Comment 
---------------------------|----------------|------------ | ------- | --------- |
`'id'` | 0 or 1 | <code>[ID](#ID)</code> | `id=WBOA:3219` | Unique identifier for an annotation in a contributing database. |
`'model-state'` | 0 or 1 | <code>[Alpha_Char](#Alpha_Char)+</code> | `model-state=production` | GO-CAM model state |
`'noctua-model-id'` | 0 or 1 | <code>[ID](#ID)</code> | `noctua-model-id=gomodel:5a7e68a100001078` | Unique GO-CAM model id |
`'contributor-id'` | 0 or more | <code>[ID](#ID)</code> | `contributor-id=orcid:0000-0002-1706-4196` | Identifier for curator or user who entered or changed an annotation. Prefix MUST be `orcid` or `goc` |
`'reviewer-id'` | 0 or more | <code>[ID](#ID)</code> | `reviewer-id=orcid:0000-0001-7476-6306` | Identifier for curator or user who last reviewed an annotation. Prefix MUST be `orcid` or `goc` |
`'creation-date'` | 0 or 1 | <code>[Date_Or_Date_Time](#Date_Or_Date_Time)</code> | `creation-date=2019-02-05` | The date on which the annotation was created. |
`'modification-date'` | 0 or more | <code>[Date_Or_Date_Time](#Date_Or_Date_Time)</code> | `modification-date=2019-02-06` | The date(s) on which an annotation was modified. |
`'reviewed-date'` | 0 or more | <code>[Date_Or_Date_Time](#Date_Or_Date_Time)</code> | `reviewed-date=2019-02-06` | The date(s) on which the annotation was reviewed. |
`'comment'` | 0 or more | <code>[Text](#Text)</code> | `comment=Confirmed species by checking PMID:nnnnnnnn.` | Free-text field that allows curators or users to enter notes about a specific annotation. |

### GPI Entity Types 

Entity types may be one of the following, or a more granular child term. The value should be provided as an ontology term identifier.

Entity Type | Ontology Label | Ontology ID 
---------------------------|----------------|------------ | 
protein-coding gene | protein_coding_gene | `SO:0001217`
ncRNA-coding gene | ncRNA_gene  | `SO:0001263` 
mRNA | mRNA | `SO:0000234`
ncRNA | ncRNA | `SO:0000655` 
protein | protein | `PR:000000001`
protein-containing complex | protein-containing complex | `GO:0032991`
marker or uncloned locus | genetic_marker | `SO:0001645`

Other possible entity types from MGI (additional examples coming):
- gene segment: `SO:3000000`
- pseudogene: `SO:0000336`
  - Example: http://www.informatics.jax.org/marker/MGI:3029152
- gene: `SO:0000704`
- biological region: `SO:0001411`


### Required and Optional DB xrefs
#### Required:

 - **MODs:** Must associate gene ids, for protein-coding genes, with UniProtKB gene-centric reference protein accessions
 - **UniProtKB:** Must associate gene-centric reference protein accessions with MOD gene ids

#### Optional DB xref suggestions (where applicable):

- RNAcentral 
- Ensembl gene
- NCBI RefSeq gene
- HGNC
- ComplexPortal
- PRO

### GPI Gene Product Properties

Property | Allowed usages per annotation | Value Grammar | Example | Comment 
---------------------------|----------------|------------ | ------- | --------- |
`'db-subset'` | 0 or 1 | <code>'TrEMBL' \| 'Swiss-Prot'</code> | `db-subset=TrEMBL` | The status of a UniProtKB accession with respect to curator review.
`'uniprot-proteome'` | 0 or 1 | <code>[ID](#ID)</code> | `uniprot-proteome=UP000001940` | A unique UniProtKB identifier for the set of proteins that constitute an organism's proteome.
`'go-annotation-complete'` | 0 or 1 | <code>[Date_Or_Date_Time](#Date_Or_Date_Time)</code> | `2019-02-05` | Indicates the date on which a curator determined that the set of GO annotations for a given entity is complete with respect to GO annotation.  Complete means that all information about a gene has been captured as a GO term, but not necessarily that all possible supporting evidence is annotated.
`'go-annotation-summary'` | 0 or 1 | <code>[Text](#Text)</code> | `go-annotation-summary=Sterol binding protein with a role in intracellular sterol transport; localizes to mitochondria and the cortical ER` | A textual gene or gene product description.
