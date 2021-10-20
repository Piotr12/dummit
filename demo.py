import dummit as d

with open('demos/less_bloated_sample_test_library.yaml', 'r') as file:
    tests = d.TestLibrary(file.read(), d.TextLogger()) 
    tests.run("DEV")
    #tests.run("QA")
    #tests.run("PROD")