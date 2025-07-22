"""
AI People Counter Adapter
------------------------
Adapter tích hợp detection, tracking, counting cho hệ thống đếm người real-time.

Usage Example:
--------------
from ai_people_counter_adapter import PeopleCounterAdapter
adapter = PeopleCounterAdapter(prototxt_path, model_path)
result = adapter.process_frame(frame, line_start=(0, 300), line_end=(800, 300))
print(result['total_in'], result['total_out'])
"""
import cv2
import numpy as np
from typing import List, Tuple, Dict
from collections import defaultdict
from config import (
    CONFIDENCE_THRESHOLD, NMS_THRESHOLD, DISTANCE_THRESHOLD, 
    DIRECTION_THRESHOLD, LINE_TOLERANCE, MIN_MOVEMENT_DISTANCE,
    BBOX_COLOR, BBOX_THICKNESS, ID_TEXT_COLOR,
    COUNTING_LINE_COLOR, COUNTING_LINE_THICKNESS,
    DEBUG_MODE, PERSON_CLASS_INDEX, CLASSES
)

class PeopleDetector:
    """
    PeopleDetector class for detecting people in frames using a pre-trained model.
    """
    def __init__(self, prototxt_path: str, model_path: str, confidence: float = CONFIDENCE_THRESHOLD):
        """
        Initializes the PeopleDetector.

        Args:
            prototxt_path (str): Path to the Caffe prototxt file.
            model_path (str): Path to the Caffe model file.
            confidence (float): Confidence threshold for detection.
        """
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.confidence = confidence
        self.CLASSES = CLASSES

    def detect_people(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detects people in a single frame using the pre-trained model.

        Args:
            frame (np.ndarray): Input frame in BGR format.

        Returns:
            List[Tuple[int, int, int, int]]: List of detected bounding boxes.
        """
        (H, W) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        boxes = []
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] != "person":
                    continue
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                boxes.append((startX, startY, endX, endY))
        return boxes

class CentroidTracker:
    """
    CentroidTracker class for tracking objects based on their centroids.
    """
    def __init__(self, max_disappeared: int = 40, max_distance: int = 50):
        """
        Initializes the CentroidTracker.

        Args:
            max_disappeared (int): Maximum number of frames an object can disappear.
            max_distance (int): Maximum distance between centroids to consider an object.
        """
        self.next_object_id = 0
        self.objects = dict()
        self.disappeared = dict()
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

    def register(self, centroid):
        """
        Registers a new object with a unique ID.

        Args:
            centroid (Tuple[int, int]): The centroid of the new object.
        """
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        """
        Deregisters an object by its ID.

        Args:
            object_id (int): The ID of the object to deregister.
        """
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects: List[Tuple[int, int, int, int]], frame_shape=None, last_detected_frame=None, current_frame_idx=None):
        """
        Updates the tracker with new detections and updates object centroids.
        Nếu không còn detection, kiểm tra centroid cuối cùng:
        - Nếu centroid đã ra khỏi frame, deregister object ngay lập tức.
        - Nếu object vẫn trong frame, chỉ tăng disappeared như cũ.
        """
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                centroid = self.objects[object_id]
                if frame_shape is not None:
                    H, W = frame_shape[:2]
                    if centroid[0] < 0 or centroid[0] > W or centroid[1] < 0 or centroid[1] > H:
                        self.deregister(object_id)
                        continue
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects
        
        # Có detection mới, xử lý bình thường
        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            input_centroids[i] = (cX, cY)
        
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            D = np.linalg.norm(np.array(object_centroids)[:, None] - input_centroids, axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            used_rows = set()
            used_cols = set()
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                if D[row, col] > self.max_distance:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)
            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col])
        return self.objects

class PeopleCounterAdapter:
    """
    PeopleCounterAdapter class for integrating detection, tracking, and counting.
    """
    def __init__(
        self,
        prototxt_path: str,
        model_path: str,
        confidence: float = CONFIDENCE_THRESHOLD,
        skip_frames: int = 5,
        resize_width: int = 1920,
        max_disappeared: int = 50,  # <-- thêm tham số này
    ):
        """
        Adapter tích hợp detection, tracking, counting cho hệ thống đếm người real-time.

        Args:
            prototxt_path (str): Đường dẫn file prototxt của model MobileNet SSD.
            model_path (str): Đường dẫn file model MobileNet SSD.
            confidence (float): Ngưỡng confidence cho detection.
            skip_frames (int): Số frame bỏ qua giữa các lần detect.
            resize_width (int): Độ rộng resize frame để tối ưu performance.
            max_disappeared (int): Số frame tối đa giữ object khi không còn detection mới.
                - Giá trị nhỏ: bounding box biến mất nhanh khi người đã đi khỏi khung hình.
                - Giá trị lớn: tracking ổn định hơn khi có occlusion hoặc detection miss.
                - Nếu quá lớn: object tồn tại lâu dù đã biến mất.
                - Nếu quá nhỏ: object bị mất khi chỉ bị che khuất tạm thời.
        """
        self.detector = PeopleDetector(prototxt_path, model_path, confidence)
        self.tracker = CentroidTracker(max_disappeared=max_disappeared, max_distance=80)
        self.trackable_objects = dict()
        self.total_in = 0
        self.total_out = 0
        self.frame_idx = 0
        self.skip_frames = skip_frames
        self.resize_width = resize_width
        self.last_boxes = []  # Lưu boxes từ frame trước để tracking
        self.net = None  # Lưu network để detect trực tiếp
        self._load_network(prototxt_path, model_path)

    def _load_network(self, prototxt_path: str, model_path: str):
        """Load network để detect trực tiếp như code mẫu"""
        import cv2
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]

    def _detect_people_direct(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect people trực tiếp trên frame gốc như code mẫu"""
        import cv2
        (H, W) = frame.shape[:2]
        
        # Convert frame to blob như code mẫu
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        
        boxes = []
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > self.detector.confidence:
                idx = int(detections[0, 0, i, 1])
                
                if self.CLASSES[idx] != "person":
                    continue
                
                # Compute bounding box như code mẫu
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                boxes.append((startX, startY, endX, endY))
        
        return boxes

    def _resize_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, float]:
        """Resize frame về resize_width, trả về frame và scale factor"""
        (H, W) = frame.shape[:2]
        scale = self.resize_width / W
        new_width = self.resize_width
        new_height = int(H * scale)
        resized = cv2.resize(frame, (new_width, new_height))
        return resized, scale

    def _scale_boxes(self, boxes: List[Tuple[int, int, int, int]], scale: float) -> List[Tuple[int, int, int, int]]:
        """Scale boxes về kích thước gốc"""
        scaled_boxes = []
        for (startX, startY, endX, endY) in boxes:
            scaled_startX = int(startX / scale)
            scaled_startY = int(startY / scale)
            scaled_endX = int(endX / scale)
            scaled_endY = int(endY / scale)
            scaled_boxes.append((scaled_startX, scaled_startY, scaled_endX, scaled_endY))
        return scaled_boxes

    def _scale_boxes_accurate(self, boxes: List[Tuple[int, int, int, int]], scale: float, original_shape: Tuple[int, int, int]) -> List[Tuple[int, int, int, int]]:
        """Scale boxes với độ chính xác cao và boundary checking"""
        scaled_boxes = []
        H, W = original_shape[:2]
        
        for (startX, startY, endX, endY) in boxes:
            # Scale với độ chính xác cao
            scaled_startX = max(0, int(startX / scale))
            scaled_startY = max(0, int(startY / scale))
            scaled_endX = min(W, int(endX / scale))
            scaled_endY = min(H, int(endY / scale))
            
            # Đảm bảo box hợp lệ
            if scaled_endX > scaled_startX and scaled_endY > scaled_startY:
                scaled_boxes.append((scaled_startX, scaled_startY, scaled_endX, scaled_endY))
        
        return scaled_boxes

    def _line_intersection(self, line_start: Tuple[int, int], line_end: Tuple[int, int], 
                          point: Tuple[int, int]) -> bool:
        """Kiểm tra điểm có vượt qua line không (công thức hình học)"""
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Tính vector từ line_start đến point và line_end
        v1 = (x - x1, y - y1)
        v2 = (x2 - x1, y2 - y1)
        
        # Tính cross product để xác định hướng
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        
        return cross_product

    def _segment_crosses_line(self, p1, p2, l1, l2, tolerance=LINE_TOLERANCE):
        """
        Kiểm tra đoạn nối giữa 2 centroid (p1, p2) có cắt qua line (l1, l2) không.
        Sử dụng thuật toán kiểm tra giao nhau 2 đoạn thẳng dựa trên cross product.
        Thêm tolerance để mở rộng line một chút, giúp nhạy hơn với các chuyển động nhỏ.
        
        Args:
            p1, p2: Hai centroid liên tiếp
            l1, l2: Hai điểm của line
            tolerance: Khoảng cách mở rộng line (pixel)
        
        Returns:
            bool: True nếu cắt qua, False nếu không
        """
        def ccw(a, b, c):
            return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])
        
        # Kiểm tra khoảng cách tối thiểu giữa 2 centroid
        distance = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5
        if distance < MIN_MOVEMENT_DISTANCE:  # Nếu di chuyển quá ít, không đếm
            return False
        
        # Mở rộng line theo hướng pháp tuyến
        import numpy as np
        line_vec = np.array([l2[0] - l1[0], l2[1] - l1[1]])
        line_length = np.linalg.norm(line_vec)
        if line_length == 0:
            return False
        
        # Vector pháp tuyến (vuông góc với line)
        normal_vec = np.array([-line_vec[1], line_vec[0]]) / line_length
        
        # Mở rộng line theo 2 hướng
        l1_extended = (l1[0] - normal_vec[0] * tolerance, l1[1] - normal_vec[1] * tolerance)
        l2_extended = (l2[0] - normal_vec[0] * tolerance, l2[1] - normal_vec[1] * tolerance)
        
        # Kiểm tra giao nhau với line đã mở rộng
        crosses = (ccw(p1, l1_extended, l2_extended) != ccw(p2, l1_extended, l2_extended)) and \
                  (ccw(p1, p2, l1_extended) != ccw(p1, p2, l2_extended))
        
        return crosses

    def _get_crossing_direction(self, prev_centroid, curr_centroid, line_start, line_end, direction_threshold=DIRECTION_THRESHOLD):
        """
        Xác định hướng crossing khi object cắt qua line bất kỳ (ngang, dọc, chéo).
        Sử dụng vector pháp tuyến của line để tính toán hướng di chuyển tương đối:
        - Trả về 1 nếu object đi từ phía A sang phía B (theo chiều pháp tuyến)
        - Trả về -1 nếu object đi ngược lại
        - Trả về 0 nếu không đủ điều kiện hoặc chỉ dao động nhỏ
        Args:
            prev_centroid (tuple): Centroid trước khi crossing (x, y)
            curr_centroid (tuple): Centroid sau khi crossing (x, y)
            line_start (tuple): Điểm đầu line (x, y)
            line_end (tuple): Điểm cuối line (x, y)
            direction_threshold (float): Ngưỡng tối thiểu để tránh rung lắc nhỏ
        Returns:
            int: 1 (qua theo chiều pháp tuyến), -1 (ngược chiều), 0 (không tính)
        """
        import numpy as np
        line_vec = np.array([line_end[0] - line_start[0], line_end[1] - line_start[1]])
        normal_vec = np.array([-line_vec[1], line_vec[0]])
        normal_vec = normal_vec / (np.linalg.norm(normal_vec) + 1e-8)
        move_vec = np.array([curr_centroid[0] - prev_centroid[0], curr_centroid[1] - prev_centroid[1]])
        proj = np.dot(move_vec, normal_vec)
        if abs(proj) > direction_threshold:
            return 1 if proj > 0 else -1
        return 0

    def process_frame(self, frame: np.ndarray, line_start: Tuple[int, int] = None, 
                     line_end: Tuple[int, int] = None, reverse_io: bool = False) -> Dict:
        """
        Processes a single frame to detect, track, and count people.
        - Đảo chiều logic đếm in/out nếu reverse_io=True
        """
        (H, W) = frame.shape[:2]
        
        # Mặc định line ở giữa khung hình
        if line_start is None:
            line_start = (0, H // 2)
        if line_end is None:
            line_end = (W, H // 2)
        
        # Debug: Log line position
        if self.frame_idx % 30 == 0:  # Log mỗi 30 frame
            print(f"[DEBUG] Line: {line_start} -> {line_end}, Frame: {self.frame_idx}")
        
        # Resize frame để tối ưu performance
        resized_frame, scale = self._resize_frame(frame)
        
        # FIX: Tracking liên tục thật sự
        if self.frame_idx % self.skip_frames == 0:
            # Detect trực tiếp trên frame gốc để đảm bảo chính xác
            new_boxes = self._detect_people_direct(frame)
            if len(new_boxes) > 0:
                print(f"[DEBUG] Frame {self.frame_idx}: Detected {len(new_boxes)} people directly")
                if self.frame_idx % 60 == 0:  # Giảm debug frequency
                    print(f"[DEBUG] New boxes: {new_boxes}")
                # Cập nhật boxes mới cho tracker
                self.last_boxes = new_boxes
            else:
                # Nếu không detect được, giữ boxes cũ để tracking liên tục
                if len(self.last_boxes) == 0:
                    # Nếu chưa có boxes nào, tạo empty list
                    self.last_boxes = []
                # Nếu có boxes cũ, giữ nguyên để tracker có thể predict
                print(f"[DEBUG] Frame {self.frame_idx}: No detection, keeping {len(self.last_boxes)} old boxes for tracking")
        
        # Update tracking với boxes hiện tại (có thể là cũ hoặc mới)
        # Gọi tracker.update với frame_shape để hỗ trợ deregister ngay khi out of frame
        objects = self.tracker.update(self.last_boxes, frame_shape=frame.shape)
        
        # Debug: Log tracking info
        if self.frame_idx % 30 == 0:
            print(f"[DEBUG] Tracker update: boxes={len(self.last_boxes)}, objects={len(objects)}")
            if len(objects) > 0:
                print(f"[DEBUG] Objects from tracker: {objects}")
                # Log tracking continuity
                for obj_id, centroid in objects.items():
                    if obj_id in self.trackable_objects:
                        history_len = len(self.trackable_objects[obj_id]["centroids"])
                        print(f"[DEBUG] Object {obj_id}: tracked for {history_len} frames")
        
        # Tạo danh sách object info cho UI
        object_info = []
        N = 10
        for object_id, centroid in list(objects.items()):
            # Kiểm tra nếu centroid ra khỏi khung hình thì xóa object ngay
            if centroid[0] < 0 or centroid[0] > W or centroid[1] < 0 or centroid[1] > H:
                self.tracker.deregister(object_id)
                if object_id in self.trackable_objects:
                    del self.trackable_objects[object_id]
                continue  # Không vẽ bounding box cho object này
            # Kiểm tra object vừa được detect gần đây
            detected_recently = False
            if object_id in self.trackable_objects:
                to = self.trackable_objects[object_id]
                if "last_detected_frame" in to:
                    if self.frame_idx - to["last_detected_frame"] <= N:
                        detected_recently = True
            if not detected_recently:
                continue  # Không vẽ bounding box nếu object không được detect gần đây
            # Nếu object đã bị deregister ở trên, không append vào object_info
            if object_id not in self.tracker.objects:
                continue
            # Tìm bounding box tương ứng
            box = None
            min_distance = float('inf')
            for (startX, startY, endX, endY) in self.last_boxes:
                box_centroid = (int((startX + endX) / 2.0), int((startY + endY) / 2.0))
                distance = ((box_centroid[0] - centroid[0]) ** 2 + (box_centroid[1] - centroid[1]) ** 2) ** 0.5
                if distance < min_distance and distance < 100:
                    min_distance = distance
                    box = (startX, startY, endX, endY)
            if box is None and centroid is not None:
                box_size = 40
                box_height = 80
                startX = max(0, int(centroid[0] - box_size // 2))
                startY = max(0, int(centroid[1] - box_height // 2))
                endX = min(W, int(centroid[0] + box_size // 2))
                endY = min(H, int(centroid[1] + box_height // 2))
                box = (startX, startY, endX, endY)
            object_info.append({
                "id": object_id,
                "centroid": centroid,
                "box": box
            })
        
        # FIX: Đếm vào/ra chỉ khi thực sự đi qua line, mỗi object chỉ đếm 1 lần
        direction_threshold = 1  # Giảm xuống 1 để nhạy hơn
        for object_id, centroid in objects.items():
            to = self.trackable_objects.get(object_id, {"centroids": [], "counted": False, "last_side": None})
            
            # Xác định phía hiện tại của centroid so với line
            current_side = self._line_intersection(line_start, line_end, centroid)
            
            # Nếu chưa có trackable object, tạo mới
            if to["last_side"] is None:
                to["last_side"] = current_side
                # Thêm centroid đầu tiên
                to["centroids"].append(centroid)
            else:
                # Chỉ thêm centroid mới khi có detection thực sự (không phải mỗi frame)
                object_detected_this_frame = False
                for (startX, startY, endX, endY) in self.last_boxes:
                    box_centroid = (int((startX + endX) / 2.0), int((startY + endY) / 2.0))
                    distance = ((box_centroid[0] - centroid[0]) ** 2 + (box_centroid[1] - centroid[1]) ** 2) ** 0.5
                    if distance < 50:
                        object_detected_this_frame = True
                        break
                if object_detected_this_frame:
                    to["centroids"].append(centroid)
                    print(f"[DEBUG] Object {object_id} detected, added centroid: {centroid}")
                # CHỈ ĐẾM KHI ĐỔI DẤU CROSS PRODUCT (đi từ phía này sang phía kia)
                if not to["counted"] and to["last_side"] != current_side:
                    if len(to["centroids"]) > 1:
                        prev_centroid = to["centroids"][-2]
                        curr_centroid = to["centroids"][-1]
                        distance = ((curr_centroid[0] - prev_centroid[0])**2 + (curr_centroid[1] - prev_centroid[1])**2)**0.5
                        if distance > 5:
                            crossing_dir = self._get_crossing_direction(prev_centroid, curr_centroid, line_start, line_end, direction_threshold)
                            # Đảo chiều logic nếu reverse_io
                            if reverse_io:
                                crossing_dir = -crossing_dir
                            import numpy as np
                            line_vec = np.array([line_end[0] - line_start[0], line_end[1] - line_start[1]])
                            normal_vec = np.array([-line_vec[1], line_vec[0]])
                            normal_vec = normal_vec / (np.linalg.norm(normal_vec) + 1e-8)
                            move_vec = np.array([curr_centroid[0] - prev_centroid[0], curr_centroid[1] - prev_centroid[1]])
                            proj = np.dot(move_vec, normal_vec)
                            print(f"[DEBUG] ✅ Side change detected: obj={object_id}, prev_side={to['last_side']}, curr_side={current_side}, prev={prev_centroid}, curr={curr_centroid}, distance={distance:.1f}, line=({line_start},{line_end}), move_vec={move_vec}, normal_vec={normal_vec}, proj={proj:.2f}, crossing_dir={crossing_dir}")
                            if crossing_dir == 1:
                                self.total_in += 1
                                to["counted"] = True
                                print(f"[DEBUG] 🎉 COUNTED IN: Object {object_id} crossed line!")
                            elif crossing_dir == -1:
                                self.total_out += 1
                                to["counted"] = True
                                print(f"[DEBUG] 🎉 COUNTED OUT: Object {object_id} crossed line!")
                            else:
                                if self.frame_idx % 30 == 0:
                                    print(f"[DEBUG] ❌ Object {object_id} side change detected but below threshold (proj={proj:.2f})")
                        else:
                            if self.frame_idx % 60 == 0:
                                print(f"[DEBUG] ❌ Object {object_id} side change detected but movement too small (distance={distance:.1f})")
                    else:
                        if self.frame_idx % 60 == 0:
                            print(f"[DEBUG] ❌ Object {object_id} side change detected but no previous centroid")
                # KHÔNG reset counted về False nữa!
                # to["counted"] = False nếu muốn đếm lại khi quay lại, nhưng ở đây chỉ đếm 1 lần
                to["last_side"] = current_side
            to["last_detected_frame"] = self.frame_idx
            self.trackable_objects[object_id] = to
        
        self.frame_idx += 1
        
        # Xác định label
        if reverse_io:
            in_label = "BÊN PHẢI: IN"
            out_label = "BÊN TRÁI: OUT"
            counting_direction = "reverse"
        else:
            in_label = "BÊN TRÁI: IN"
            out_label = "BÊN PHẢI: OUT"
            counting_direction = "normal"
        return {
            "total_in": self.total_in,
            "total_out": self.total_out,
            "objects": object_info,
            "boxes": self.last_boxes,
            "frame_idx": self.frame_idx,
            "line_start": line_start,
            "line_end": line_end,
            "fps_optimized": True,
            "resize_width": self.resize_width,
            "skip_frames": self.skip_frames,
            "reverse_io": reverse_io,
            "in_label": in_label,
            "out_label": out_label,
            "counting_direction": counting_direction
        } 