import requests

url = 'https://django-project-tn9e.onrender.com/api/documents/'
files = {
    'file': open("requirements.txt", 'rb')
}

print(files)
data = {
    'property': 'a791dab1-05e2-49f3-b289-5d6fa7daf969',
    'title': 'Sample Document',
    'document_type': 'other'
}

response = requests.post(url, files=files, data=data)
print(response.json())