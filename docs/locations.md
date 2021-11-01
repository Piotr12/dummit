# Locations

Right now the following locations are implemented.

+ **exact** location is one that requires no logic at all. Check ExactLocation class for details. It has a single URI there that can be interpreted as Azure Location / Sharepoint one or a local path. 
+ **versioned_by_date** is for cases where you store historical files somewhere (a yyyymmdd timestamp is available). More details in VersionedByDateLocalFileLocation and VersionedByDateAzureBlobLocation classes. 

## Class Diagram
![Locations class diagram](../img/location_classes.png "Locations class diagram")

[back](../README.md)