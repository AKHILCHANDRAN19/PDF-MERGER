from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from PyPDF2 import PdfMerger
import os

class PDFCombinerApp(App):
    def build(self):
        layout = FloatLayout()

        # Background gradient
        with layout.canvas.before:
            Color(0.2, 0.4, 0.6, 1)  # Light blue gradient
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout for widgets
        v_layout = BoxLayout(orientation='vertical', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(v_layout)

        # Label
        self.label = Label(text='Select PDFs', size_hint=(1, 0.1))
        v_layout.add_widget(self.label)

        # FileChooser
        self.filechooser = FileChooserIconView(size_hint=(1, 0.5))
        self.filechooser.multiselect = True
        self.filechooser.bind(selection=self.on_file_select)
        v_layout.add_widget(self.filechooser)

        # Output file name input
        self.output_name_input = TextInput(text='combined.pdf', size_hint=(1, 0.1), multiline=False, hint_text='Enter output file name')
        v_layout.add_widget(self.output_name_input)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.1))
        v_layout.add_widget(button_layout)

        combine_button = Button(text='Combine PDFs', size_hint=(0.5, 1))
        combine_button.bind(on_press=self.combine_pdfs)
        button_layout.add_widget(combine_button)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_file_select(self, *args):
        self.selected_files = self.filechooser.selection
        self.label.text = '\n'.join([os.path.basename(f) for f in self.selected_files])

    def combine_pdfs(self, instance):
        if not self.selected_files:
            self.label.text = 'No PDFs selected!'
            return

        output_name = self.output_name_input.text
        if not output_name.endswith('.pdf'):
            output_name += '.pdf'

        # Directory for saving files
        output_directory = "/storage/emulated/0/Downloads/"
        output_path = os.path.join(output_directory, output_name)

        try:
            # Ensure the directory exists
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            merger = PdfMerger()
            for pdf in self.selected_files:
                if os.path.isfile(pdf):
                    merger.append(pdf)
                else:
                    self.label.text += f'\nFile not found: {pdf}'
            merger.write(output_path)
            merger.close()
            self.label.text = f'PDFs combined successfully! Saved as {output_name}'
        except Exception as e:
            self.label.text = f'Error: {str(e)}'

if __name__ == '__main__':
    PDFCombinerApp().run()
