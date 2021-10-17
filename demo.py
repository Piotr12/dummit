import dummit as d

with open('sample_test_library.yaml', 'r') as file:
    tests = d.TestLibrary(file.read(), d.TextLogger()) 
    tests.run("DEV")
    #tests.run("QA")
    #tests.run("PROD")