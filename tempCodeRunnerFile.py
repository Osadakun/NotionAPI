try:
      quantity = req.json()['results'][i]['properties']['日付']['date']['start']
    except TypeError:
      pass
    else:
      pass