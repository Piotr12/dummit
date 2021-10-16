rm *.png
pyreverse -o png dummit_tests.py
mv classes.png test_classes.png
pyreverse -o png dummit_inputs.py
mv classes.png input_classes.png
pyreverse -o png dummit_df_tests.py
mv classes.png df_test_classes.png
pyreverse -o png dummit.py dummit_factories.py dummit_df_tests.py
