# Dummit Inputs

The following input types are implemented:
+ **local_file** - a single file in local file system
+ **local_versioned_file** - a pair of files in the local file system, current and previous one. On such input the tests like "no drastic (i.e. +/- 50%) increase vs previous file" can be executed.
+ **azure_blob** - a blob in Azure Storage Container

## Class Diagram
![Inputs class diagram](../img/input_classes.png "Inputs class diagram")

[back](../README.md)