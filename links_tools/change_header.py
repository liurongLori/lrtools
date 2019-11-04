import requests
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True)
    parser.add_argument('-v', '--value', required=True)
    args = parser.parse_args()

    #headers = {'X-Host': args.value,
    #            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; View XL Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'
    #           }
    headers = {'X-Host': args.value,
               }

    r = requests.get(args.url, headers=headers)

    if r.status_code == 200:
        print(r.headers)
    else:
        print(r.status_code)

