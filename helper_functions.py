
def build_url(url, *params):
    for param in params:
        field = param[0]
        value = param[1]
        url = url + "%s=%s&" % (field,value)
    url = url[:-1]
    return url
        
        

    
