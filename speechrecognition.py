import tkinter as tk
import speech_recognition as sr

class AudioToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio to Text Converter")
        
        self.record_button = tk.Button(root, text="Record and Convert", command=self.record_and_convert)
        self.record_button.pack(pady=20)
        
        self.result_label = tk.Label(root, text="", wraplength=300)
        self.result_label.pack()

    def record_and_convert(self):
        self.result_label.config(text="Recording...")

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.result_label.config(text="You said: " + text)
            except sr.WaitTimeoutError:
                self.result_label.config(text="No speech detected.")
            except sr.UnknownValueError:
                self.result_label.config(text="Sorry, could not understand audio.")
            except sr.RequestError as e:
                self.result_label.config(text="Could not request results; {0}".format(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioToTextGUI(root)
    root.mainloop()