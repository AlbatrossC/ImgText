import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract as tess
import openai
import time

class ImageUploaderApp:
    def __init__(self, main):
        self.main = main
        self.main.title("Food Ingredients Info")
        
        self.background_color = "#8c8c8c"
        self.button_color = "#4CAF50"
        self.text_color = "#333333"
        self.font_style = ("Helvetica", 10)
        
        self.main.configure(bg=self.background_color)
        
        self.create_widgets()

    def create_widgets(self):
        self.image_label = tk.Label(self.main, bg="white", bd=100, relief="ridge")
        self.image_label.pack(pady=10)
        
        self.text_frame = tk.Frame(self.main, bg=self.background_color)
        self.text_frame.pack(pady=5, fill="both", expand=True)
        
        self.text_label = tk.Text(self.text_frame, wrap="word", font=self.font_style)
        self.text_label.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_label.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_label.config(yscrollcommand=self.scrollbar.set)
        
        button_style = {"font": self.font_style, "padx": 10, "pady": 5, "bg": self.button_color, "fg": "white", "bd": 0}
        
        self.upload_button = tk.Button(self.main, text="Upload Image", command=self.upload_image, **button_style)
        self.upload_button.pack(pady=5)
        
        self.clear_button = tk.Button(self.main, text="Clear Image", command=self.clear_image, **button_style)
        self.clear_button.pack(pady=5)
        
        self.image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((500, 500))  
            self.render_image()
            self.perform_ocr()

    def render_image(self):
        if self.image:
            img = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=img)
            self.image_label.image = img  
        else:
            self.image_label.config(image="")

    def clear_image(self):
        self.image = None
        self.text_label.delete("1.0", tk.END)
        self.render_image()

    def perform_ocr(self):
        if self.image:
            grayscale_image = self.image.convert("L")
            text = tess.image_to_string(grayscale_image)
            
            if text:
                self.update_text("Extracted Text:\n" + text)
                self.check_food_safety(text)
            else:
                self.update_text("No text extracted.")

    def check_food_safety(self, text):
        obj = text
        messages = [
            {"role": "system", "content": "Answer in this format. new line by line.Analyzing your product: [product name], - [List of ingredients].Common names of ingredients: [Common names of each ingredient] ,Function of ingredients: After listing the common names, briefly explain the function of each ingredient. For example, [sugar (sweetener),] [salt (flavor enhancer),][cornstarch (thickener),] etc. Dietary considerations: Indicate any allergens (soy, wheat, peanuts, etc.) or other dietary restrictions (gluten-free, vegan, etc.) based on the ingredients.Nutrient content: While a full nutritional breakdown might be beyond the scope, you can mention key nutrients like Vitamin C, fiber, or protein content based on the ingredients.Sugar content: Highlight the amount of added sugar (if any) as this can be a concern for many consumers.Intake of the product: [Based on the ingredients, suggest a recommended serving size or frequency of consumption]. This will depend on the product type and its overall nutritional profile.Safety assessment: [Whether the product is safe to consume or not] Phrased cautiously, mentioning if there are any ingredients that might be a concern for certain individuals (e.g., lactose intolerance for dairy products)."},
            {"role": "user", "content":  obj }
        ]
        self.update_text("Food Safety Assessment: Analyzing ingredients for food safety. Please wait...")
        
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=450,
            temperature=0.5
        )

        response = chat.choices[0].message.content.strip()
        self.update_text(response)

    def update_text(self, text, fg=None):
        self.text_label.insert(tk.END, text + "\n")
        if fg:
            self.text_label.tag_add("color", "1.0", tk.END)
            self.text_label.tag_config("color", foreground=fg)

def main():
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    tess.pytesseract.tesseract_cmd = r'C:/Users/Soham/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    openai.api_key = "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"
    main()
