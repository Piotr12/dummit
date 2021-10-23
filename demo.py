import dummit as d
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("config", help="yaml with config")
parser.add_argument("--run_date", default="", help="run date, optional")
parser.usage = "sample usage: python3 demo.py demos/less_bloated_sample_test_library.yaml --run_date 20211002"
args = parser.parse_args()

with open(args.config, 'r') as file:
    tests = d.TestLibrary(yaml_string = file.read(), params_dict = {"run_date": args.run_date}, logger = d.TextLogger()) 
    tests.run()