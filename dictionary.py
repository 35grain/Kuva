dictionary = {"clear sky": "selge taevas", "few clouds": "vähepilvine" , "scattered clouds": "pilvine", "broken clouds": "pilvine", "shower rain": "uduvihm", "rain": "vihm", "thunderstorm": "äikesetorm", "snow": "lumesadu", "mist": "udu", 
"light intensity drizzle": "kerge uduvihm", "drizzle": "uduvihm", "heavy intensity drizzle": "tugev uduvihm", "light intensity drizzle rain": "kerge uduvihm", "drizzle rain": "uduvihm", "heavy intensity drizzle rain": "tugev uduvihm", "shower rain and drizzle": "uduvihm", "heavy shower rain and drizzle": "vihm", "shower drizzle": "vihm", "light rain": "kerge vihm", "moderate rain": "vihm", "heavy intensity rain": "tugev vihm", 
"heavy intensity rain": "tugev vihm", "very heavy rain": "väga tugev vihm", "extreme rain": "erakordselt tugev vihm", "freezing rain": "külm vihm", "light intensity shower rain": "nõrk vihm", "shower rain": "uduvihm", "heavy intensity shower rain": "tugev uduvihm", "ragged shower rain": "vahelduv uduvihm", 
"light snow": "kerge lumesadu", "Snow": "lumesadu", "Heavy snow": "tugev lumesadu", "Sleet": "rahe", "Light shower sleet": "kerge rahe", "Shower sleet": "rahe", "Light rain and snow": "õrn lörts", "Rain and snow": "lörts", "Light shower snow": "väike lörts", "Shower snow": "lumesadu", "Heavy shower snow": "lumesadu", 
"mist": "udu", "Smoke": "suits", "Haze": "sudu", "sand/ dust whirls": "liivatorm", "fog": "udu", "sand": "liiv", "dust": "tolm", "volcanic ash": "vulkaanituhk", "squalls": "tugev tuul", "tornado": "tornaado", 
"clear sky": "selge taevas", "few clouds": "õrn pilvisus", "scattered clouds": "pilves", "broken clouds": "pilves", "overcast clouds": "tugev pilvisus"}

def translate(word):
    if word in dictionary:
        return dictionary[word]
    