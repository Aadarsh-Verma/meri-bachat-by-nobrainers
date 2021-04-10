from time import sleep
from selenium import webdriver

thread_data = {}


def full_flipkart(prd_name):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    prd_get_url = 'https://www.flipkart.com/search?q={0}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1'.format(
        prd_name)
    driver.get(prd_get_url)
    sleep(1)

    components = driver.find_elements_by_class_name('_1fQZEK')
    product = []
    hrefs = []
    num = 0
    for component in components:
        hrefs.append(component.get_attribute('href'))
        num += 1
        if num == 2:
            break

    for component in hrefs:
        product_url = component
        driver.get(product_url)

        name = driver.find_element_by_class_name('B_NuCI').text
        category = name.split(" ")[0]
        rating = driver.find_element_by_class_name('_3LWZlK').text
        price = driver.find_element_by_class_name('_16Jk6d').text
        images = driver.find_elements_by_class_name('q6DClP')
        reviews = driver.find_elements_by_class_name('t-ZTKy')
        specs = driver.find_elements_by_class_name('_21Ahn-')

        highlights = []
        for spec in specs:
            highlights.append(spec.text)

        image_url = []
        review = []
        r_limit = 1
        for r in reviews:
            review.append(r.text)
            r_limit += 1
            if r_limit == 4:
                break

        for image in images:
            image_url.append(image.get_attribute('style')[23:-3])
        description = None
        try:
            description = driver.find_elements_by_class_name('_3nkT-2')[0].text[12:]
        except:
            description = None

        context = {
            'category': category,
            'name': name,
            'rating': rating,
            'price': price,
            'images': image_url,
            'reviews': review,
            'specs': highlights,
            'description': description,
            'product_url': product_url,
        }
        product.append(context)
        # print(context)
    driver.close()
    print(product[0])
    return product


def util_flipkart(prd_name):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    url = 'https://www.flipkart.com/search?q=' + prd_name
    driver.get(url)

    sleep(0.2)
    components = driver.find_elements_by_class_name('_1fQZEK')
    context = {}
    for component in components:
        try:
            names = component.find_element_by_class_name('_4rR01T').text
            price = component.find_element_by_class_name('_30jeq3').text[1:]
            context['name'] = names
            context['price'] = price
            break
        except Exception as e:
            print("exc")
            continue
    driver.close()
    thread_data['flipkart'] = context
    return context


def util_tatacliq(prd_name):
    option = webdriver.FirefoxOptions()
    option.headless = True
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=option)
    url = 'https://www.tatacliq.com/search/?searchCategory=all&text=' + prd_name
    driver.get(url)
    sleep(0.2)
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
    thread_data['tata'] = context
    return context


def util_amazon(prd_name):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    url = 'https://www.amazon.in/s?k=' + str(prd_name)
    driver.get(url)
    sleep(0.2)
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
    thread_data['amazon'] = context
    return context


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
        'mobile': mob,
    }
    return context


def get_data_scrape(mob):
    images_list = mob['images']
    images = images_list
    reviews = mob['reviews']
    specs = mob['specs']

    context = {
        'images': images,
        'reviews': reviews,
        'specs': specs,
        'mobile': mob,
    }
    return context
