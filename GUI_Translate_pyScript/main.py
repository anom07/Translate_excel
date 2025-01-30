import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.uix.button import Button
from deep_translator import GoogleTranslator

class TranslatorApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # File chooser
        self.file_chooser = FileChooserIconView(filters=['*.xlsx'])
        self.add_widget(self.file_chooser)

        # Status label
        self.status_label = Label(text="Select an Excel file to translate.")
        self.add_widget(self.status_label)

        # Translate button
        self.translate_button = Button(text="Translate to Marathi")
        self.translate_button.bind(on_press=self.translate_file)
        self.add_widget(self.translate_button)

    def translate_file(self, instance):
        file_path = self.file_chooser.selection
        if not file_path:
            self.status_label.text = "No file selected. Please choose an Excel file."
            return

        try:
            file_path = file_path[0]
            data = pd.read_excel(file_path)

            # Translate content
            for col in data.columns:
                data[col] = data[col].apply(
                    lambda x: GoogleTranslator(source="auto", target="mr").translate(x) if isinstance(x, str) else x
                )

            # Save translated file
            output_file = file_path.replace(".xlsx", "_translated_marathi.xlsx")
            data.to_excel(output_file, index=False)

            self.status_label.text = f"Translation complete! Saved as {output_file}"
        except Exception as e:
            self.status_label.text = f"Error: {e}"

class MyApp(App):
    def build(self):
        return TranslatorApp()

if __name__ == "__main__":
    MyApp().run()
