import http

def send(message, webhook):

	conn = http.client.HTTPSConnection("discordapp.com")

	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + \
		message + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

	headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
          		'cache-control': "no-cache",
        }

	conn.request("POST", webhook, payload.encode("utf-8"), headers)

	res = conn.getresponse()
	data = res.read()

