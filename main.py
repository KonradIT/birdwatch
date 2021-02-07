import birdwatch
import json

secretsinfile = json.loads(open("secrets.json").read())
secrets = birdwatch.Secrets(headers=secretsinfile.get("headers"), cookies=secretsinfile.get("cookies"))

bw = birdwatch.Birdwatch(auth=secrets, debug=True)
d= bw.fetch_public_data()
bw.save(d)