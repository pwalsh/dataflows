from .format_json import JSONFormat


class GeoJSONFormat(JSONFormat):

    def initialize_file(self, file):
        file.write('{"type": "FeatureCollection","features":')
        super(GeoJSONFormat, self).initialize_file(file)

    def write_transformed_row(self, transformed_row):
        properties = dict()
        geometry = None
        for k, v in transformed_row.items():
            if self.fields[k].type == 'geopoint':
                geometry = dict(
                    type='Point',
                    coordinates=v
                )
            elif self.fields[k].type == 'geojson':
                geometry = v
            else:
                properties[k] = v
        feature = dict(
            geometry=geometry,
            type='Feature',
            properties=properties
        )
        super(GeoJSONFormat, self).write_transformed_row(feature)

    def finalize_file(self):
        super(GeoJSONFormat, self).finalize_file()
        self.writer.write('}')
