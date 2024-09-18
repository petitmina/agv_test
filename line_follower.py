import cv2
import numpy as np

class LineFollower:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)  # 0번 카메라 사용 (기본 카메라)

    def process_frame(self):
        """카메라에서 프레임을 받아 선을 인식하고 위치를 반환"""
        ret, frame = self.camera.read()
        if not ret:
            print("Failed to capture image")
            return None
        
        # 이미지를 흑백으로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 가우시안 블러 적용하여 노이즈 제거
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # 이진화 (threshold)
        _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # ROI 설정 (하단만 선을 탐지)
        height, width = binary.shape
        roi = binary[int(height/2):, :]  # 이미지의 하단 절반

        # 선의 중심 찾기 (흰색 픽셀의 평균 위치)
        contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            # 가장 큰 컨투어 찾기
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)

            if M['m00'] > 0:  # 선이 있는 경우
                cx = int(M['m10'] / M['m00'])  # 선의 중심 x좌표 계산
                return cx  # 선의 중심 좌표 반환
        return None  # 선을 찾지 못한 경우

    def release(self):
        """카메라 해제"""
        self.camera.release()
