import cvzone
import mediapipe
import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import time

"""STEP 1"""
camera = cv2.VideoCapture(0)
# increasing the size of our video img
camera.set(3, 1200)
camera.set(4, 720)
detector = HandDetector(detectionCon=0.8)  # detecting our hands value towards 1 mean more harder to detect more
# accurate value

"""STEP 4"""


class MCQ:
    def __init__(self, data):
        """

        :param data: retrieve our question in each columns,
        data = ['Question', 'Choice1', 'Choice2', 'Choice3', 'Choice4', 'Answer']
        """
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None  # Storing what user answered

    """STEP 9 """

    def update(self, cursor, boundboxs):
        for x, bbox in enumerate(boundboxs):
            x1, y1, x2, y2 = bbox
            # checking if cursor is within the box or not
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1  # x will return which option is clicked by user +1 is for starting with 1 index
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


"""STEP 3"""
# Importing our csv data from MCQ.csv file
pathCSV = "../Questions/MCQ.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    ALLdata = list(reader)[1:]  # we are leaving first(['Question', 'Choice1', 'Choice2', 'Choice3', 'Choice4',
    # 'Answer']) rows that is why we did [1:]
# print(ALLdata)


"""STEP 5"""
# Create Object for each MCQ
mcqList = []
for q in ALLdata:
    mcqList.append(MCQ(q))  # creating our object here.

print(len(mcqList))
questionNO = 0  # question number
questionTotal = len(ALLdata)  # Total Question we have

"""STEP 2"""
# Opening our webcam
while True:
    success, img = camera.read()
    img = cv2.flip(img, 1)  # flipping our video in correct manner
    """STEP 6"""
    hands, img = detector.findHands(img, flipType=False)  # Here flipType correcting our hand position

    """STEP 7"""
    # Displaying MCQ question on to the web screen
    if questionNO < questionTotal:
        mcq = mcqList[questionNO]
        img, boundBox = cvzone.putTextRect(img,
                                           mcq.question,
                                           [200, 100],
                                           2,
                                           2,
                                           offset=50,
                                           border=5,
                                           )  # offset give us the margin
        img, boundBox1 = cvzone.putTextRect(img,
                                            mcq.choice1,
                                            [200, 250],
                                            2,
                                            2,
                                            offset=50,
                                            border=5,
                                            )  # offset give us the margin
        img, boundBox2 = cvzone.putTextRect(img,
                                            mcq.choice2,
                                            [500, 250],
                                            2,
                                            2,
                                            offset=50,
                                            border=5,
                                            )  # offset give us the margin
        img, boundBox3 = cvzone.putTextRect(img,
                                            mcq.choice3,
                                            [200, 400],
                                            2,
                                            2,
                                            offset=50,
                                            border=5,
                                            )  # offset give us the margin
        img, boundBox4 = cvzone.putTextRect(img,
                                            mcq.choice4,
                                            [500, 400],
                                            2,
                                            2,
                                            offset=50,
                                            border=5,
                                            )  # offset give us the margin

        """STEP 8"""
        # checking if we clicked answer
        if hands:
            lmList = hands[0]['lmList']  # first hand hands[0], lmList -> LandMarkList
            # cursor is your tip of your index finger
            cursor = lmList[8]  # From mediapipe we know that 8 point is our tip of our index finger
            # check weather we clicked or not
            length, info = detector.findDistance(lmList[8], lmList[12])  # Here point 12 is the tip of the
            # middle finger.
            # when Distance from the index and middle tip is less then we assume we clicked
            # print(length)  # seeing the distance value

            """STEP 9 Cont..."""
            # finding lowest distance value
            if length < 34:
                # print("clicked")
                mcq.update(cursor, [boundBox1, boundBox2, boundBox3, boundBox4])
                print(mcq.userAns)
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    questionNO += 1
    else:
        """STEP 11"""
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        # Converting score into percentage
        score = round((score/questionTotal)*100,2)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)

    """STEP 10"""
    # Drawing Progress Bar
    barVal = 150 + (
                950 // questionTotal) * questionNO  # starting point + total width(1100-150=950) of the bar % by questionTotal
    cv2.rectangle(img, (150, 600), (barVal, 650), (0, 255, 0), cv2.FILLED)  # progress bar size
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)  # progress bar outer
    img, _ = cvzone.putTextRect(img, f'{round((questionNO / questionTotal) * 100)}%', [1130, 635], 2, 2, offset=16,
                                border=None)  # displaying percentage

    cv2.imshow('Quiz', img)
    cv2.waitKey(1)
