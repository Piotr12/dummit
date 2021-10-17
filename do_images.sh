rm *.png
pyreverse -o png dummit/dummit_tests.py
mv classes.png img/test_classes.png
pyreverse -o png dummit/dummit_inputs.py
mv classes.png img/input_classes.png
pyreverse -o png dummit/dummit_df_tests.py
mv classes.png img/df_test_classes.png
pyreverse -o png dummit/dummit_locations.py
mv classes.png img/location_classes.png
pyreverse -o png dummit/dummit.py dummit/dummit_factories.py 
mv classes.png img/all_other_classes.png
rm packages.png