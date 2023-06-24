def build_recognition_service():
    from infrastructure.detection import YOLODetector
    from infrastructure.activity_detection import ActivityDetector
    from service.recognition import RecognitionService

    detector = YOLODetector(
        model_path="models/detector.pt", conf_thresh=0.6, device="cuda:0"
    )
    activity_detector = ActivityDetector()
    service = RecognitionService(detector, activity_detector)
    return service
