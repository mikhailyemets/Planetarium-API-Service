import os
from datetime import datetime, timezone
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)
from planetarium.serializers import TicketCreateSerializer


User = get_user_model()




def create_admin_user():
    user = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword'
    )
    return user


def create_user():
    user = User.objects.create_user(
        email='user@example.com',
        password='userpassword'
    )
    return user


def get_user_token():
    client = APIClient()
    response = client.post('/api/user/token/', {
        'email': 'user@example.com',
        'password': 'userpassword'
    })
    return response.data['access']


def get_admin_token():
    client = APIClient()
    response = client.post('/api/user/token/', {
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    return response.data['access']


class ShowThemeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = create_admin_user()
        self.token = get_admin_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.list_url = reverse('planetarium:showtheme-list')
        self.valid_payload = {"name": "StarGazing"}
        self.invalid_payload = {"name": "StarGazing!"}

    def test_create_show_theme_with_valid_payload(self):
        response = self.client.post(self.list_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 1)
        self.assertEqual(ShowTheme.objects.get().name, 'StarGazing')

    def test_create_show_theme_with_invalid_payload(self):
        response = self.client.post(self.list_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShowTheme.objects.count(), 0)

    def test_get_show_theme_list(self):
        ShowTheme.objects.create(name="CosmicShow")
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'CosmicShow')

    def test_delete_show_theme(self):
        show_theme = ShowTheme.objects.create(name="GalacticTour")
        url = reverse('planetarium:showtheme-detail', kwargs={'pk': show_theme.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShowTheme.objects.count(), 0)


class AstronomyShowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = create_admin_user()
        self.token = get_admin_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.theme = ShowTheme.objects.create(name="SpaceExploration")
        self.valid_payload = {
            "title": "Journey to Mars",
            "description": "A thrilling show about Mars exploration",
            "theme": [self.theme.id]
        }
        self.invalid_payload = {
            "title": "Journey tо Mars123",
            "description": "A thrilling show about Mars exploration.",
            "theme": [self.theme.id]
        }
        self.list_url = reverse('planetarium:astronomyshow-list')

    def test_create_astronomy_show_with_valid_payload(self):
        response = self.client.post(self.list_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AstronomyShow.objects.count(), 1)
        self.assertEqual(AstronomyShow.objects.get().title, 'Journey to Mars')

    def test_create_astronomy_show_with_invalid_payload(self):
        response = self.client.post(self.list_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AstronomyShow.objects.count(), 0)

    def test_get_astronomy_show_list(self):
        AstronomyShow.objects.create(title="Galactic Adventure", description="Exploring galaxies far, far away.")
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Galactic Adventure')

    def test_update_astronomy_show(self):
        show = AstronomyShow.objects.create(title="Old Title", description="Old description")
        url = reverse('planetarium:astronomyshow-detail', kwargs={'pk': show.id})
        valid_payload_update = {
            "title": "New Title",
            "description": "New description",
            "theme": [self.theme.id]
        }
        response = self.client.put(url, valid_payload_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        show.refresh_from_db()
        self.assertEqual(show.title, 'New Title')
        self.assertEqual(show.description, 'New description')


class PlanetariumDomeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = create_admin_user()
        self.token = get_admin_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.valid_payload = {
            "name": "Apollo Dome",
            "rows": 10,
            "seats_in_row": 20,
            "price_per_seat": "15.50"
        }
        self.invalid_payload = {
            "name": "Apollo Dome!",
            "rows": -10,
            "seats_in_row": 20,
            "price_per_seat": "15.50"
        }
        self.list_url = reverse('planetarium:planetariumdome-list')

    def test_create_planetarium_dome_with_valid_payload(self):
        response = self.client.post(self.list_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanetariumDome.objects.count(), 1)
        self.assertEqual(PlanetariumDome.objects.get().name, 'Apollo Dome')

    def test_create_planetarium_dome_with_invalid_payload(self):
        response = self.client.post(self.list_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PlanetariumDome.objects.count(), 0)

    def test_get_planetarium_dome_list(self):
        PlanetariumDome.objects.create(name="Orion Dome", rows=25, seats_in_row=30, price_per_seat="20.00")
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Orion Dome')

    def test_update_planetarium_dome(self):
        dome = PlanetariumDome.objects.create(name="Old Name", rows=15, seats_in_row=20, price_per_seat="10.00")
        url = reverse('planetarium:planetariumdome-detail', kwargs={'pk': dome.id})
        valid_payload_update = {
            "name": "New Name",
            "rows": 20,
            "seats_in_row": 25,
            "price_per_seat": "12.00"
        }
        response = self.client.put(url, valid_payload_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dome.refresh_from_db()
        self.assertEqual(dome.name, 'New Name')
        self.assertEqual(dome.rows, 20)
        self.assertEqual(dome.seats_in_row, 25)
        self.assertEqual(dome.price_per_seat, 12.00)

    def test_delete_planetarium_dome(self):
        dome = PlanetariumDome.objects.create(name="Delete Dome", rows=10, seats_in_row=20, price_per_seat="5.00")
        url = reverse('planetarium:planetariumdome-detail', kwargs={'pk': dome.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PlanetariumDome.objects.count(), 0)


class ShowSessionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = create_admin_user()
        self.token = get_admin_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.show_theme = ShowTheme.objects.create(name="Educational")
        self.astronomy_show = AstronomyShow.objects.create(
            title="Test Show",
            description="A test show description."
        )
        self.astronomy_show.theme.add(self.show_theme)

        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Test Dome",
            rows=10,
            seats_in_row=20,
            price_per_seat=Decimal("15.50")
        )

        self.valid_payload = {
            "astronomy_show": self.astronomy_show.id,
            "planetarium_dome": self.planetarium_dome.id,
            "show_time": "2023-10-15T18:00:00Z"
        }

        self.invalid_payload = {
            "astronomy_show": self.astronomy_show.id,
            "planetarium_dome": self.planetarium_dome.id,
            "show_time": "invalid date format"
        }

        self.list_url = reverse('planetarium:showsession-list')

    def test_create_show_session_with_valid_payload(self):
        response = self.client.post(self.list_url, self.valid_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowSession.objects.count(), 1)
        show_session = ShowSession.objects.get()
        self.assertEqual(show_session.astronomy_show, self.astronomy_show)
        self.assertEqual(show_session.planetarium_dome, self.planetarium_dome)
        self.assertEqual(show_session.show_time,
                         datetime(2023, 10, 15, 18, 0, tzinfo=timezone.utc))

    def test_create_show_session_with_invalid_payload(self):
        response = self.client.post(self.list_url, self.invalid_payload,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShowSession.objects.count(), 0)

    def test_get_show_session_list(self):
        ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=datetime(2023, 10, 15, 18, 0, tzinfo=timezone.utc)
        )
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['astronomy_show'],
                         self.astronomy_show.title)
        self.assertEqual(response.data[0]['planetarium_dome'],
                         self.planetarium_dome.name)

    def test_update_show_session(self):
        show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=datetime(2023, 10, 15, 18, 0, tzinfo=timezone.utc)
        )
        url = reverse('planetarium:showsession-detail',
                      kwargs={'pk': show_session.id})
        update_payload = {
            "astronomy_show": self.astronomy_show.id,
            "planetarium_dome": self.planetarium_dome.id,
            "show_time": "2023-10-16T19:00:00Z"
        }
        response = self.client.put(url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        show_session.refresh_from_db()
        self.assertEqual(show_session.show_time,
                         datetime(2023, 10, 16, 19, 0, tzinfo=timezone.utc))

    def test_delete_show_session(self):
        show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time=datetime(2023, 10, 15, 18, 0, tzinfo=timezone.utc)
        )
        url = reverse('planetarium:showsession-detail',
                      kwargs={'pk': show_session.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShowSession.objects.count(), 0)


class ReservationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.token = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_reservation_with_valid_payload(self):
        response = self.client.post(reverse('planetarium:reservation-list'),
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get()
        self.assertEqual(reservation.user, self.user)

    def test_get_reservation_list(self):
        Reservation.objects.create(user=self.user)
        response = self.client.get(reverse('planetarium:reservation-list'),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.email)

    def test_delete_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        url = reverse('planetarium:reservation-detail',
                      kwargs={'pk': reservation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)


class TicketModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.token = get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.theme = ShowTheme.objects.create(name="Test Theme")
        self.show = AstronomyShow.objects.create(title="Test Show", description="Test Description")
        self.show.theme.add(self.theme)
        self.dome = PlanetariumDome.objects.create(name="Test Dome", rows=5, seats_in_row=10, price_per_seat=5.0)
        self.session = ShowSession.objects.create(astronomy_show=self.show, planetarium_dome=self.dome, show_time="2023-01-01 12:00:00")
        self.reservation = Reservation.objects.create(user_id=1)
        self.reservation.refresh_from_db()

    def test_valid_ticket(self):
        ticket = Ticket(row=3, seat=5, show_session=self.session, reservation=self.reservation)
        ticket.clean()
        ticket.save()
        self.assertEqual(Ticket.objects.count(), 1)

    def test_invalid_ticket_row(self):
        with self.assertRaises(ValidationError):
            ticket = Ticket(row=0, seat=5, show_session=self.session, reservation=self.reservation)
            ticket.clean()

    def test_invalid_ticket_seat(self):
        with self.assertRaises(ValidationError):
            ticket = Ticket(row=3, seat=15, show_session=self.session, reservation=self.reservation)
            ticket.clean()

    def test_duplicate_ticket(self):
        data = {
            'row': 3,
            'seat': 5,
            'show_session': self.session.id,
            'reservation': self.reservation.id
        }

        serializer = TicketCreateSerializer(data=data)
        try:
            self.assertTrue(serializer.is_valid())
        except AssertionError:
            print(serializer.errors)
        serializer.save()

        duplicate_serializer = TicketCreateSerializer(data=data)
        self.assertFalse(duplicate_serializer.is_valid())

