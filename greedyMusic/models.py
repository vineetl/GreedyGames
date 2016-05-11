from django.db import models

class Genre(models.Model):
    Name = models.CharField(max_length=100)
    def __unicode__(self):
        return '%s' % (self.Name)


class Track(models.Model):
    STAR_CHOICES = (
        ('20','1'),
        ('40','2'),
        ('60','3'),
        ('80','4'),
        ('100','5'),
    )
    Title = models.CharField(max_length=100)
    Stars = models.CharField(max_length=3, choices=STAR_CHOICES, blank=False)
    Genres = models.ManyToManyField(Genre)

    def __unicode__(self):
        return '%s' % (self.Title)

'''class Track_Genre_Mapping(models.Model):
    Genre = models.ForeignKey(Track_Genre)
    Title = models.ForeignKey(Track_Details)

    def __unicode__(self):
        return '%s %s' % (self.Genre,self.Title)'''