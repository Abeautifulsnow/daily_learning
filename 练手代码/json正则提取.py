import re

s = '''
{"count":3,"next":null,"previous":null,"results":[{"id":1,"username":"admin","password":"pbkdf2_sha256$120000$h8Nrgz8wfkO0$G1QCYGMX5pr/wYqtfZKlK5B7BfU1sH2Sp96e8dVSL6Q=","email":"15639936570@189.cn","date_joined":"2018-11-11T10:10:00"},{"id":3,"username":"WanFQ","password":"pbkdf2_sha256$120000$ogKQsNdB2Zuj$Nt569LmMWq5J3hg8LnRa837Ot6DeO+mrC+qriT8RkOM=","email":"2567809010@qq.com","date_joined":"2018-11-22T00:04:00"},{"id":4,"username":"Runstone","password":"pbkdf2_sha256$120000$spnYMm9F5Pjr$tgo+Ecz4dnkwXmf3R50jAEU7YJJ/raq26dRVJAuhfHE=","email":"","date_joined":"2018-12-06T00:20:00"}]}
'''
c = re.findall(r'\"id\":.*?(?=,)', s)
d = re.findall(r'\"username\":\".*?\"', s)
print(c)
print('='*88)
print(d)
