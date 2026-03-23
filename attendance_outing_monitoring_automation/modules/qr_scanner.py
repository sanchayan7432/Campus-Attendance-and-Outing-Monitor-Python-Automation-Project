# modules/qr_scanner.py

import cv2


def scan_qr_code():
    """
    Opens webcam and scans a QR code using OpenCV QRCodeDetector.
    Returns the detected QR code text.
    Press 'q' to cancel scanning.
    """

    # Use DirectShow backend to avoid MSMF warnings on Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Error: Unable to access camera.")
        return None

    detector = cv2.QRCodeDetector()
    qr_code_data = None

    print("🔄 Starting camera. Press 'q' to cancel scanning.")

    try:
        while True:

            ret, frame = cap.read()

            # If frame not captured properly
            if not ret or frame is None:
                print("⚠️ Warning: Failed to grab frame.")
                continue

            # Detect and decode QR
            data, points, _ = detector.detectAndDecode(frame)

            if data:
                qr_code_data = data

                # Draw bounding box
                if points is not None:
                    points = points.astype(int)

                    for i in range(len(points[0])):
                        pt1 = tuple(points[0][i])
                        pt2 = tuple(points[0][(i + 1) % len(points[0])])
                        cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

                # Display QR data
                cv2.putText(
                    frame,
                    f"QR: {qr_code_data}",
                    (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                cv2.imshow("QR Code Detected", frame)

                # Show result for 1.5 seconds
                cv2.waitKey(1500)

                print(f"✅ QR Code detected: {qr_code_data}")

                break

            # Show scanning window
            cv2.imshow("Scan QR Code - Press 'q' to cancel", frame)

            # Cancel scan
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("❌ Scan cancelled.")
                qr_code_data = None
                break

    finally:
        # Always release camera safely
        cap.release()
        cv2.destroyAllWindows()

    return qr_code_data








# # qr_scanner.py
# import cv2

# def scan_qr_code():
#     """
#     Opens the webcam and scans QR codes using OpenCV's QRCodeDetector.
#     Returns the first detected QR code data.
#     Press 'q' to cancel scanning.
#     """
#     cap = cv2.VideoCapture(0)
#     detector = cv2.QRCodeDetector()
#     qr_code_data = None

#     print("🔄 Starting camera. Press 'q' to cancel scanning.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             continue

#         # Detect and decode QR code
#         data, points, _ = detector.detectAndDecode(frame)
#         if data:
#             qr_code_data = data
#             # Draw bounding box if points detected
#             if points is not None:
#                 points = points.astype(int)
#                 n = len(points)
#                 for i in range(n):
#                     pt1 = tuple(points[i][0])
#                     pt2 = tuple(points[(i + 1) % n][0])
#                     cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
#                 cv2.putText(frame, f"QR: {qr_code_data}", (50, 50),
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#             cv2.imshow("QR Code Detected", frame)
#             cv2.waitKey(1500)  # Show result for 1.5 seconds
#             cap.release()
#             cv2.destroyAllWindows()
#             print(f"✅ QR Code detected: {qr_code_data}")
#             return qr_code_data

#         cv2.imshow("Scan QR Code - Press 'q' to cancel", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             print("❌ Scan cancelled.")
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return None