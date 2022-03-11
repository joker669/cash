#!/usr/bin/env python
# -*- coding: utf-8 -*-

# In[ ]:
import cv2
import mediapipe as mp

# In[ ]:
class FaceMeshDetector:

    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False,
                                                    max_num_faces=5,
                                                    refine_landmarks=False,
                                                    min_detection_confidence=0.5,
                                                    min_tracking_confidence=0.5)

    def closestLandmark(self, multi_face_landmarks):
        faces_number = len(multi_face_landmarks)
        print('number of face =', faces_number)
        multi_facelandmark_6z = []
        for face_landmarks in multi_face_landmarks:
            multi_facelandmark_6z.append(face_landmarks.landmark[6].z)
            # nose bridge landmark [6]
            # 生成一个列表：在一张图片中的多个脸的6z值,
            # the smaller the z value the closer the landmark is to the camera.

        min6z = min(multi_facelandmark_6z)
        index = multi_facelandmark_6z.index(min6z)
        face_landmarks = multi_face_landmarks[index]

        return face_landmarks

    def findFaceMesh(self, image, draw = False):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.face_mesh.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        face = []
        point_2d = []
        point_3d = []
        nose_2d = []
        nose_3d = []
        if self.results.multi_face_landmarks:
            face_landmarks = self.closestLandmark(self.results.multi_face_landmarks)

            if draw:
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())

            ih, iw, ic = image.shape
            for idx, landmark in enumerate(face_landmarks.landmark):
                # print(landmark)
                x, y = int(landmark.x * iw), int(landmark.y * ih)
                # cv2.putText(image, str(idx), (x, y), cv2.FONT_HERSHEY_PLAIN,
                #             1, (0, 0, 255), 1)
                face.append([x, y])
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    # Right Eye[263], Left Eye[33], Nose[1], left mouth Corner[63],right mouth corner[291], Chin[199]
                    if idx == 1:
                        nose_2d = (x, landmark.y * ih)
                        nose_3d = (landmark.x * iw, landmark.y * ih, landmark.z * 5000)
                    point_2d.append([x, y])
                    point_3d.append([x, y, landmark.z])

        return image, face, point_2d, point_3d, nose_2d, nose_3d
