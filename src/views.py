from django.shortcuts import render
from selenium import webdriver
from time import sleep

from src.models import Mobile


def get_data(mob):
    image_list = mob.images
    images_list = image_list[1:-1].split(",")
    images = [images_list[0][1:-1]]
    for i in range(1, len(images_list)):
        images.append(images_list[i][2:-1])

    reviews = mob.reviews[1:-1].split(",")
    specs = mob.specs[1:-1].split(",")

    context = {
        'images': images,
        'reviews': reviews,
        'specs': specs,
        'mobile':mob
    }
    return context


def home(request):
    context = {}
    if request.method == 'POST':
        print("post recieved from home")
        prd_name = request.POST.get('prd_name')

        if prd_name:
            amazon = util_amazon(prd_name)
            flipkart = util_flipkart(prd_name)
            tata = util_tatacliq(prd_name)

            context = {
                'amazon': amazon,
                'flipkart': flipkart,
                'tata': tata,

            }
            # print(context)
            return render(request, 'products.html', context)

    return render(request,'index.html',{})

def list_form(request):
    # Product List
    if request.method == 'POST':
        prd_name_list = request.POST.get('prd_name')
        category = request.POST.get('category')
        if prd_name_list and category:
            print("inside product list")
            mobiles = Mobile.objects.filter(name__icontains=prd_name_list)
            metadata = []
            for mobile in mobiles:
                metadata.append(get_data(mobile))
            context = {
                'mobiles': mobiles,
                'metadata': metadata,
            }
            # print(context)
            return render(request,'product-list.html',context)
    return render(request, 'product_list_form.html', {})

def index(request,pk):
    mobiles = Mobile.objects.get(pk=pk)
    metadata = get_data(mobiles)

    context = {
        'mobiles': mobiles,
        'metadata': metadata,
    }
    return render(request, 'product-detail.html', context)


def util_amazon(prd_name):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    url = 'https://www.amazon.in/s?k=' + str(prd_name)
    driver.get(url)
    sleep(1)
    # tree = html.fromstring(driver.page_source)
    print("inside driver")
    titles = driver.find_elements_by_class_name('s-result-item')
    context = {}
    for title in titles:
        try:
            div = title.find_element_by_class_name('sg-col-inner')
            spans = div.find_elements_by_tag_name('h2')

            name = spans[0].text
            price = title.find_element_by_class_name('a-price-whole').text
            print(str(name) + "=>" + str(price))
            context['name'] = name
            context['price'] = price
            break
        except Exception as e:
            print("exc")
            continue
    return context


def util_flipkart(prd_name):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    url = 'https://www.flipkart.com/search?q=' + prd_name
    driver.get(url)

    sleep(1)
    components = driver.find_elements_by_class_name('_1fQZEK')
    context = {}
    for component in components:
        try:
            names = component.find_element_by_class_name('_4rR01T').text
            price = component.find_element_by_class_name('_30jeq3').text
            context['name'] = names
            context['price'] = price
            break
        except Exception as e:
            print("exc")
            continue
    driver.close()
    return context


def util_tatacliq(prd_name):
    option = webdriver.FirefoxOptions()
    option.headless = True
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=option)
    url = 'https://www.tatacliq.com/search/?searchCategory=all&text=' + prd_name
    driver.get(url)
    sleep(1)
    components = driver.find_elements_by_class_name('ProductModule__base')
    context = {}
    for component in components:
        try:
            names = component.find_element_by_class_name('ProductDescription__description').text
            price = component.find_element_by_class_name('ProductDescription__discount').text
            context['name'] = names
            context['price'] = price
            break
        except Exception as e:
            print("exception occured")
            continue

    driver.close()
    return context
