import requests
import datetime

# # # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
access_token = 'yZ4syUrBIOlwFr34d1pCuPSRaItCEUYWzqBnMw7K'

def get_group_ids():
    # Make a GET request to the 'me' endpoint
    response = requests.get('https://api.groupme.com/v3/groups', params={'token': access_token})
    # Parse the JSON response and print it
    data = response.json()['response']
    for group in data:
        print(group['id'], group['name'])
    return

def get_most_liked_person(group_id):
    # Dates for analysis
    date1 = datetime.datetime(2021, 1, 1)  # REPLACE with your start date
    date2 = datetime.datetime(2021, 12, 31)  # REPLACE with your end date

    # Dictionary to store total likes for each user
    user_likes = {}
    user_names = {}

    # ID of the last message retrieved
    last_id = None
    # group_id = 
    print("going in")

    while True:
        params = {'token':access_token, 'limit': 100}
        if last_id is not None:
            params['before_id'] = last_id
        response = requests.get(f'https://api.groupme.com/v3/groups/{group_id}/messages', params=params)
        
        if response.status_code != 200:
            print(f'Error: API returned status code {response.status_code}')
            break

        response_json = response.json()
        if 'response' not in response_json or 'messages' not in response_json['response']:
            print('Error: Unexpected response format')
            break

        messages = response_json['response']['messages']

        if not messages:
            break  # No more messages

        for message in messages:
            # Convert the created_at timestamp to a datetime object
            created_at = datetime.datetime.fromtimestamp(message['created_at'])

            # Check if the message was sent between date1 and date2
            if date1 <= created_at <= date2:
                # Add the number of likes the message received to the user's total
                user_likes[message['sender_id']] = user_likes.get(message['sender_id'], 0) + len(message['favorited_by'])
                # Store the user's name
                user_names[message['sender_id']] = message['name']

        # Update the last_id to the ID of the last message in the list
        last_id = messages[-1]['id']

    # Find the user with the most likes
    print('dipping')
    most_likes_id = max(user_likes, key=user_likes.get)
    most_likes = user_likes[most_likes_id]
    most_likes_name = user_names[most_likes_id]

    print(f'The user with the most likes is {most_likes_name} ({most_likes_id}) with {most_likes} likes.')

# get_group_ids()
get_most_liked_person(66677313)

