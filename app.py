
import requests
import json
import csv

MEDIUM = 'https://medium.com'


def clean_json_response(response):
    return json.loads(response.text.replace('])}while(1);</x>', '', 1))


# Returns the User ID of a Medium Username
def get_user_id(username):

    print('Retrieving user ID...')

    url = MEDIUM + '/@' + username + '?format=json'
    response = requests.get(url)
    response_dict = clean_json_response(response)
    return response_dict['payload']['user']['userId']


#Returns followers
def get_followers(username):

    print('Followers for %s...' % username)

    user_id = get_user_id(username)

    return user_id


def main():
    name="krishsaran"
    interesting_users = get_followers(name)
    print(interesting_users)

if __name__ == '__main__':
    main()