
# Proposed specifications for Gene Ontology Consortium GPAD and GPI tabular formats version 2.0

## BNF Notation

GPAD and GPI document structures are defined using a BNF notation similar to [W3C specs](https://www.w3.org/TR/2004/REC-xml11-20040204/#sec-notation), which is summarized below.

 * terminal symbols are single quoted
 * non-terminal symbols are unquoted
 * zero or more symbols are indicated by following the symbol with a star; e.g. `Annotation*`
 * one or more symbols are indicated by following the symbol with a plus; e.g. `Digit+`
 * zero or one symbols are indicated by following the symbol with a question mark; e.g. `Extension_Conj?`
 * alternative symbols are written using vertical bars
 * groupings are written using parentheses
 * complementation is written using minus symbol

GPI and GPAD documents consist of sequences of ASCII characters.

## GPAD-GPI Full Grammar

### Document structure

| | Grammar | Comments |
| ------ | ------ | ------ |
| <code><a name="Doc">Doc</a></code> | <code>[GPAD_Doc](#GPAD_Doc) \| [GPI_Doc](#GPI_Doc)</code>| |
| <code><a name="GPAD_Doc">GPAD_Doc</a></code> | <code>[GPAD_Header](#GPAD_Header) [Annotation](#Annotation)*</code>| |
| <code><a name="GPI_Doc">GPI_Doc<a></code> | <code>[GPI_Header](#GPI_Header) [Entity](#Entity)*</code>| |
| <code><a name="GPAD_Header">GPAD_Header</a></code> | <code>'!gpa-version: 2.0' \n [Header_Line](#Header_Line)*</code>| |
| <code><a name="GPI_Header">GPI_Header</a></code> | <code>'!gpi-version: 2.0' \n [Header_Line](#Header_Line)*</code>| |
| <code><a name="Annotation">Annotation</a></code> | <code>[DB_Object_ID](#DB_Object_ID) \t [Negation](#Negation) \t [Relation](#Relation) \t [Ontology_Class_ID](#Ontology_Class_ID) \t [Reference](#Reference) \t [Evidence_Type](#Evidence_Type) \t [With_Or_From](#With_Or_From) \t [Interacting_Taxon_ID](#Interacting_Taxon_ID) \t [Annotation_Date](#Annotation_Date) \t [Assigned_By](#Assigned_By) \t [Annotation_Extensions](#Annotation_Extensions) \t [Annotation_Properties](#Annotation_Properties) \n</code>| |
| <code><a name="Entity">Entity</a></code> | <code>[DB_Object_ID](#DB_Object_ID) \t [DB_Object_Symbol](#DB_Object_Symbol) \t [DB_Object_Name](#DB_Object_Name) \t [DB_Object_Synonyms](#DB_Object_Synonyms) \t [DB_Object_Type](#DB_Object_Type) \t [DB_Object_Taxon](#DB_Object_Taxon) \t [Encoded_By](#Encoded_By) \t [Parent_Protein](#Parent_Protein) \t [Protein_Containing_Complex_Members](#Protein_Containing_Complex_Members) \t [DB_Xrefs](#DB_Xrefs) [Gene_Product_Properties](#Gene_Product_Properties) \n</code>| |

### GPAD columns

| Column | | Grammar | Example | Comments |
| ------ | ------ | ------ | ------ | ------ |
| 1 | <code><a name="DB_Object_ID">DB_Object_ID</a></code> | <code>[ID](#ID)</code>| UniProtKB:P11678 | |
| 2 | <code><a name="Negation">Negation</a></code> | <code>'NOT'?</code>| NOT | |
| 3 | <code><a name="Relation">Relation</a></code> | <code>[ID](#ID)</code>| RO:0002263 | The relation used MUST come from the [allowed gene-product-to-term relations](#allowed-gene-product-to-go-term-relations) |
| 4 | <code><a name="Ontology_Class_ID">Ontology_Class_ID</a></code> | <code>[ID](#ID)</code>| GO:0050803 | The identifier MUST be a term from the GO ontology |
| 5 | <code><a name="Reference">Reference</a></code> | <code>[ID](#ID) ( '\|' [ID](#ID) )*</code>| PMID:30695063 | Different IDs, e.g. PMID and MOD paper ID, MUST correspond to the same publication or reference |
| 6 | <code><a name="Evidence_Type">Evidence_Type</a></code> | <code>[ID](#ID)</code>| ECO:0000315 | The evidence identifier MUST be a term from the ECO ontology. Mapping file in progress: https://github.com/evidenceontology/evidenceontology#249 |
| 7 | <code><a name="With_Or_From">With_Or_From</a></code> | <code>( [ID](#ID) ( [\|,] [ID](#ID) )* )?</code>| WB:WBVar00000510 | Pipe-separated entries represent independent evidence; comma-separated entries represent grouped evidence, e.g. two of three genes in a triply mutant organism |
| 8 | <code><a name="Interacting_Taxon_ID">Interacting_Taxon_ID</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| NCBITaxon:5476 | The taxon MUST be a term from the NCBITaxon ontology |
| 9 | <code><a name="Annotation_Date">Annotation_Date</a></code> | <code>[Date_Or_Date_Time](#Date_Or_Date_Time)</code>| 2019-01-30 | |
| 10 | <code><a name="Assigned_By">Assigned_By</a></code> | <code>[Prefix](#Prefix)</code>| MGI | |
| 11 | <code><a name="Annotation_Extensions">Annotation_Extensions</a></code> | <code>( [Extension_Conj](#Extension_Conj) ( '\|' [Extension_Conj](#Extension_Conj) )* )?</code>| BFO:0000066(GO:0005829) | |
| 12 | <code><a name="Annotation_Properties">Annotation_Properties</a></code> | <code>( [Property_Value_Pair](#Property_Value_Pair) ( '\|' [Property_Value_Pair](#Property_Value_Pair) )* )?</code>| contributor-id=orcid:0000-0002-1478-7671 | Properties and values MUST come conform to the list in [GPAD annotation properties](#gpad-annotation-properties) |

### GPI columns

| Column | | Grammar | Example | Comments | Observed characters |
| ------ | ------ | ------ | ------ | ------ | ------ |
| 1 | <code><a name="DB_Object_ID">DB_Object_ID</a></code> | <code>[ID](#ID)</code>| UniProtKB:Q4VCS5 | | |
| 2 | <code><a name="DB_Object_Symbol">DB_Object_Symbol</a></code> | <code>[Text_No_Spaces](#Text_No_Spaces)</code>| AMOT | | [Alpha_Char](#Alpha_Char) [Digit](#Digit) [Space](#Space) `#&'()*+,-./:;<>?[\]_\|`  |
| 3 | <code><a name="DB_Object_Name">DB_Object_Name</a></code> | <code>[Text](#Text)</code>| Angiomotin | CHECK | [Alpha_Char](#Alpha_Char) [Digit](#Digit) [Space](#Space) ``#%&'()*+,-./:;<=>?@[\]_`ä\|`` |
| 4 | <code><a name="DB_Object_Synonyms">DB_Object_Synonyms</a></code> | <code>([Text](#Text) ( '\|' [Text](#Text) )* )?</code>| AMOT\|KIAA1071 | | [Alpha_Char](#Alpha_Char) [Digit](#Digit) [Space](#Space) `"#%&'()*+,-./:;<=>?@[]_àäéö~βγδ–` |
| 5 | <code><a name="DB_Object_Type">DB_Object_Type</a></code> | <code>[ID](#ID) ( '\|' [ID](#ID) )*</code>| PR:000000001 | Sequence Ontology OR Protein Ontology OR Gene Ontology | |
| 6 | <code><a name="DB_Object_Taxon">DB_Object_Taxon</a></code> | <code>[ID](#ID)</code>| NCBITaxon:9606 | The taxon MUST be a term from the NCBITaxon ontology | |
| 7 | <code><a name="Encoded_By">Encoded_By</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| HGNC:17810 | For proteins and transcripts, this refers to the gene id that encodes those entities. | |
| 8 | <code><a name="Parent_Protein">Parent_Protein</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| | When column 1 refers to a protein isoform or modified protein, this column refers to the gene-centric reference protein accession of the column 1 entry. | |
| 9 | <code><a name="Protein_Containing_Complex_Members">Protein_Containing_Complex_Members</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| UniProtKB:Q15021\|UniProtKB:Q15003 | | |
| 10 | <code><a name="DB_Xrefs">DB_Xrefs</a></code> | <code>( [ID](#ID) ( '\|' [ID](#ID) )* )?</code>| HGNC:17810 | See below for required DB xref values | |
| 11 | <code><a name="Gene_Product_Properties">Gene_Product_Properties</a></code> | <code>( [Property_Value_Pair](#Property_Value_Pair) ( '\|' [Property_Value_Pair](#Property_Value_Pair) )* )?</code>| db-subset=Swiss-Prot | Properties and values MUST conform to the list in [GPI gene product properties](#gpi-gene-product-properties) | |

### Values

| | Grammar | Comments |
| ------ | ------ | ------ |
| <code><a name="Header_Line">Header_Line</a></code> | <code>( [Tag_Value_Header](#Tag_Value_Header) \| [Unstructured_Value_Header](#Unstructured_Value_Header) ) \n</code>| |
| <code><a name="Tag_Value_Header">Tag_Value_Header</a></code> | <code>'!' [Property](#Property) ':' [Space](#Space)* [Header_Value](#Header_Value)</code>| |
| <code><a name="Unstructured_Value_Header">Unstructured_Value_Header</a></code> | <code>'!!' [Header_Value](#Header_Value)</code>| |
| <code><a name="Header_Value">Header_Value</a></code> | <code>[Text](#Text)</code>| |
| <code><a name="Extension_Conj">Extension_Conj</a></code> | <code>[Relational_Expression](#Relational_Expression) ( ',' [Relational_Expression](Relational_Expression) )*</code>| |
| <code><a name="Relational_Expression">Relational_Expression</a></code> | <code>[Relation_ID](#Relation_ID) '(' [Target_ID](#Target_ID) ')'</code>| |
| <code><a name="Relation_ID">Relation_ID</a></code> | <code>[ID](#ID)</code>| |
| <code><a name="Target_ID">Target_ID</a></code> | <code>[ID](#ID)</code>| |
| <code><a name="Property_Value_Pair">Property_Value_Pair</a></code> | <code>[Property](#Property) '=' [Property_Value](#Property_Value)</code>| |
| <code><a name="Property">Property</a></code> | <code>([Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| '-')+</code>| |
| <code><a name="Property_Value">Property_Value</a></code> | <code>[Text](#Text)</code>| |
| <code><a name="ID">ID</a></code> | <code>[Prefix](#Prefix) ':' [Local_ID](#Local_ID)</code>| |
| <code><a name="Prefix">Prefix</a></code> | <code>[Alpha_Char](#Alpha_Char) [ID_Char](#ID_Char)*</code>| |
| <code><a name="Local_ID">Local_ID</a></code> | <code>( [ID_Char](#ID_Char) \| ':' )+</code>| |
| <code><a name="ID_Char">ID_Char</a></code> | <code>[Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| '_' \| '-' \| '.'</code>| |
| <code><a name="Date_Or_Date_Time">Date_Or_Date_Time</a></code> | <code>[Date](#Date) \| [Date_Time](#Date_Time)</code>| |
| <code><a name="Date">Date</a></code> | <code>YYYY-MM-DD</code>| Corresponds to [xsd:date](https://www.w3.org/TR/xmlschema-2/#date) without optional timezone |
| <code><a name="Date_Time">Date_Time</a></code> | <code>YYYY-MM-DDTHH:MM:SS('.' s+)?((('+' \| '-') hh ':' mm) \| 'Z')?</code>| Corresponds to [xsd:dateTime](https://www.w3.org/TR/xmlschema-2/#dateTime) |
| <code><a name="Text">Text</a></code> | <code>[Text_Char](#Text_Char)+</code>| |
| <code><a name="Text_No_Spaces">Text_No_Spaces</a></code> | <code>( [Text_Char](#Text_Char) - [Space](#Space) )+</code>| |
| <code><a name="Text_Char">Text_Char</a></code> | <code>[Alpha_Char](#Alpha_Char) \| [Digit](#Digit) \| [Symbol_Char](#Symbol_Char) \| [Space](#Space)</code>| |
| <code><a name="Alpha_Char">Alpha_Char</a></code> | <code>[A-Z] \| [a-z]</code>| |
| <code><a name="Digit">Digit</a></code> | <code>[0-9]</code>| |
| <code><a name="Symbol_Char">Symbol_Char</a></code> | <code>'!' \| '"' \| '#' \| '$' \| '%' \| '&' \| ''' \| '(' \| ')' \| '*' \| '+' \| ',' \| '-' \| '.' \| '/' \| ':' \| ';' \| '<' \| '=' \| '>' \| '?' \| '@' \| '[' \| '\\' \| ']' \| '^' \| '_' \| '`' \| '{' \| '}' \| '~'</code>| |
| <code><a name="Space">Space</a></code> | <code>' '</code>| |

### Allowed Gene Product to GO Term Relations

#### Default usage is indicated for MF and CC.  Groups may choose which relation to use for BP annotations according to their curation practice.  'acts upstream of or within' is the parent Relations Ontology term for the BP relations listed below.  A full view of the BP relation hierarchy can be found at http://www.ontobee.org/ or https://www.ebi.ac.uk/ols/index. Note: the RO term labels and IDs listed below are current as of 2020-06-09.  However, to ensure accurate use of RO, groups should always derive mappings between RO term labels and IDs from the RO source file available here: https://github.com/oborel/obo-relations


GO Aspect 	| Relations Ontology Label  | Relations Ontology ID | Usage Guidelines
-----------|---------------------------|----------------------| ------------------ |
Molecular Function | enables | RO:0002327 | Default for MF
Molecular Function | contributes to | RO:0002326 |
Biological Process | involved in | RO:0002331 |
Biological Process | acts upstream of | RO:0002263 |
Biological Process | acts upstream of positive effect | RO:0004034 |
Biological Process | acts upstream of negative effect | RO:0004035 |
Biological Process | acts upstream of or within | RO:0002264 | Default for BP (GO:0008150) and child terms
Biological Process | acts upstream of or within positive effect | RO:0004032 |
Biological Process | acts upstream of or within negative effect | RO:0004033 |
Cellular Component | part of	| BFO:0000050 | Default for protein-containing complex (GO:0032991) and child terms
Cellular Component | located in | RO:0001025 | Default for non-protein-containing complex CC terms
Cellular Component | is active in | RO:0002432 | Used to indicate where a gene product enables its MF
Cellular Component | colocalizes with | RO:0002325 |

### GPAD Annotation Properties
All properties are single valued as shown.

Annotation_Property_Symbol | Property must be unique | Property_Value | Example | Semantics 
---------------------------|----------------|------------ | ------- | --------- |
 id | True | unique database identifier | id=WBOA:3219 | Unique identifier for an annotation in a contributing database. |
 model-state | True | GO-CAM model state | model-state=production |
 noctua-model-id | True | unique GO-CAM model id | noctua-model-id=gomodel:5a7e68a100001078 |
 contributor-id | False | ORCID | contributor-id=https://orcid.org/0000-0002-1706-4196 | Used by GOC to indicate ORCID of curator or user who entered or changed an annotation |
 reviewer-id | False | ORCID | reviewer-id=https://orcid.org/0000-0001-7476-6306 | Used by GOC to indicate ORCID of curator or user who last reviewed an annotation |
 creation-date | True | YYYY-MM-DD | creation-date=2019-02-05 | The date on which the annotation was created. |
 modification-date | False | YYYY-MM-DD | modification-date=2019-02-06 | The date(s) on which an annotation was modified. |
 reviewed-date | False | YYYY-MM-DD | reviewed-date=2019-02-06 | The date(s) on which the annotation was reviewed. |
 comment | False | text | comment=Confirmed species by checking PMID:nnnnnnnn. | Free-text field that allows curators or users to enter notes about a specific annotation. |

### GPI Entity Types 
#### Entity types may be one of the following, or a more granular child term.

Entity Type | Ontology Label | Ontology ID 
---------------------------|----------------|------------ | 
protein-coding gene | protein_coding_gene | SO:0001217 
ncRNA-coding gene | ncRNA_gene  | SO:0001263 
mRNA | mRNA | SO:0000234
ncRNA | ncRNA | SO:0000655 
protein | protein | PR:000000001
protein-containing complex | protein-containing complex | GO:0032991
marker or uncloned locus | genetic_marker | SO:0001645

Other possible entity types from MGI (additional examples coming):

 *gene segment: SO:3000000
 
 *pseudogene: SO:0000336
 
 *Example: http://www.informatics.jax.org/marker/MGI:3029152
 
 *gene: SO:0000704
 
 *biological region: SO:0001411


### Required and Optional DB xrefs
#### Required:

 MODs: Must associate gene ids, for protein-coding genes, with UniProtKB gene-centric reference protein accessions
 
 UniProtKB: Must associate gene-centric reference protein accessions with MOD gene ids

#### Optional DB xref suggestions (where applicable):

 *RNAcentral 
 
 *Ensembl gene
 
 *NCBI RefSeq gene
 
 *HGNC
 
 *ComplexPortal
 
 *PRO

### GPI Gene Product Properties

Annotation_Property_Symbol | Property_Value | Cardinality (if used) | Example | Semantics 
---------------------------|----------------|------------ | ------- | --------- |
db-subset | TrEMBL or Swiss-Prot | 1 | db-subset=TrEMBL | The status of a UniProtKB accession with respect to curator review.
uniprot-proteome | identifier  | 1 | uniprot-proteome=UP000001940 | A unique UniProtKB identifier for the set of proteins that constitute an organism's proteome.
go-annotation-complete | YYYY-MM-DD | 1| 2019-02-05 | Indicates the date on which a curator determined that the set of GO annotations for a given entity is complete with respect to GO annotation.  Complete means that all information about a gene has been captured as a GO term, but not necessarily that all possible supporting evidence is annotated.
go-annotation-summary | text | 1 | go-annotation-summary=Sterol binding protein with a role in intracellular sterol transport; localizes to mitochondria and the cortical ER | A textual gene or gene product description.
