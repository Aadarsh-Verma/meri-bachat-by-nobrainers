from time import sleep
from selenium import webdriver
from fuzzywuzzy import process

thread_data = {}


def full_flipkart(prd_name):
    prd_name = str(prd_name)
    option = webdriver.ChromeOptions()
    option.headless = True
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
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
        if num == 3:
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


def fuzzy(string1, list1):
    string1 = [string1]
    Ratios = [process.extract(x, list1) for x in string1]
    ans = []
    for ratio in Ratios:
        ans.append(ratio)
    # print(ans[0][0][0])

    index = 0
    for i in range(0, len(list1)):
        if str(list1[i]) == str(ans[0][0][0]):
            index = i
            break
    return index


def util_flipkart(prd_name):
    print("Product name is " + prd_name)
    prd_name = str(prd_name)
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    url = 'https://www.flipkart.com/search?q=' + prd_name
    driver.get(url)

    sleep(0.2)
    components = driver.find_elements_by_class_name('_1fQZEK')
    context = {}
    fuzzy_names = []
    for component in components:
        try:
            names = component.find_element_by_class_name('_4rR01T').text
            fuzzy_names.append(names)
        except:
            continue
    index = fuzzy(prd_name, fuzzy_names)
    try:
        names = components[index].find_element_by_class_name('_4rR01T').text
        price = components[index].find_element_by_class_name('_30jeq3').text[1:]
        prd_link = components[index].get_attribute('href')
        context['name'] = names
        context['price'] = price
        context['prd_link'] = prd_link

    except:
        for component in components:
            try:
                names = component.find_element_by_class_name('_4rR01T').text
                price = component.find_element_by_class_name('_30jeq3').text[1:]
                prd_link = component.get_attribute('href')
                context['name'] = names
                context['price'] = price
                context['prd_link'] = prd_link
                # print(context)
                break
            except Exception as e:
                print("exc")
                continue

    driver.close()
    thread_data['flipkart'] = context
    return context


def util_tatacliq(prd_name):
    prd_name = str(prd_name)
    option = webdriver.FirefoxOptions()
    option.headless = True
    driver = webdriver.Firefox(executable_path='geckodriver.exe', options=option)
    url = 'https://www.tatacliq.com/search/?searchCategory=all&text=' + prd_name
    driver.get(url)
    sleep(0.2)
    components = driver.find_elements_by_class_name('ProductModule__base')
    print("length of component in tata cliq is" + str(len(components)))
    if len(components) == 0:
        thread_data['error_tata'] = 'Product Not Available'
        return {}
    context = {}
    fuzzy_names = []
    for component in components:
        try:
            names = component.find_element_by_class_name('ProductDescription__description').text
            fuzzy_names.append(names)
        except:
            continue
    index = fuzzy(prd_name, fuzzy_names)
    try:
        names = components[index].find_element_by_class_name('ProductDescription__description').text
        price = components[index].find_element_by_class_name('ProductDescription__discount').text
        context['name'] = names
        context['price'] = price

    except Exception as e:
        print("exception occured in tata cliz" + str(e))
        for component in components:
            try:
                names = component.find_element_by_class_name('ProductDescription__description').text
                price = component.find_element_by_class_name('ProductDescription__discount').text
                context['name'] = names
                context['price'] = price
                print(context)
                break
            except Exception as e:
                print("exception occured in tata cliq" + str(e))
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
    components = driver.find_elements_by_class_name('s-result-item')
    context = {}
    fuzzy_names = []
    print('length of componenet in amazon is' + str(len(components)))
    for component in components:
        try:
            div = component.find_element_by_class_name('sg-col-inner')
            spans = div.find_elements_by_tag_name('h2')
            name = spans[0].text
            fuzzy_names.append(name)
        except:
            continue
    index = fuzzy(prd_name, fuzzy_names)
    print(str(fuzzy_names))
    print("the fuzzy answer is " + str(fuzzy_names[index]))
    try:
        div = components[index].find_element_by_class_name('sg-col-inner')
        spans = div.find_elements_by_tag_name('h2')
        name = spans[0].text
        price = components[index].find_element_by_class_name('a-price-whole').text
        # print(str(name) + "=>" + str(price))
        context['name'] = name
        context['price'] = price
    except:
        print("amazon => could not get the index product")
        for component in components:
            try:
                div = component.find_element_by_class_name('sg-col-inner')
                spans = div.find_elements_by_tag_name('h2')

                name = spans[0].text
                price = component.find_element_by_class_name('a-price-whole').text
                # print(str(name) + "=>" + str(price))
                context['name'] = name
                context['price'] = price

            except Exception as e:
                print("exc")

    thread_data['amazon'] = context
    return context


def get_data(mob):
    image_list = mob.images
    images_list = image_list[1:-1].split(",")
    images = [images_list[0][1:-1].replace('image/128/128', 'image/416/416')]
    for i in range(1, len(images_list)):
        images.append(images_list[i][2:-1].replace('image/128/128', 'image/416/416'))

    reviews = mob.reviews[1:-1].split(",")
    temp_specs = mob.specs[1:-1].split(",")
    specs = [temp_specs[0][1:-1]]
    for i in range(1, len(temp_specs)):
        specs.append(temp_specs[i][2:-1])
    context = {
        'images': images,
        'reviews': reviews,
        'specs': specs,
        'mobile': mob,
    }
    return context


def get_data_scrape(mob):
    images_list = mob['images']
    images = []
    for image in images_list:
        images.append(image.replace('image/128/128', 'image/416/416'))
    reviews = mob['reviews']
    specs = mob['specs']

    context = {
        'images': images,
        'reviews': reviews,
        'specs': specs,
        'mobile': mob,
    }
    return context
