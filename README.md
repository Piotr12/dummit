# dummit
dummy input tests (spelled /ˈdamɪt/)

nothing to be seen here just an attempt to start a skeleton for simple (i.e. dummy) input tests.

## See it in action:

```bash
# get the code
git clone git@github.com:Piotr12/dummit.git
# install the package (can also use the local one if you know how)
pip install dummit
# run a sample demo,sample files are included in the repo, just a dummy csv ones. 
. ./run_demo.sh
```


## Learn more: 
The idea behind dummit is to make data tests as abstract as possible and reuse abstract building blocks to run specialized tests. Code once, run twice (or preferably dozen+ times). 

Not only for input but also for output / intermittent artifacts.

Key abstractions:
+ **Input** - either a file, or an Azure blob, or a SQL query output. A set of files, a directory with its contents. Just extend the Input class and you have your Input covered. See [Inputs](docs/inputs.md) for more.
+ **Locations** - either an exact *'path'* or some kinds of a mask to use and find an exact path (or paths). See [Locations](docs/locations.md) for more.
+ **Tests / DataFrame Tests** - abstract tests that are run on an Input (or quite often on its abstraction, via pandas.DataFrame) after getting the config injected. See [Tests](docs/tests.md) and [DataFrameTests](docs/df_tests.md) for more.
  
Sample [config file](demos/sample_local_files_config.yaml) (local files) is a first place to look at on how this all plays together. 

## Local files? Thats so 90's
Azure based inputs are also there and you can easily extend it to add your cloud provider of choice. Things just get a bit more tricky as authentication steps in. For Azure you will need to inject the code with a ConnectionString or even better use Azure KeyVault. Do not step in if thats Hungarian to you, learn the Azure Basics first (check the azure libs I do have included and learn their basic use).

## Performance
I have not tested it on large blobs, partitioned parquets. At least not yet. What is on my mind you can decide to implement a 'LargeInput' class that will just test some sample of the final one, every 10th row, 1% sample, you name it. Just thinking loud for now. 