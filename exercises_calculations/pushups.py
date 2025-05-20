from base import ExersicesBase
import cv2 
from angles_calculations import _angle_with_horizontal, _angle_between


def calculate_angles(
    hip: tuple[float, float],
    shoulder: tuple[float, float],
    elbow: tuple[float, float],
    hand: tuple[float, float]
) -> dict:
    """
    Given the (x, y) positions of hip, shoulder, elbow, and hand on one side of the body,
    returns a dict with:
      • 'hip_torso_angle': angle of your torso (hip→shoulder) vs. horizontal,
      • 'shoulder_angle': angle at your shoulder between torso and upper arm,
      • 'elbow_angle':   angle at your elbow between upper arm and forearm.
    """
    hip_torso_angle = _angle_with_horizontal(hip, shoulder)
    shoulder_angle = _angle_between(hip, shoulder, elbow)
    elbow_angle   = _angle_between(shoulder, elbow, hand)

    return {
        'hip_torso_angle': hip_torso_angle,
        'shoulder_angle': shoulder_angle,
        'elbow_angle': elbow_angle
    }


class PushUpExercise(ExersicesBase): 
    
    shoulders_landmarks_ids = [12, 11 ]
    hips_landmarks_ids = [24, 23]
    elbows_landmarks_ids = [14, 13]
    hands_landmarks_ids = [15, 16]

    right_side = [i[0] for i in [shoulders_landmarks_ids, hips_landmarks_ids, elbows_landmarks_ids, hands_landmarks_ids]]
    left_side = [i[1] for i in [shoulders_landmarks_ids, hips_landmarks_ids, elbows_landmarks_ids, hands_landmarks_ids]]


    def __init__(self, visibity_threahold = 0.2, *args, **kwargs, ):
        super().__init__(*args, **kwargs) 
        self.name = 'Push Ups'
        self.visibity_threahold = visibity_threahold

        self.down = False 
        self.up = False 

    def process_frame(self, pose_landmarks, frame):
        ps = pose_landmarks.landmark
        # Check for "down" position.  Using hips (23,24) and knees (25,26) is more robust.
        
        if all([ps[i].visibility > self.visibity_threahold for i in self.left_side]): 
            shoulder = ps[self.shoulders_landmarks_ids[1]]
            hip = ps[self.hips_landmarks_ids[1]]
            elbow = ps[self.elbows_landmarks_ids[1]]
            hand = ps[self.hands_landmarks_ids[1]]
        elif all([ps[i].visibility > self.visibity_threahold for i in self.right_side]): 
            shoulder = ps[self.shoulders_landmarks_ids[0]]
            hip = ps[self.hips_landmarks_ids[0]]
            elbow = ps[self.elbows_landmarks_ids[0]]
            hand = ps[self.hands_landmarks_ids[0]]
        else: 
            text = """Please take the right pose!"""
            text1 = """Camera have to see Hips, Shoulders, hands and elbows"""
            org = (int(frame.shape[0]/2)-50, int(frame.shape[1]/2 -40))
            org1 = (int(frame.shape[0]/2) -50, int(frame.shape[1]/2))
            cv2.putText(
                frame, text, org,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6, color=(100, 100, 255),
                thickness=2, lineType=cv2.LINE_AA
            )
            cv2.putText(
                frame, text1, org1,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6, color=(100, 100, 255),
                thickness=2, lineType=cv2.LINE_AA
            )
            return False 

        angles = calculate_angles(hip=(hip.x, hip.y), 
                                            shoulder=(shoulder.x, shoulder.y), 
                                            elbow=(elbow.x, elbow.y), 
                                            hand=(hand.x, hand.y)
                                            )
        
        # 3. Prepare text with positions offset a bit so it’s legible
        offsets = {
            'hip_torso_angle':    ( -30, -10),
            'shoulder_angle':     ( +10, -20),
            'elbow_angle':        ( +10, +20)
        }
        positions = {
            'hip_torso_angle':    (hip.x * frame.shape[0], hip.y * frame.shape[1]),
            'shoulder_angle':     (shoulder.x *frame.shape[0], shoulder.y* frame.shape[1]),
            'elbow_angle':        (elbow.x*frame.shape[0], elbow.y* frame.shape[1])
        }

        # 4. Draw each angle label
        for name, value in angles.items():
            pos = positions[name]
            off = offsets[name]
            text = f"{int(value)}°"
            org = (int(pos[0] + off[0]), int(pos[1] + off[1]))
            cv2.putText(
                frame, text, org,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6, color=(255, 255, 255),
                thickness=2, lineType=cv2.LINE_AA
            )

        if all([(angles['hip_torso_angle'] < 45), (angles['shoulder_angle'] < 45), (angles['elbow_angle'] < 45)]): 
            self.down = True 
        
        if (self.down==True) and (all([(angles['shoulder_angle'] > 45), (angles['elbow_angle'] > 55)])): 
            self.up = True 
            

            self.down = False
            self.up = False 
            return True 


        return False 


if __name__ == "__main__":

    ex = PushUpExercise() # Run it once.  Removed the loop.
    ex.run()
