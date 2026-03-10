import cv2
import numpy as np
import json
import os

SEQUENCE = ["1", "أ", "2", "ب", "3", "ت", "4", "ث", "5", "ج"]

def process_clock(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None: return {"error": "read_error", "score": 0}

    img = cv2.resize(img, (800, 800))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 8)

    circle_present = False
    center_x, center_y = 400, 400
    radius_detected = 300
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnts = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in cnts:
            area = cv2.contourArea(c)
            peri = cv2.arcLength(c, True)
            if peri == 0: continue
            circularity = 4 * np.pi * area / (peri**2)
            
            if area > 5000 and circularity > 0.35:
                circle_present = True
                M = cv2.moments(c)
                if M['m00'] != 0:
                    center_x = int(M['m10'] / M['m00'])
                    center_y = int(M['m01'] / M['m00'])
                
                radius_detected = int(np.sqrt(area / np.pi))
                break

    edges = cv2.Canny(gray, 50, 150)
    ys, xs = np.where(edges > 0)
    bins = [0] * 12
    for x_p, y_p in zip(xs, ys):
        dx, dy = x_p - center_x, center_y - y_p
        d = np.hypot(dx, dy)
        if 0.7 * radius_detected < d < 1.1 * radius_detected:
            ang = (np.degrees(np.arctan2(dy, dx)) + 360) % 360
            bins[int(ang // 30)] += 1
    
    occupied = sum(b > 5 for b in bins)
    num_ok = (occupied >= 8)

    angle_votes = []
    for x_p, y_p in zip(xs, ys):
        dist = np.hypot(x_p - center_x, center_y - y_p)
        if 15 < dist < 0.6 * radius_detected:
            angle = (np.degrees(np.arctan2(center_y - y_p, x_p - center_x)) + 360) % 360
            angle_votes.append(angle)
    
    time_ok = False
    if len(angle_votes) > 30:
        hist, b_edges = np.histogram(angle_votes, bins=24, range=(0, 360))
        peaks = [i for i in range(len(hist)) if hist[i] > (max(hist)*0.4)]
        h_ok = any(100 < (p*15) < 170 for p in peaks)
        m_ok = any(0 <= (p*15) < 60 or 330 < (p*15) <= 360 for p in peaks)
        time_ok = (h_ok and m_ok)

    score = (1 if circle_present else 0) + (1 if num_ok else 0) + (1 if time_ok else 0)
    return {
        "score": score, 
        "details": {
            "circle_valid": circle_present, 
            "occupied_zones": occupied, 
            "time_correct": time_ok,
            "metrics": {"circularity": round(circularity, 2) if 'circularity' in locals() else 0}
        }
    }

def process_cube(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(cv2.GaussianBlur(gray, (5,5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    edges = cv2.Canny(thresh, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, minLineLength=40, maxLineGap=15)
    v_count = 0
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        v_count = len(cv2.approxPolyDP(max(contours, key=cv2.contourArea), 0.04 * cv2.arcLength(max(contours, key=cv2.contourArea), True), True))
    score = 1 if ((len(lines) if lines is not None else 0) >= 6 and v_count >= 5) else 0
    return {"score": score, "lines": len(lines) if lines is not None else 0, "vertices": v_count}

def process_trails(patient_data):
    if not os.path.exists("tmt_targets.json"): return {"score": 0}
    with open("tmt_targets.json", "r", encoding="utf-8") as f: targets = json.load(f)
    points = patient_data["points"]
    raw_hits = []
    for p in points:
        px, py = p.get("nx", 0), p.get("ny", 0)
        for label, t in targets.items():
            if np.sqrt((px - t["nx"])**2 + (py - t["ny"])**2) <= 0.12:
                if not raw_hits or label != raw_hits[-1]: raw_hits.append(label)
                break
    cleaned_path = []
    target_idx = 0
    for hit in raw_hits:
        if target_idx < len(SEQUENCE) and hit == SEQUENCE[target_idx]:
            cleaned_path.append(hit); target_idx += 1
    score = 1 if cleaned_path == SEQUENCE else 0
    return {"score": score, "hits_raw": raw_hits, "cleaned_path": cleaned_path}
