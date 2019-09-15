# Information-Extraction-Romanian

The system extracts information from a Romanian text file and saves it as a Resource Description Framework(RDF) data graph that can be 
futher queried using the `query.py` script. 

Each node in the RDF graph is saved as triples(Subject+Predicate+Object) and has the following structure:

```
<relation:relation rdf:nodeID="RDF_ID">
    <relation:object>
      <entity:TYPE_OF_ENTITY rdf:nodeID="RDF_ID">
        <entity:words>list of words</entity:words>
      </entity:TYPE_OF_ENTITY>
    </relation:object>
    <relation:predicate>list of words</relation:predicate>
    <relation:subject>
      <entity:TYPE_OF_ENTITY rdf:nodeID="RDF_ID">
        <entity:words>list of words</entity:words>
      </entity:TYPE_OF_ENTITY>
    </relation:subject>
</relation:relation>
```

Where:
 - `RDF_ID` is the id of the rdf node
 - `TYPE_OF_ENTITY` is one of the 16 entities described in [RONEC](https://github.com/dumitrescustefan/ronec)
 - `list of words` is a list of words that creates the Subject, predicate or the object of the node
 
## Installation

Install with:

```
git clone https://github.com/avramandrei/Information-Extraction-Romanian.git
cd Information-Extraction-Romanian
pip install -r requirements.txt
```

 ## Usage
 
 To extract information from a file, run the `extract_information.py` script as following:
 
 `python3 extract_information.py [ro_text_file_path] [output_dir]`
 
 The script automatically creates two files: `output.conllup` and `output.xml` in `[output_dir]`, representing the output of the Named 
 Entity Recognizer in CoNLL-U Plus format and the output RDF graph, respectievly.
 
 ## Query
 
 The repository contains a RDF graph in `resources\rdf_graph.xml`, that has been obtained by crawling news sites. The `query.py` script
 allows you to select specific Subjects and Predicates from the RDF graph. It must be used as follows:
 
 ```
 python3 query.py [rdf_graph_path] [sql_out] [--subj] [--pred]
 ```
 
 The command will create a file that contains the output of the query. 
 
 ## Notes
 
 - Feel free to ask any questions regarding the system by opening an issue or by directly sending me an email at
 avram.andreimarius@gmail.com.
 - We are looking for a team to develop a relationship corpus for the Romanian language to further improve the system.
 Contact me at avram.andreimarius@gmail.com for more information.
 
