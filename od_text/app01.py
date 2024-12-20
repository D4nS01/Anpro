from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import cv2
import numpy as np

class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.7, 0.3, 1)  # Green color
        self.color = (1, 1, 1, 1)  # White text
        self.bold = True
        self.font_size = '16sp'
        self.size_hint = (None, None)
        self.size = (dp(180), dp(50))
        self.border = (0, 0, 0, 0)

class ModernLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0.9, 0.9, 0.9, 1)  # Light gray text
        self.font_size = '16sp'
        self.bold = True

class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.2, 0.2, 0.2, 1)  # Dark gray background
        self.foreground_color = (1, 1, 1, 1)  # White text
        self.cursor_color = (0.2, 0.7, 0.3, 1)  # Green cursor
        self.font_size = '16sp'
        self.size_hint = (None, None)
        self.size = (dp(300), dp(40))
        self.multiline = False

class ObjectDetectionApp(App):
    def build(self):
        print("Build method called")
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)  # Slightly lighter than the window background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Camera feed
        self.img = Image(size_hint=(1, 0.7), pos_hint={'top': 1})

        # Control panel
        control_panel = BoxLayout(orientation='vertical', size_hint=(1, 0.3), pos_hint={'bottom': 1}, padding=dp(10), spacing=dp(10))

        # Mode switch and label
        switch_layout = BoxLayout(size_hint=(1, None), height=dp(30))
        self.mode_switch = Switch(active=False, size_hint=(None, None), size=(dp(60), dp(30)))
        self.mode_switch.bind(active=self.on_switch_active)
        self.switch_label = ModernLabel(text="All Objects", size_hint=(None, None), size=(dp(120), dp(30)))
        switch_layout.add_widget(self.switch_label)
        switch_layout.add_widget(self.mode_switch)

        # Labels
        self.mode_label = ModernLabel(text="Mode: All objects", size_hint=(1, None), height=dp(30))
        self.object_label = ModernLabel(text="", size_hint=(1, None), height=dp(30))

        # Text input
        self.input_text = ModernTextInput(hint_text="Enter specific object", pos_hint={'center_x': 0.5})
        self.input_text.bind(on_text_validate=self.on_enter)

        # Close button
        self.close_button = ModernButton(text="Close App", on_press=self.close_app, pos_hint={'center_x': 0.5})

        # Add widgets to control panel
        control_panel.add_widget(switch_layout)
        control_panel.add_widget(self.mode_label)
        control_panel.add_widget(self.object_label)
        control_panel.add_widget(self.input_text)
        control_panel.add_widget(self.close_button)

        # Add main components to layout
        self.layout.add_widget(self.img)
        self.layout.add_widget(control_panel)

        # Load COCO class names
        try:
            with open('coco.names.txt', 'r') as f:
                self.class_names = f.read().strip().split('\n')
        except FileNotFoundError:
            print("Error: coco.names.txt file not found")
            self.class_names = []

        # Load model and configuration
        try:
            self.net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
        except cv2.error as e:
            print(f"Error loading model: {e}")
            self.net = None

        # Access camera
        try:
            self.capture = cv2.VideoCapture(0)
            self.capture.set(3, 1080)
            self.capture.set(4, 720)
        except Exception as e:
            print(f"Error accessing camera: {e}")
            self.capture = None

        # Global variables
        self.desired_object = None
        self.detect_single_object = False
        self.input_mode = False

        # Schedule the update function
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return self.layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update(self, dt):
        if self.capture is None or self.net is None:
            return

        ret, frame = self.capture.read()
        if ret:
            height, width = frame.shape[:2]
            center = (width // 2, height // 2)
            square_size = min(width, height) // 4
            square_top_left = (center[0] - square_size // 2, center[1] - square_size // 2)
            square_bottom_right = (center[0] + square_size // 2, center[1] + square_size // 2)

            if self.detect_single_object:
                cv2.rectangle(frame, square_top_left, square_bottom_right, (0, 255, 255), 2)

            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (320, 320), swapRB=True, crop=False)
            self.net.setInput(blob)

            layer_names = self.net.getLayerNames()
            output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            detections = self.net.forward(output_layers)

            boxes = []
            confidences = []
            class_ids = []

            for detection in detections:
                for obj in detection:
                    scores = obj[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.55:
                        center_x = int(obj[0] * width)
                        center_y = int(obj[1] * height)
                        w = int(obj[2] * width)
                        h = int(obj[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.65, 0.4)

            detected_objects = []
            for i in indices:
                i = i[0] if isinstance(i, (list, np.ndarray)) else i
                box = boxes[i]
                x, y, w, h = box
                label = self.class_names[class_ids[i]]

                if not self.detect_single_object or (self.detect_single_object and label == self.desired_object):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label}: {confidences[i]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)
                    detected_objects.append(label)

            mode_text = f"Specific mode: {self.desired_object}" if self.detect_single_object else "all objects"
            cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Update labels
            self.mode_label.text = f"Mode: {'Specific' if self.detect_single_object else 'All objects'}"
            self.object_label.text = f"Detected: {', '.join(detected_objects)}"

            # Convert frame to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = image_texture

    def on_switch_active(self, instance, value):
        if value:
            self.switch_label.text = "Specific Object"
            self.detect_single_object = True
            self.input_mode = True
            self.input_text.text = ""
            self.input_text.focus = True
        else:
            self.switch_label.text = "All Objects"
            self.detect_single_object = False
            self.desired_object = None
            self.input_mode = False
        self.mode_label.text = f"Mode: {'Specific' if self.detect_single_object else 'All objects'}"

    def on_enter(self, instance):
        if self.input_mode:
            self.input_mode = False
            self.desired_object = self.input_text.text if self.input_text.text else None
            self.input_text.text = ""
            self.input_text.focus = False

    def close_app(self, instance):
        if self.capture:
            self.capture.release()
        App.get_running_app().stop()

if __name__ == '__main__':
    try:
        print("Creating ObjectDetectionApp instance...")
        app = ObjectDetectionApp()
        print("ObjectDetectionApp instance created successfully.")
        print("Starting the app...")
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
