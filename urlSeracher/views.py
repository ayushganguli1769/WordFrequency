from django.shortcuts import render
from . models import URL, word
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import os, sys
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
common = os.path.join(dirname, "common_words.txt")
common_word_list = []
with open(common,'r') as f:
    for line in f:
        for word in line.split():
            common_word_list.append(word)
def inputURL(request):
    return render(request,'frequency.html')
def result(request):
    global common_word_list
    print(common_word_list)
    
    if 'searchButton' in request.POST:
        url = request.POST['search']
        if URL.objects.filter(value = url).exists():
            web_url = URL.objects.get(value = url)
            message = "Pre existing URL. No pre-processing done."
            w_val = web_url.value
            return render(request, 'result.html', {'message': message,'web_url':web_url})
        else:
            message = "New URL. Results have been processed just now."
            new_url_object = URL(value = url)
            new_url_object.save()
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            text = (''.join(s.findAll(text=True))for s in soup.findAll('html'))
            c = Counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))
            count = 0
            i = 0
            data = c.most_common()
            print(data[i][0])
            print(data[i][1])
            print(data)
            while (count < 10 and i < len(data) ):
                if data[i][0] not in common_word_list and len(data[i][0]) > 1 and data[i][0].isdigit() == False :
                    word_name = str(data[i][0])
                    frequency = int(data[i][1])
                    new_url_object.word_set.create(word_name = word_name, frequency = frequency)
                    count += 1
                i += 1
            return render(request, 'result.html', {'message': message,'web_url':new_url_object})
    return render(request,'frequency.html')
def home(request):
    return render(request,'base.html')
# Create your views here.
