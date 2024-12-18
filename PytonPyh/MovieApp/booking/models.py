from django.db.models.signals import post_migrate
from django.dispatch import receiver
import qrcode
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_year = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    seat = models.CharField(max_length=10)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate the QR code
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(f"Movie: {self.movie.title}, Seat: {self.seat}, Date: {self.date}")
        qr.make(fit=True)

        # Create the image and save it in memory
        img = qr.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        self.qr_code.save(f"{self.movie.title}_qrcode.png", ContentFile(buffer.read()), save=False)
        buffer.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket for {self.movie.title} (Seat: {self.seat})"



@receiver(post_migrate)
def populate_movies(sender, **kwargs):
    if sender.name == "booking":
        movies = [
            {"title": "Inception", "genre": "Sci-Fi", "release_year": 2020, "price": 10.00},
            {"title": "Avengers: Endgame", "genre": "Action", "release_year": 2021, "price": 12.00},
            {"title": "Dune", "genre": "Sci-Fi", "release_year": 2021, "price": 15.00},
            {"title": "Top Gun: Maverick", "genre": "Action", "release_year": 2022, "price": 14.00},
            {"title": "Spider-Man: No Way Home", "genre": "Action", "release_year": 2023, "price": 13.00},
            {"title": "The Batman", "genre": "Action", "release_year": 2022, "price": 14.50},
            {"title": "Everything Everywhere All At Once", "genre": "Comedy", "release_year": 2022, "price": 10.50},
            {"title": "Tenet", "genre": "Sci-Fi", "release_year": 2020, "price": 11.00},
            {"title": "Black Panther: Wakanda Forever", "genre": "Action", "release_year": 2023, "price": 13.00},
            {"title": "The Whale", "genre": "Drama", "release_year": 2022, "price": 9.00},
            {"title": "Joker", "genre": "Drama", "release_year": 2019, "price": 10.00},
            {"title": "Knives Out", "genre": "Mystery", "release_year": 2019, "price": 8.50},
            {"title": "No Time to Die", "genre": "Action", "release_year": 2021, "price": 11.50},
            {"title": "Soul", "genre": "Animation", "release_year": 2020, "price": 8.00},
            {"title": "Parasite", "genre": "Thriller", "release_year": 2019, "price": 9.50},
            {"title": "1917", "genre": "War", "release_year": 2020, "price": 12.00},
            {"title": "Ford v Ferrari", "genre": "Drama", "release_year": 2019, "price": 10.00},
            {"title": "Frozen II", "genre": "Animation", "release_year": 2019, "price": 7.50},
            {"title": "The Irishman", "genre": "Crime", "release_year": 2019, "price": 9.50},
            {"title": "A Quiet Place Part II", "genre": "Horror", "release_year": 2020, "price": 8.50},
            {"title": "Cruella", "genre": "Comedy", "release_year": 2021, "price": 9.00},
            {"title": "The Lion King", "genre": "Animation", "release_year": 2019, "price": 7.50},
            {"title": "Shang-Chi and the Legend of the Ten Rings", "genre": "Action", "release_year": 2021, "price": 12.00},
            {"title": "The Suicide Squad", "genre": "Action", "release_year": 2021, "price": 11.00},
            {"title": "Doctor Strange in the Multiverse of Madness", "genre": "Action", "release_year": 2022, "price": 13.50},
            {"title": "Encanto", "genre": "Animation", "release_year": 2021, "price": 7.00},
            {"title": "Lightyear", "genre": "Animation", "release_year": 2022, "price": 8.50},
            {"title": "The Northman", "genre": "Adventure", "release_year": 2022, "price": 12.50},
            {"title": "Morbius", "genre": "Sci-Fi", "release_year": 2022, "price": 10.50},
            {"title": "Fantastic Beasts: The Secrets of Dumbledore", "genre": "Fantasy", "release_year": 2022, "price": 11.00},
            {"title": "Eternals", "genre": "Sci-Fi", "release_year": 2021, "price": 12.50},
            {"title": "The Matrix Resurrections", "genre": "Sci-Fi", "release_year": 2021, "price": 13.00},
            {"title": "Uncharted", "genre": "Adventure", "release_year": 2022, "price": 11.50},
            {"title": "The Gray Man", "genre": "Action", "release_year": 2022, "price": 13.00},
            {"title": "Minions: The Rise of Gru", "genre": "Animation", "release_year": 2022, "price": 7.00},
            {"title": "Turning Red", "genre": "Animation", "release_year": 2022, "price": 7.50},
            {"title": "Luca", "genre": "Animation", "release_year": 2021, "price": 8.00},
            {"title": "Black Widow", "genre": "Action", "release_year": 2021, "price": 12.50},
            {"title": "Death on the Nile", "genre": "Mystery", "release_year": 2022, "price": 9.00},
            {"title": "Don't Look Up", "genre": "Comedy", "release_year": 2021, "price": 9.50},
        ]
        for movie in movies:
            Movie.objects.get_or_create(**movie)




