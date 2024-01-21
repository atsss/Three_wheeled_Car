import argparse
import time

import cv2
import mediapipe as mp
from picamera2 import Picamera2

from led_control import LedControl

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def run(model: str, num_hands: int,
        min_hand_detection_confidence: float,
        min_hand_presence_confidence: float, min_tracking_confidence: float,
        width: int, height: int) -> None:

  # Start capturing video input from the camera
  picam2 = Picamera2()
  picam2.preview_configuration.main.size = (width, height)
  picam2.preview_configuration.main.format = "RGB888"
  picam2.preview_configuration.align()
  picam2.configure("preview")
  picam2.start()

  # LED setup
  led_control = LedControl()

  recognition_result_list = []

  def save_result(result: vision.GestureRecognizerResult,
                  unused_output_image: mp.Image, timestamp_ms: int):
      recognition_result_list.append(result)

  # Initialize the gesture recognizer model
  base_options = python.BaseOptions(model_asset_path=model)
  options = vision.GestureRecognizerOptions(base_options=base_options,
                                          running_mode=vision.RunningMode.LIVE_STREAM,
                                          num_hands=num_hands,
                                          min_hand_detection_confidence=min_hand_detection_confidence,
                                          min_hand_presence_confidence=min_hand_presence_confidence,
                                          min_tracking_confidence=min_tracking_confidence,
                                          result_callback=save_result)
  recognizer = vision.GestureRecognizer.create_from_options(options)

  try:
    # Continuously capture images from the camera and run inference
    while True:
      image = picam2.capture_array()
      image = cv2.flip(image, 1)

      # Convert the image from BGR to RGB as required by the TFLite model.
      rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

      # Run gesture recognizer using the model.
      recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)

      if recognition_result_list:
        # Draw landmarks and write the text for each hand.
        for hand_index, hand_landmarks in enumerate(
            recognition_result_list[0].hand_landmarks):
          # Get gesture classification results
          if recognition_result_list[0].gestures:
            gesture = recognition_result_list[0].gestures[hand_index]
            category_name = gesture[0].category_name

            # Control LED
            current_command = led_control.get_command(category_name)
            led_control.update_led(current_command)
            led_control.prev_command = current_command

        recognition_result_list.clear()
  except KeyboardInterrupt:
    recognizer.close()
    cv2.destroyAllWindows()
    print('interrupted!')

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Name of gesture recognition model.',
      required=False,
      default='gesture_recognizer.task')
  parser.add_argument(
      '--numHands',
      help='Max number of hands that can be detected by the recognizer.',
      required=False,
      default=1)
  parser.add_argument(
      '--minHandDetectionConfidence',
      help='The minimum confidence score for hand detection to be considered '
           'successful.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minHandPresenceConfidence',
      help='The minimum confidence score of hand presence score in the hand '
           'landmark detection.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minTrackingConfidence',
      help='The minimum confidence score for the hand tracking to be '
           'considered successful.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      default=480)
  args = parser.parse_args()

  run(args.model, int(args.numHands), args.minHandDetectionConfidence,
      args.minHandPresenceConfidence, args.minTrackingConfidence,
      args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()
