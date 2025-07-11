from fastapi import UploadFile
from .base_processor import BaseProcessor
from fastkml import kml, KML
from zipfile import ZipFile
import io

class KMLProcessor(BaseProcessor):
    async def process(self, file: UploadFile) -> str:
        try:
            content = await file.read()
            
            kml_doc = None
            if file.filename.lower().endswith('.kmz'):
                with ZipFile(io.BytesIO(content), 'r') as kmz:
                    # Find the KML file in the KMZ archive
                    kml_files = [f for f in kmz.namelist() if f.lower().endswith('.kml')]
                    if not kml_files:
                        raise ValueError("No .kml file found in the KMZ archive.")
                    # Assuming the first KML file is the main one
                    with kmz.open(kml_files[0], 'r') as kml_file:
                        kml_doc = kml_file.read()
            elif file.filename.lower().endswith('.kml'):
                kml_doc = content
            else:
                raise ValueError("Unsupported file type for KMLProcessor.")

            if kml_doc is None:
                raise ValueError("Could not read KML document.")

            k = KML()
            k.from_string(kml_doc)

            features_data = []
            # KML documents can have features in a nested structure.
            # We need to recursively extract them.
            features = list(k.features())
            self._extract_features(features, features_data)
            
            return "\n".join(features_data)

        except Exception as e:
            print(f"Error processing KML/KMZ file: {e}")
            raise

    def _extract_features(self, features, features_data):
        for feature in features:
            if isinstance(feature, kml.Placemark):
                placemark_info = f"Placemark: {feature.name or 'No Name'}"
                if feature.description:
                    placemark_info += f", Description: {feature.description}"
                if feature.geometry:
                    placemark_info += f", Geometry: {feature.geometry.wkt}"
                features_data.append(placemark_info)
            elif isinstance(feature, kml.Folder) or isinstance(feature, kml.Document):
                # Recursively process features within Folders or Documents
                self._extract_features(list(feature.features()), features_data) 