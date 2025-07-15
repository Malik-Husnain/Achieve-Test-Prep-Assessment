import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Send credentials to Platzi Fake Store API
        url = 'https://fakestoreapi.com/auth/login'
        payload = {
            'username': username,
            'password': password
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            token = response.json().get('token')
            # Store in session
            request.session['jwt_token'] = token
            request.session['username'] = username

            return redirect('progress')  # ✅ Redirect to course progress page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')



def progress_view(request):
    # 🔐 Check authentication from session
    token = request.session.get('jwt_token')
    username = request.session.get('username')

    if not token or not username:
        return redirect('login')  # user not logged in

    # ✅ Filter by logged-in user's progress, most recent first
    progress_list = UserProgress.objects.filter(username=username).order_by('-last_updated')

    return render(request, 'progress.html', {'progress_list': progress_list})


def logout_view(request):
    request.session.flush()
    return redirect('login')


#API VIEWS

class CourseProgressAPIView(APIView):
    def get(self, request):
        username = request.session.get('username')
        if not username:
            return Response({"error": "Unauthorized"}, status=401)

        queryset = UserProgress.objects.filter(username=username)
        serializer = UserProgressSerializer(queryset, many=True)
        return Response(serializer.data)
    
class BookRecommendationAPIView(APIView):
    authentication_classes = []

    def get(self, request):
        username = request.session.get('username')
        if not username:
            print("⚠️ Unauthorized request — no username in session.")
            return Response({"error": "Unauthorized"}, status=401)

        courses = UserProgress.objects.filter(username=username)
        if not courses.exists():
            print(f"🔍 No courses found for user: {username}")
            return Response([], status=200)

        course_title = courses.first().course
        keyword = course_title.split()[-1]
        

        page = int(request.query_params.get("page", 1))
        per_page = 5
        start = (page - 1) * per_page
        end = start + per_page

        recommendations = []

        # 🔹 GUTENDEX
        gutendex_url = f"https://gutendex.com/books/?search={keyword}&author_year_start=1900&languages=en,fr"
        try:
            response = requests.get(gutendex_url, timeout=5)
            response.raise_for_status()
            books = response.json().get('results', [])
            

            for book in books[start:end]:
                authors = ", ".join([a.get('name', 'Unknown') for a in book.get('authors', [])]) or "Unknown"
                image = book.get('formats', {}).get('image/jpeg', '')
                title = book.get('title', 'Untitled')
                recommendations.append({"authors": authors, "image": image, "title": title})
        except requests.RequestException as e:
            #print("❌ Gutendex API Error:", e)
            pass

        # 🔹 OPENLIBRARY
        openlib_url = f"https://openlibrary.org/search.json?q={keyword}"
        try:
            response = requests.get(openlib_url, timeout=5)
            response.raise_for_status()
            books = response.json().get('docs', [])
            #print(f"✅ OpenLibrary returned {len(books)} books")

            for book in books[start:end]:
                authors = ", ".join(book.get('author_name', ['Unknown']))
                title = book.get('title', 'Untitled')
                cover_id = book.get('cover_i')
                image = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else ''
                recommendations.append({"authors": authors, "image": image, "title": title})
        except requests.RequestException as e:
            #print("❌ OpenLibrary API Error:", e)
            pass

        #print(f"📦 Final recommendations count: {len(recommendations)}")
        return Response(recommendations)


class AddCourseProgressAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.session.get('username')
        if not username:
            return Response({"error": "Unauthorized"}, status=401)

        course_title = request.data.get("title")
        if not course_title:
            return Response({"error": "Course title is required"}, status=400)

        # Check if it already exists
        if UserProgress.objects.filter(username=username, course=course_title).exists():
            return Response({"message": "Course already exists"}, status=200)

        UserProgress.objects.create(
            username=username,
            course=course_title,
            progress=0,
            last_updated=timezone.now()
        )

        return Response({"message": "Course added successfully!"}, status=201)