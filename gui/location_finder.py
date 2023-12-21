import sys
import googlemaps
import folium
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

#API KEY HANDLER
def configure():
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))



class GoogleMapsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.location_entry = QLineEdit(self)
        self.find_button = QPushButton('Find Location', self)
        self.result_label = QLabel(self)
        self.map_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.location_entry)
        layout.addWidget(self.find_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.map_label)

        self.setLayout(layout)

        self.find_button.clicked.connect(self.find_location)

        self.setWindowTitle('Google Maps App')
        self.setGeometry(100, 100, 800, 600)

    def find_location(self):
        location = self.location_entry.text()

        if not location:
            self.show_message('Warning', 'Please enter a location.')
            return

        # Replace 'YOUR_API_KEY' with your actual Google Maps API key
        api_key = os.getenv('google_maps_api')
        gmaps = googlemaps.Client(key=api_key)

        try:
            geocode_result = gmaps.geocode(location)

            if geocode_result:
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']

                result_text = f"Latitude: {lat}\nLongitude: {lng}"
                self.result_label.setText(result_text)

                # Create a folium map centered on the location
                m = folium.Map(location=[lat, lng], zoom_start=15)

                # Add a marker to the map
                folium.Marker([lat, lng], popup=location).add_to(m)

                # Save the map as an HTML file
                m.save('map.html')

                # Generate an image from the HTML file
                img_path = 'map.png'
                m.save(img_path)

                # Display the image in the QLabel
                pixmap = QPixmap(img_path)
                self.map_label.setPixmap(pixmap)
                self.map_label.setAlignment(Qt.AlignCenter)

            else:
                self.result_label.setText("Location not found.")

        except Exception as e:
            self.show_message('Error', f"Error: {str(e)}")

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()


if __name__ == '__main__':
    configure()
    app = QApplication(sys.argv)
    window = GoogleMapsApp()
    window.show()
    sys.exit(app.exec_())
