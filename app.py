
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

# Returns the upvotes for a medium post
def get_upvotes_for_post(post_id):

    url = MEDIUM + '/p/' + post_id + '/upvotes?format=json'
    response = requests.get(url)
    response_dict = clean_json_response(response)
    upvotes = []
    for user in response_dict['payload']['value']['users']:
        upvotes.append((user['userId'],user['createdAt']))
    return upvotes

#Returns [(tag,endorsee,endorser,endorsedAt,facebookID)]
def get_endorser_endorsee_map(username):

    print('Retrieving the latest posts...')
    tags =set()
    url = MEDIUM + '/@' + username + '/latest?format=json'
    response = requests.get(url)
    response_dict = clean_json_response(response)
    res = []
    user_id = get_user_id(username)

    try:
        posts = response_dict['payload']['references']['Post']
    except:
        posts = []

    if posts:
        print('Retrieving the upvotes...')
        print('Constructing the map...')
        for key in posts.keys():
            for pair in get_upvotes_for_post(posts[key]['id']):
                for tag in posts[key]['virtuals']['tags']:
                    res.append((tag['slug'],user_id,pair[0],pair[1]))
    return res


#Returns followers
def get_followers(username):

    print('Followers for %s...' % username)
    user_id = get_user_id(username)
    return user_id

#Writes output to a file
def write_to_csv(get_endorser_endorsee_map):

    with open('output.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(get_endorser_endorsee_map)

def main():
    
    name="karpathy"
    user_id = get_user_id(name)
    print(user_id) 
    print(get_endorser_endorsee_map(name))

if __name__ == '__main__':
    main()