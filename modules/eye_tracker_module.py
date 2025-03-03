## 👁 **眼动追踪模块（预留接口）**
class EyeTrackerModule:
    def __init__(self):
        self.tracker = None

    def start_tracking(self):
        print("Eye tracking démarré (placeholder) — futur support MediaPipe")

    def get_gaze_position(self):
        return (0, 0)

    def stop_tracking(self):
        print("Eye tracking arrêté")