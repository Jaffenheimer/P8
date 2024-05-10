from Detector import *
from Client import *
import time

id = "c4219aac-b1cd-4c0e-87fe-27be70c99cb6"
detector = Detector()
client = Client(id)

while True:
    img = detector.CaptureVideo(0)
    no_of_people = detector.imageDetection(img)
    body = {"peopleCount": no_of_people, "id": id}
    #res = client.PostPeopleCount(request=body) #Requires backend to run
    open
    time.sleep(5)