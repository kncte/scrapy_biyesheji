import requests
import execjs
import os

# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建完整的文件路径
file_path = os.path.join(current_dir, '163music.js')

# 打开文件
with open(file_path, 'r', encoding='utf-8') as f:
    js = f.read()
jscode = execjs.compile(js)


def Download(id):
    key = '{{"ids":"[{}]","level":"standard","encodeType":"aac","csrf_token":""}}'.format(id)
    print(key)
    music_url = jscode.call('get_musicId', key)
    print(music_url)
    headers = {
        "authority": "music.163.com",
        "sec-ch-ua": "\"Chromium\";v=\"21\", \" Not;A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "sec-ch-ua-platform": "\"Windows\"",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "*/*",
        "origin": "https://music.163.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://music.163.com/",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    cookies = {
        "_ntes_nnid": "6c21e4b3fbbbd3cfc69382b32ce3c4c5,1681142831856",
        "_ntes_nuid": "6c21e4b3fbbbd3cfc69382b32ce3c4c5",
        "WNMCID": "sghqht.1681142832188.01.0",
        "WEVNSM": "1.0.0",
        "WM_TID": "IMl9I0oViPhEBUUVRRKUKjmfqNritVyu",
        "__bid_n": "187ac6473a79ff4a184207",
        "FPTOKEN": "6pK2sZXFwhGqOH7mbrpn0z8YzgJ1VFjcNNgabTw0aLkZYfRH+JEZ6oNFSVKU6ziR5j2RHT+wk7AKswNy7L/dscEwEX5XWYFrCdFw7HjFVcsNkUoi5u134EPGYciie0+57ndPFe0avEKExrUhVCl7688KgzpWxQjmOrtQ6hZ9PrKTJks6Xsawt9PYGM9mv6zolHHQzqBCmvgo3wPYz1nu68JO+JwMzIgrVuLYR1olMykbV2fZux8C92uxUoQHc80r4F6zwciT1hiDVXk8vgwsZYnb8lamc0yA1EDbvj38w1LLnCaGAIesbiBRD5XATvSbe7vTWbxskJytaHKetlrnx4mWaSuONv2Goriv9Dku1siiU0erraqeND1vkz9maI+OZ6h92b0iewK31C2TN67GkA==|bwIjMsutTsHSG3AA6rFzo/N+I0J7PiKdkU+4YM2rJhA=|10|9934c6280a40737231aa1ec78f16e890",
        "NMTID": "00OcQ0gOn8BK5ZMzUwUv9vYsZNOvgkAAAGHrHwxWA",
        "ntes_kaola_ad": "1",
        "sDeviceId": "YD-QEimUXqzsfdFF1EFVAfE0E3kbZw2KPBM",
        "ntes_utid": "tid._.z4lW7969MzhFAwBQFROQgFiuKtOxCW7v._.0",
        "_iuqxldmzr_": "32",
        "__root_domain_v": ".163.com",
        "_qddaz": "QD.537085161169138",
        "NTES_P_UTID": "ao7zMwfyO36a959lTMCs0aJDTNq4bOqY|1685535419",
        "P_INFO": "m15177817192@163.com|1685535419|1|mail163|00&99|null&null&null#gux&450100#10#0#0|151192&1||15177817192@163.com",
        "nts_mail_user": "15177817192@163.com:-1:1",
        "_ga": "GA1.1.198386827.1686033535",
        "Qs_pv_382223": "101054986232919570",
        "Qs_lvt_382223": "1686033534",
        "_clck": "86s5wg|2|fc8|0|1252",
        "_ga_C6TGHFPQ1H": "GS1.1.1686033534.1.1.1686034944.0.0.0",
        "WM_NI": "pPFbj%2F4sQ6Qh5Zuhp9uZM8QLM1HoKN1IHwo8ps2zsRTvW8QpWNAJQuZYEtg4BJeZisSfg%2Fn%2Ff07bv%2B4ZHTeNio7ShUUxzLhaSEm1%2B5ZFwsxvkQXEp2LUd%2F1F7OKjZEqXTjE%3D",
        "WM_NIKE": "9ca17ae2e6ffcda170e2e6eed4f1398a99bd97f83bada88eb2c45a869a9aadc864b7b689aff57d8fa7abb8dc2af0fea7c3b92ab4908a83e925f8ad9fd7d464f786bb89f333b78683d9d4488fef8890ca46f3978898ee34b4adfe9bf25a98aa99d9d47c95928fabd47f9a878b95e6408296abbbec7991baa9d0ed25a6f0f983f521f88688b5e846abb1f9b4eb5f97a8b6adeb6b919ba3d2aa3f9a9ab994fb7ea98f98a6f33a908bacd0b44ef591858bd94fb3889c8bc837e2a3",
        "JSESSIONID-WYYY": "RIkMwuUEF1R4WlQuW%5CqZdDzl%5CK3XIcKdrFk%2BzPrxcF%2B2Qac%5CWH3%2Bs5AhnNxn%2Fugd3PE6fSobCxd5NsgkvWugvAugoImCNgzxXkDnTInPJIWkBFo7CEHH8HZJHgu44dIpPRSg9ql4S2UiDj4M2%2FaIuc6ce7%2B6E3PxUFN%5CdQ9rF9ve%2BT%2Bj%3A1691843034549",
        "playerid": "33819245"
    }
    url = "https://music.163.com/weapi/song/enhance/player/url/v1"
    params = {
        "csrf_token": ""
    }
    data = {
        # "params": "nKYUop/WYY48FL22qh04M1xuaEUS+BCgrwZNxRmIZLWSBNg27F/WSfB/Q79SF5HF6/13voyRBjttDCxvtsdY4/7jnqHbOoOKeF02OyZ83BmzgpK5iNjcMYTnd2acpjtNyZB8xu9j1c5NeVIG3CfckQ==",
        # "encSecKey": "35eb2ad672af66981cf5b22782c7d46afd66606ff75c67c0844cb43f56d06007c960f58e6c05b73ef41fffdbd135dd4a3c7b5243203937cbaaa4709033991d839acaf9abb4d7b29303339e0c36b32b393a9008bc985a0fff9ab8a6a1a58ed4bdb86b57037157a11b3c1ee97f934bbd44f52dced1c411bc9d6c16b403ad7db3d6"
        "params": music_url['encText'],
        "encSecKey": music_url['encSecKey']
    }

    response = requests.post(url, headers=headers, params=params, data=data).json()
    if response:
        print(response)
        return response['data'][0]['url']
    else:
        return 0
