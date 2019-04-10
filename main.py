from dotenv import load_dotenv
from os import getenv
from os.path import join
from os import getcwd
from post_to_vk import create_post_on_vk
from post_to_telegram import create_post_on_telegtam
from post_to_facebook import create_post_on_fb
from google_sheets import fetch_sheet_rows
from google_sheets import get_id
from google_sheets import fetch_files
from google_sheets import fetch_updated_sheet_rows
import datetime
from time import sleep

#
# def verification_of_publication_conditions(row_with_article):
#     if


def get_article_for_publication(sheet_rows):
    index_for_publication_status = 7
    index_for_weekday = 3
    index_for_time = 4
    unpublished_status = 'нет'
    now = datetime.datetime.now()
    present_weekday = now.weekday()
    present_hour = now.hour

    week = [
        'понедельник',
        'вторник',
        'среда',
        'четверг',
        'пятница',
        'суббота',
        'воскресенье'
    ]

    rows_with_articles_published_today = [
        (counter, row) for counter, row in sheet_rows
        if week[present_weekday] == row[index_for_weekday]
    ]
    rows_with_unpublished_articles = [
        (counter, row) for counter, row in rows_with_articles_published_today
        if unpublished_status == row[index_for_publication_status]
    ]
    rows_with_articles_for_publication_now = [
        (counter, row) for counter, row in rows_with_unpublished_articles
        if present_hour == row[index_for_time]
    ]
    if rows_with_articles_for_publication_now:
        return rows_with_articles_for_publication_now


def create_posts(path_to_picture, message, article):
    if article[0] == 'да':
        create_post_on_vk(path_to_picture, message)
    if article[1] == 'да':
        create_post_on_telegtam(path_to_picture, message)
    if article[2] == 'да':
        create_post_on_fb(path_to_picture, message)


def main():
    load_dotenv(join(getcwd(), '.env'))
    sheet_id = getenv('SHEET_ID')
    sheet_rows = fetch_sheet_rows(sheet_id)

    while True:
        rows_with_articles_for_publication = get_article_for_publication(sheet_rows)
        if rows_with_articles_for_publication is None:
            sleep(360)
            continue
        index_for_image_hyperlink = 6
        index_for_text_hyperlink = 5
        image_hyperlink = rows_with_articles_for_publication[1][index_for_image_hyperlink]
        text_hyperlink = rows_with_articles_for_publication[1][index_for_text_hyperlink]
        image_id = get_id(image_hyperlink)
        text_id = get_id(text_hyperlink)
        image_title, text_title = fetch_files(image_id, text_id)

        path_to_picture_for_posting = join(getcwd(), image_title)
        with open(text_title, 'r') as file:
            message = file.read()
        create_posts(path_to_picture_for_posting, message, rows_with_articles_for_publication[1])
        sheet_rows = fetch_updated_sheet_rows(sheet_id, rows_with_articles_for_publication)


if __name__ == '__main__':
    main()
