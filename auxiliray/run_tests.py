import os
import subprocess

root_dir = "Phase1_implementations"
test_file_name = "hidden_tests_TaskB.py"

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    
    if os.path.isdir(folder_path):
        found = False
        for dirpath, dirnames, filenames in os.walk(folder_path):
            if test_file_name in filenames:
                test_path = os.path.join(dirpath, test_file_name)
                print(f"Running test: {test_path}")
                
                # Explicit python call and verbose pytest
                subprocess.run(["python3", "-m", "pytest", "-v", test_path])
                
                found = True
                break
        if not found:
            print(f"Test file not found in folder: {folder_path}")