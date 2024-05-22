# from langchain.chat_models import ChatOpenAI
import os
import json
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "Your Key"

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)

function_descriptions_multiple = [
    {
        "name": "search_books",
        "description": "Search for books based on various criteria",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the book, e.g. 'To Kill a Mockingbird'",
                },
                "author": {
                    "type": "string",
                    "description": "The author of the book, e.g. 'Harper Lee'",
                },
                "genre": {
                    "type": "string",
                    "description": "The genre of the book, e.g. 'Fiction'",
                },
                "isbn": {
                    "type": "string",
                    "description": "The ISBN number of the book, e.g. '978-0-06-112008-4'",
                },
            },
            "required": ["title", "author"],
        },
    },
    {
        "name": "purchase_book",
        "description": "Purchase a book based on book information",
        "parameters": {
            "type": "object",
            "properties": {
                "book_id": {
                    "type": "string",
                    "description": "The unique identifier for the book, e.g. '123456'",
                },
                "title": {
                    "type": "string",
                    "description": "The title of the book, e.g. 'To Kill a Mockingbird'",
                },
                "author": {
                    "type": "string",
                    "description": "The author of the book, e.g. 'Harper Lee'",
                },
                "quantity": {
                    "type": "integer",
                    "description": "The number of copies to purchase, e.g. 2",
                },
                "payment_method": {
                    "type": "string",
                    "description": "The method of payment, e.g. 'credit_card'",
                },
                "shipping_address": {
                    "type": "string",
                    "description": "The address where the book will be shipped, e.g. '123 Main St, Anytown, USA'",
                },
            },
            "required": ["title", "author", "quantity", "payment_method", "shipping_address"],
        },
    },
    {
        "name": "submit_review",
        "description": "Submit a review for a book",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the book, e.g. 'To Kill a Mockingbird'",
                },
                "author": {
                    "type": "string",
                    "description": "The author of the book, e.g. 'Harper Lee'",
                },
                "user_name": {
                    "type": "string",
                    "description": "The name of the user submitting the review, e.g. 'Jane Doe'",
                },
                "rating": {
                    "type": "integer",
                    "description": "The rating given to the book, e.g. 4",
                },
                "review_text": {
                    "type": "string",
                    "description": "The text of the review, e.g. 'A captivating read from start to finish!'",
                },
            },
            "required": ["title", "author", "user_name", "rating", "review_text"],
        },
    }
]


def ask_and_reply(prompt):
    """Give LLM a given prompt and get an answer."""

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": prompt}],
    # add function calling
    functions=function_descriptions_multiple,
    function_call="auto",  # specify the function call
    )

    print(f'User Prompt: {prompt}')
    print(f'Function: {response.choices[0].message.function_call.name}')
    output = json.loads(response.choices[0].message.function_call.arguments)
    print(f'Type: {type(output)}')
    print(f'JSON response: {output}')
    print(f'Total Tokens used: {response.usage.total_tokens}\n')

# Scenario 1: Search Books
search_book = """Where is the novel The Silent Patient by Alex Michaelides,
               which is of the genere psychological thriller
               and has number 123-0-12-112008-4?"""
ask_and_reply(search_book)


# Scenario 2: Purchase Book
purchase_book = """i would like to buy The Silent Patient ,book id is 194712,
               i would like to pay via UPI, my UPI id is user@paytm
               and deliver it to my address 123 street, Udaipur, Rajasthan"""
ask_and_reply(purchase_book)


# Scenario 2: Submit a review
submit_review = """Review - Alex Michaelides' "The Silent Patient" is a captivating suspense novel that kept me guessing until the last chapter. The storyline is skillfully written with unexpected surprises and complex characters. Michaelides explores the depths of the human mind, offering an insightful and thrilling read—a must-have for any avid reader seeking an emotional rollercoaster.
                    definitely worthy of 5 stars.
                    by User123"""
ask_and_reply(submit_review)