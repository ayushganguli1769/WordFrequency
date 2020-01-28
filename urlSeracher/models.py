from django.db import models
class URL(models.Model):
    value = models.CharField(max_length= 450, null= True, blank= True)
    def __str__(self):
        return self.value
class word(models.Model):
    url = models.ForeignKey(URL, on_delete = models.CASCADE)
    word_name = models.CharField(max_length= 450, null= True, blank= True)
    frequency = models.IntegerField(null= True)
    def __str__(self):
        return self.word_name + " - URL -"+ str(self.url.id)
