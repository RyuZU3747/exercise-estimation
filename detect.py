import math
import numpy as np

def vector_angle(point1, point2):
    x = point2.x - point1.x
    y = point2.y - point1.y
    z = point2.z - point1.z
    x2 = x*x
    y2 = y*y
    z2 = z*z
    p1 = x2+y2+z2
    p2 = x2+z2
    p1 = math.sqrt(p1)
    p2 = math.sqrt(p2)
    return math.degrees(math.acos((x+z)/p1*p2))
    
def arm_ccw(landmark):
    if landmark[14].visibility > 0.5:
        return (landmark[12].x - landmark[24].x) * (landmark[14].y - landmark[24].y) - (landmark[12].y - landmark[24].y) * (landmark[14].x - landmark[24].x)
    elif landmark[13].visibility > 0.5:
        return (landmark[11].x - landmark[23].x) * (landmark[13].y - landmark[23].y) - (landmark[11].y - landmark[23].y) * (landmark[13].x - landmark[23].x)
    return 0

class pushup:
    flag = 0
    cnt = 0
    frame = 0
    
    def islying(results):
        if vector_angle(results.pose_world_landmarks.landmark[23], results.pose_world_landmarks.landmark[11]) < 70 or vector_angle(results.pose_world_landmarks.landmark[23], results.pose_world_landmarks.landmark[11]) > 110:
            return True
        elif vector_angle(results.pose_world_landmarks.landmark[24], results.pose_world_landmarks.landmark[12]) < 70 or vector_angle(results.pose_world_landmarks.landmark[24], results.pose_world_landmarks.landmark[12]) > 110:
            return True
        return False
    
    def check(results):
        if abs(vector_angle(results.pose_world_landmarks.landmark[11], results.pose_world_landmarks.landmark[23]) - vector_angle(results.pose_world_landmarks.landmark[23], results.pose_world_landmarks.landmark[27])) < 30:
            return True
        elif abs(vector_angle(results.pose_world_landmarks.landmark[12], results.pose_world_landmarks.landmark[24]) - vector_angle(results.pose_world_landmarks.landmark[24], results.pose_world_landmarks.landmark[28])) < 30:
            return True
        return False
        
    def count(results):
        if abs(arm_ccw(results.pose_world_landmarks.landmark)) < 0.05:
            pushup.flag = 1
        if pushup.flag and abs(arm_ccw(results.pose_world_landmarks.landmark)) > 0.05:
            pushup.flag = 0
            pushup.cnt += 1


class squat:
    flag = 0
    cnt = 0
    frame = 0
    
    def isstand(results):
        if vector_angle(results.pose_world_landmarks.landmark[23], results.pose_world_landmarks.landmark[11]) > 70:
            return True
        elif vector_angle(results.pose_world_landmarks.landmark[24], results.pose_world_landmarks.landmark[12]) > 70:
            return True
        return False
    
    def check(results):
        if(results.pose_world_landmarks.landmark[25].visibility<0.5 and results.pose_world_landmarks.landmark[26].visibility<0.5):
            return False
        if (abs(results.pose_world_landmarks.landmark[23].y - results.pose_world_landmarks.landmark[11].y) >
            abs(results.pose_world_landmarks.landmark[23].x - results.pose_world_landmarks.landmark[11].x)):
            return True
        return False
    
    def count(results):
        knee = 0
        hip = 0
            
        if results.pose_world_landmarks.landmark[25].visibility > 0.5:
            knee = results.pose_world_landmarks.landmark[25].y
        elif results.pose_world_landmarks.landmark[26].visibility > 0.5:
            knee = results.pose_world_landmarks.landmark[26].y
            
        if results.pose_world_landmarks.landmark[23].visibility > 0.5:
            hip = results.pose_world_landmarks.landmark[23].y
        elif results.pose_world_landmarks.landmark[24].visibility > 0.5:
            hip = results.pose_world_landmarks.landmark[24].y   
        
        if knee - hip < 0.1:
            squat.flag = 1
        if squat.flag and knee - hip > 0.1:
            squat.flag = 0
            squat.cnt += 1
            

class pullup:
    flag = 0
    cnt = 0
    frame = 0
    
    def isstand(results):
        if vector_angle(results.pose_world_landmarks.landmark[23], results.pose_world_landmarks.landmark[11]) > 80:
            return True
        elif vector_angle(results.pose_world_landmarks.landmark[24], results.pose_world_landmarks.landmark[12]) > 80:
            return True
        return False
    
    def check(results):
        if(results.pose_world_landmarks.landmark[13].visibility<0.5 and results.pose_world_landmarks.landmark[14].visibility<0.5):
            return False
        if (results.pose_world_landmarks.landmark[15].y < results.pose_world_landmarks.landmark[11].y and
            results.pose_world_landmarks.landmark[16].y < results.pose_world_landmarks.landmark[12].y):
            return True
        return False
    
    def count(results):
        if (results.pose_world_landmarks.landmark[13].y < results.pose_world_landmarks.landmark[11].y and
            results.pose_world_landmarks.landmark[14].y < results.pose_world_landmarks.landmark[12].y):
            pullup.flag = 1
        if (pullup.flag == 1 and results.pose_world_landmarks.landmark[13].y > results.pose_world_landmarks.landmark[11].y and
            results.pose_world_landmarks.landmark[14].y > results.pose_world_landmarks.landmark[12].y):
            pullup.flag = 0        
            pullup.cnt += 1

class delta:
    before = None
    def caldel(idx, landmark):
        x = landmark.x - delta.before.pose_world_landmarks.landmark[idx].x
        y = landmark.y - delta.before.pose_world_landmarks.landmark[idx].y
        z = landmark.z - delta.before.pose_world_landmarks.landmark[idx].z
        return math.sqrt(x**2+y**2+z**2)
        
    def get(results):
        retlist = []
        if delta.before==None:
            delta.before = results
            return False
        else:
            for idx, landmark in enumerate(results.pose_world_landmarks.landmark):
                if delta.before.pose_world_landmarks.landmark[idx].visibility < 0.5 or landmark.visibility < 0.5:
                    continue
                retlist.append(delta.caldel(idx, landmark))
            avg = np.mean(retlist)
            delta.before = results
            if avg < 0.03:
                return True
            return False

def detposes(results):
    curpose = ""
    if pushup.check(results) and pushup.islying(results):
        curpose = "Pushup"
        pushup.count(results)
                
    if squat.check(results) and squat.isstand(results):
        curpose = "Squat"
        squat.count(results)
                
    if pullup.check(results) and pullup.isstand(results):
        curpose = "Pullup"
        pullup.count(results)
        
    return curpose