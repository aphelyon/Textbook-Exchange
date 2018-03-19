from django.db import models
from datetime import datetime


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=100, unique=True)
    userJoined = models.DateTimeField('User joined on this date')

    # Maybe edit this to give the password? Not sure
    def as_json(self):
        return dict(first_name=self.first_name, last_name=self.last_name, username=self.username, email=self.email,
                    userJoined=str(self.userJoined), pk=str(self.pk))


class Professor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)

    def as_json(self):
        if self.email is not None:
            return dict(name=self.name, email=self.email, pk=str(self.pk))
        else:
            return dict(name=self.name, pk=str(self.pk))


class Course(models.Model):
    identifier = models.CharField(max_length=32)
    department = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    viewed_count = models.IntegerField(default=0)

    def as_json(self):
        if self.professor is not None:
            return dict(identifier=self.identifier, department=self.department, professor=self.professor.as_json(), name=self.name, pk=str(self.pk), viewed_count=self.viewed_count)
        else:
            return dict(identifier=self.identifier, department=self.department, name=self.name, pk=str(self.pk), viewed_count=self.viewed_count)


class Textbook(models.Model):
    item_title = models.CharField(max_length=200)
    item_author = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    item_ISBN = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    """Return a dictionary containing each component of the model with its respective label"""
    def as_json(self):
        if self.course is not None:
            return dict(title=self.item_title, author=self.item_author, course=self.course.as_json(), ISBN=self.item_ISBN,
                        pub_date=str(self.pub_date), pk=str(self.pk))
        else:
            return dict(title=self.item_title, author=self.item_author, ISBN=self.item_ISBN, pub_date=str(self.pub_date),
                        pk=str(self.pk))


class Listing(models.Model):
    item = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    price_text = models.CharField(max_length=200)
    actualprice = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition_of_textbook = (
            ('NEW', 'Brand new, unused Textbook'),
            ('USED_GOOD', 'Used, in good condition'),
            ('USED_OKAY', 'Used, in okay condition'),
            ('USED_POOR', 'Used, in poor condition')
            )
    condition = models.CharField(max_length=20, choices=condition_of_textbook, default='NEW')
    status_of_listing = (
            ('For Sale', 'For Sale'),
            ('Negotiation', 'Under Negotiation'),
            ('Sold', 'Sold')
            )
    status = models.CharField(max_length=20, choices=status_of_listing, default='For Sale')
    viewed_count = models.IntegerField(default=0)
    time_created = models.DateTimeField('Listing was created on this date', null=True)

    def as_json(self):
        return dict(item=self.item.as_json(), price_text=self.price_text, actualprice=self.actualprice,
                    user=self.user.as_json(), condition=self.condition, status=self.status, pk=str(self.pk),
                    viewed_count=self.viewed_count, time_created=self.time_created)


class Authenticator(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    authenticator = models.CharField(max_length=64, primary_key=True)
    date_created = models.DateTimeField(default=datetime.now)
