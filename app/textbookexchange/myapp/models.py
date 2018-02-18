from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=100)
    userJoined = models.DateTimeField('User joined on this date')

    # Maybe edit this to give the password? Not sure
    def as_json(self):
        return dict(first_name=self.first_name, last_name=self.last_name, username=self.username, email=self.email,
                    userJoined=str(self.userJoined),pk=str(self.pk))


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
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Textbook(models.Model):
    item_title = models.CharField(max_length=200)
    item_author = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    item_ISBN = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    """Return a dictionary containing each component of the model with its respective label"""
    def as_json(self):
        if self.course is not None:
            return dict(title=self.item_title, author=self.item_author, course=self.course, ISBN=self.item_ISBN,
                        pub_date=str(self.pub_date), pk=str(self.pk))
        else:
            return dict(title=self.item_title, author=self.item_author, ISBN=self.item_ISBN, pub_date=str(self.pub_date),
                        pk=str(self.pk))

    

class Listing(models.Model):
    item = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    price_text = models.CharField(max_length=200)
    actualprice = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition_of_textbook = (
            ('NEW', 'Brand new, unused Textbook'),
            ('USED_GOOD', 'Used, in good condition'),
            ('USED_OKAY', 'Used, in okay condition'),
            ('USED_POOR', 'Used, in poor condition')
            )
    condition = models.CharField(max_length=20, choices=condition_of_textbook, default = 'NEW')
    status_of_listing = (
            ('For Sale', 'For Sale'),
            ('Negotiation', 'Under Negotiation'),
            ('Sold', 'Sold')
            )
    status = models.CharField(max_length=20, choices=status_of_listing, default = 'For Sale')

# Create your models here.
