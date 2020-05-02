# XML and brat

A Repository to exhibit a simple workflow working with xml and brat, as shown in *Exercise Session 2* for the course *Creation and Annotation of Linguistic Resources*.

Remember that the code provided here was written for exactly the files I worked on in the session. If you want to use them for other files/projects, they quite possibly need to be adjusted.

## The Pipeline 

1. Get a `.txt`-file out of the original, not-yet-annotated `.xml`-file. For this, the script `get_text_to_annotate.py` can be used. It takes the following arguments:

    - `-x`: Path to the original `.xml`-file
    - `-t`: Path to target-file (brat is only going to open it if it has the suffix `.txt`)

2. Annotate the textfile in brat. If its done online, enter only one character as the title when asked to specify. The online version includes the title in the document, and counts it when writing the position of the annotation in the standoff-file. Later in the pipeline, we therefore need to specify if we've annotated on the brat-website or locally.

3. Get the `.ann`-file with all the annotations and save it. Run the *(at this point hopefully completely debugged)* `reintegrate_annotation.py` to get back the original XML-format, but now with the annotations. The following arguments need to be specified:

    - `-x`: Path to the original `.xml`-file
    - `-t`: Path to the `.txt`-file that was used to annotate
    - `-a`: Path to the `.ann`-file that was created by brat
    - `-n`: Path for the new `.xml`-file with annotations
    - `-o`: Flag to use if the `.ann`-file was created online
