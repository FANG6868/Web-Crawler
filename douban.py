import requests
import parsel
import csv

# Open the file
with open('豆瓣.csv', mode='a', encoding='utf-8', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=[
        '昵称',
        '评分',
        '日期',
        '归属地',
        '评论',
        '有用',
    ])

    csv_writer.writeheader()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    # Loop over each page of comments
    for start in range(0, 200, 10):  # Adjust 200 to suit your needs (number_of_pages * 10)
        url = f'https://movie.douban.com/subject/26928226/comments?start={start}&limit=20&status=P&sort=new_score'

        response = requests.get(url=url, headers=headers)

        selector = parsel.Selector(response.text)
        divs = selector.css('div.comment-item')

        for div in divs:
            name = div.css('.comment-info a::text').get()
            rating = div.css('.rating::attr(title)').get()
            date = div.css('.comment-time ::attr(title)').get()
            area = div.css('.comment-location::text').get()
            short = div.css('.short::text').get().replace('\n', '')
            count = div.css('.vote-count::text').get()

            dit = {
                '昵称': name,
                '评分': rating,
                '日期': date,
                '归属地': area,
                '评论': short,
                '有用': count,
            }

            csv_writer.writerow(dit)

            print(name, rating, date, area, short, count)

