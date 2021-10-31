rm *.png
pyreverse -o png src/dummit/tests.py
mv classes.png img/test_classes.png
pyreverse -o png src/dummit/inputs.py
mv classes.png img/input_classes.png
pyreverse -o png src/dummit/df_tests.py
mv classes.png img/df_test_classes.png
pyreverse -o png src/dummit/locations.py
mv classes.png img/location_classes.png
pyreverse -o png src/dummit/dummit.py src/dummit/factories.py src/dummit/secrets.py 
mv classes.png img/all_other_classes.png
rm packages.png
