def build_recognition_service():
    from infrastructure.detection import YOLODetector
    from infrastructure.classification import DummyClassifier
    from service.recognition import RecognitionService

    detector = YOLODetector(model_path="models/detector.pt", conf_thresh=0.6)
    service = RecognitionService(detector)
    return service
