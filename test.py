from Detector import *
from Client import *
from glob import glob
from datetime import datetime

detector = Detector()

now = datetime.now()
outputDir = f"images/snapshots/{now.strftime('%H_%M_%S')}"
os.mkdir(outputDir)
out = open("results.txt", "a")
out.truncate(0)

for file in glob('images\people_detection_photos\High_21-inf\*.jpg', recursive=True):
        no_of_people = detector.imageDetection(file, outputDir)
        print(f'File: {file} | PeopleCount: {no_of_people}')
        out.write(f'File: {file} | PeopleCount: {no_of_people}\n')
for file in glob('images\people_detection_photos\Low_1-20\*.jpg', recursive=True):
        no_of_people = detector.imageDetection(file, outputDir)
        print(f'File: {file} | PeopleCount: {no_of_people}')
        out.write(f'File: {file} | PeopleCount: {no_of_people}\n')
out.close()