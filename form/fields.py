from django.db import models

class ShowHideDependentCharField(models.CharField):
    def __init__(self,latitude=0.00, longitude=0.00, *args, **kwargs):
        self.latitude = latitude
        self.longitude = longitude
        super(ShowHideDependentCharField, self).__init__(*args, **kwargs)

    def __repr__(self):
        return str(self.latitude) + ',' + str(self.longitude)