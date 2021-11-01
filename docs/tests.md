# Tests

The following tests are implemented and run straight on input level (without pandas.DataFrame abstraction in use):

+ **be_present** - just check if the file (or blob, sharepoint file, query result) is there. 
+ **be_modified_at_least_x_hours_ago** - above plus check on the last modification date vs a parametrized limit.

The content tests are based on a pandas.DataFrame abstraction - check them at [df_tests](df_tests.md) page.

## Tests Class Diagram
![Tests class diagram](../img/test_classes.png "Tests class diagram")

[back](../README.md)