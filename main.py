from Detector import *
from Client import *
import time

id = "c4219aac-b1cd-4c0e-87fe-27be70c99cb6"
now = datetime.now()
outputDir = f"images/snapshots/main/{now.strftime('%A_%d%b_%H_%M_%S')}"
os.mkdir(outputDir)
out = open(f"{outputDir}/results.txt", "a")
out.truncate(0)

detector = Detector(outputDir)
client = Client(id)


while True:
    out = open(f"{outputDir}/results.txt", "a")
    img = detector.CaptureVideo(0)
    no_of_people = detector.imageDetection(img)
    body = {"peopleCount": no_of_people, "id": id}
    #res = client.PostPeopleCount(request=body) #Requires backend to run
    out.write(f'PeopleCount: {no_of_people}\n')
    out.close()
    time.sleep(5)