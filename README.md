# venomx - Vector Embedding Named Object Model indeX

VENOMX is an exchange standard for vector embeddings, layered on existing vector storage standards,
with the goal of sharing vector embeddings for named entities (books, genes, publications, anything
in schema.org, ...).

One of the goals is to support an **Embedding Hub**, potentially layered on existing dataset
repositories (e.g. huggingface, zenodo, figshare, ...).

# Why?

Why have a standard for embeddings? We have CSVs and Parquet and arrow, what else do we need?

Let's say Barb has made vector embeddings of all of Wikidata using OpenAI `text-embedding-ada-002`,
and distributes them (e.g. on HuggingFace), and Alice downloads from here.

Two months later, Alice wants to use this for RAG querying. But she has
forgotten what model was used, and also what version of Wikidata was used. She also doesn't remember
what exactly was indexed. Was it the page titles? The descriptions? Or the full Wikipedia text?

Multiply this by multiple datasets, versions, indexing strategies, subsets, and chaos ensues.

The goal of venomx is to provide:

- a simple YAML format for metadata about an embeddings set
- a super-simple parquet schema for the embeddings themselves

It is intended to *compose* with existing standards for model cards and dataset descriptions,
rather than replace.

It is also intended to be flexible, and support the following scenarios:

1. distribute embedding metadata alongside embeddings, with the latter in an efficient format like Parquet
2. distribute both together in YAML (convenience at the expense of some access-time/space efficiency)
3. Use of other serializations than YAML for the metadata (JSON, TSV, RDF, Avro, GraphQL, ...)
4. Use of alternate storage formats for the embeddings (Arrow, HDF5, ...)
5. Easy composition with your favorite array library (numpy, xarr, pyarrow, ...)
6. Easy composition with your favorite vector database (ChromaDB, etc)
7. Use in combination with objects stored in databases like Solr, PostgreSQL, ...

Note that current functionality is highly minimal, but in future there may be
plugins e.g. for import/export from vectordbs.

Things that are out of scope including actually creating the embedding and computing over them.
There already existing many existing great frameworks for this. Venomx is focused purely on making
indexes of embeddings FAIR and easy to share.

## Example

This example is based around the Human Phenotype Ontology (HPO). Vector embeddings of HPO
are useful for searching for phenotypes, for RAG-type LLM applications, and for applications
such as variant prioritization (cosine similarity of vector embeddings could replace
traditional ontological semantic similarity measures).

The default way to distribute using venomx is a YAML file with metadata, and a Parquet file:

```
$ ls
hp.yaml
hp.parquet
```

The contents of `hp.yaml`:

```yaml
description: HPO label index
prefixes:
  HP: http://purl.obolibrary.org/obo/HP_
model:
  name: "text-embedding-ada-002"
model_input_method:
  description: Simple pass through of labels only
  fields: [ "rdfs:label" ]
dataset:
  name: HPO-Jan-2024
  url: http://purl.obolibrary.org/obo/hp/releases/2024-01-01/hp.owl
objects:
  - id: "HP:0000001"
    label: "All"
  - id: "HP:0000002"
    label: "Abnormality of body height"
  # <snip>
```

Running `parquet schema hp.parquet`
gives the schema for `hp.parquet`:

```json
{
  "type" : "record",
  "name" : "schema",
  "fields" : [ {
    "name" : "id",
    "type" : [ "null", "int" ],
    "default" : null
  }, {
    "name" : "name",
    "type" : [ "null", "string" ],
    "default" : null
  }, {
    "name" : "embedding",
    "type" : [ "null", {
      "type" : "array",
      "items" : {
        "type" : "record",
        "name" : "list",
        "fields" : [ {
          "name" : "element",
          "type" : [ "null", "float" ],
          "default" : null
        } ]
      }
    } ],
    "default" : null
  }, {
    "name" : "metadata",
    "type" : [ "null", {
      "type" : "map",
      "values" : [ "null", "string" ]
    } ],
    "default" : null
  } ]
}
```

## Command line tools

Although the main purpose of this repo is as a proposed standard, we
include some simple tools for basic conversion and validation

### Conversion

Currently only two formats are supported:

- `parquet`: two files, a metadata yaml file and a parquet file
- `yaml`: a combined all-in-one yaml file (may be less efficient)

(THIS IS PROBABLY A BIT CONFUSING AND MAY CHANGE)

The test folder includes an all-in-one example, we can convert that to a dual yaml/parquet format:

```
venomx convert -f yaml tests/input/example.combined.yaml -t parquet -o tests/output/example.yaml
```

### Validation

```
venomx validate tests/output/example.yaml
```

## Roadmap

- Use linkml-arrays standard
- other embeddings formats (xarr, arrow, ...)
- ...