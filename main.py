import os
import sys
import glob

try:
    sys.path.append(glob.glob(
        'C:/Program Files/WindowsNoEditor/PythonAPI/carla/dist/carla-0.9.9-py3.7-win-amd64.egg'
    )[0])
except IndexError:
    print("CARLA egg not found")

print("1. Train Model")
print("2. Run Model")

choice = input("Enter choice: ")

if choice == "1":
    os.system("python models/train.py")
elif choice == "2":
    os.system("python inference/run_model.py")