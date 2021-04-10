from concurrent.futures.thread import ThreadPoolExecutor
import threading
from django.shortcuts import render
from src.models import Mobile
import time
from src.scrapes import util_amazon, util_flipkart, util_tatacliq, thread_data, full_flipkart, get_data, get_data_scrape


def compare_util(request, name):
    tick = time.time()
    t1 = threading.Thread(target=util_amazon, args=[name])
    t2 = threading.Thread(target=util_flipkart, args=[name])
    t3 = threading.Thread(target=util_tatacliq, args=[name])
    try:
        t1.start()
    except:
        amazon = None
    try:
        t2.start()
    except:
        flipkart = None
    try:
        t3.start()
    except:
        tata = None
    t1.join()
    t2.join()
    t3.join()

    print(thread_data)

    context = {
        'thread_data': thread_data,
        'prd_name': name,
        'time_taken': time.time() - tick,
    }
    return render(request, 'compare.html', context)


def compare(request, name):
    name_amazon = name
    name_flikart = name
    name_tata = name
    tick = time.time()
    executor = ThreadPoolExecutor()
    try:
        task1 = executor.submit(util_amazon, name_amazon)
        amazon = task1.result()
    except:
        amazon = None
    try:
        task2 = executor.submit(util_flipkart, name_flikart)
        flipkart = task2.result()
    except:
        flipkart = None
    try:
        task3 = executor.submit(util_tatacliq, name_tata)
        tata = task3.result()
    except:
        tata = None

    compare_context = {
        'amazon': amazon,
        'flipkart': flipkart,
        'tata': tata,
        'prd_name': name,
        'time_taken': time.time() - tick,
    }
    return render(request, 'compare.html', compare_context)


def home(request):
    # Product List
    if request.method == 'POST':
        prd_name_list = request.POST.get('prd_name')
        # category = request.POST.get('category')
        if prd_name_list:
            print("inside product list")
            mobiles = Mobile.objects.filter(name__icontains=prd_name_list)

            if len(mobiles) != 0:
                print("Inside DB")
                metadata = []
                for mobile in mobiles:
                    metadata.append(get_data(mobile))
                context = {
                    'mobiles': mobiles,
                    'metadata': metadata,
                }
                # print(context)
            else:
                scrape_products = full_flipkart(prd_name_list)
                metadata = []
                mobiles = []
                temp = []

                for scrape in scrape_products:
                    temp.append(get_data_scrape(scrape))
                    mobiles.append(create_product(temp[-1]))
                    for mobile in mobiles:
                        metadata.append(get_data(mobile))
                context = {
                    'mobiles': mobiles,
                    'metadata': metadata,
                }

        return render(request, 'product-list.html', context)
    return render(request, 'index.html', {})


def create_product(meta):
    # print(meta)
    return Mobile.objects.create(name=meta['mobile']['name'], category=meta['mobile']['category'],
                                 price=meta['mobile']['price'], product_url=meta['mobile']['product_url'],
                                 reviews=str(meta['reviews']),
                                 description=meta['mobile']['description'], specs=str(meta['specs']),
                                 images=str(meta['images']))


def index(request, pk):
    mobiles = Mobile.objects.get(pk=pk)
    metadata = get_data(mobiles)
    context = {
        'mobiles': mobiles,
        'metadata': metadata,
    }
    return render(request, 'product-detail.html', context)
