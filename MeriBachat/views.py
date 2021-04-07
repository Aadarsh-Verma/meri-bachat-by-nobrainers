from django.shortcuts import render
from selenium import webdriver
from lxml import html
from time import sleep


def home(request):
    context = {}
    if request.method == 'POST':
        prd_name = request.POST.get('prd_name')
        amazon = util_amazon(prd_name)
        flipkart = util_flipkart(prd_name)
        tata = util_tatacliq(prd_name)

        context = {
            'amazon': amazon,
            'flipkart': flipkart,
            'tata': tata,
        }
        print(context)
        return render(request, 'products.html', context)
    return render(request, 'index.html', context)


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
