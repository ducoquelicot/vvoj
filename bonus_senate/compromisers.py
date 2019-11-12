'''

Script dat werkt met de ProPublica Congress API. Gebruikt deze om voor de Dems en GOPs de top vijf politici op te lijsten die het minst vaak met hun partij meestemmen. 

'''

import os
import requests

def main():
    url = 'https://api.propublica.org/congress/v1/116/senate/members.json'
    key = {"X-API-Key": os.environ['PP_API']}
    response = requests.get(url, headers=key)
    members = response.json()

    senators = []

    for row in members['results']:
        for member in row['members']:
            senators.append(member)

    for row in senators:
        dems_five = sorted(senators, key = sort_dems)[:5]
        reps_first = sorted(senators, key = sort_reps)
        reps_five = sorted(reps_first, key = reps_vote, reverse = True)[:5]

    dem_outcome = "Democrats lowest party vote:\n"

    for row in dems_five:
        line = "{} {}, {}, {}\n".format(row['first_name'], row['last_name'], row['state'], row['votes_with_party_pct'])
        dem_outcome += line

    rep_outcome = "Republicans lowest party vote:\n"

    for row in reps_five:
        line = "{} {}, {}, {}\n".format(row['first_name'], row['last_name'], row['state'], row['votes_with_party_pct'])
        rep_outcome += line


    print("{}\n{}".format(dem_outcome, rep_outcome))

def sort_dems(senator):
    return senator['party'], senator['votes_with_party_pct']

def sort_reps(senator):
    return senator['votes_with_party_pct']

def reps_vote(senator):
    return senator['party']

if __name__ == '__main__':
    main()