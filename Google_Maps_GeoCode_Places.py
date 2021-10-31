from urllib.parse import urlencode
import requests

#ref https://console.cloud.google.com/
google_api_key="use your api key from google cloud"


class GoogleMapApi(object):
    
    lat,lng=None,None
    data_type='json'
    location_query=None
    api_key=None

    def __init__(self,api_key=None,address_or_postal_code = None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if api_key==None:
            raise Exception("Api Key is required")
        self.api_key=api_key
        self.location_query=address_or_postal_code
        if self.location_query != None:
            self.extract_lat_long()


    #simply extract the lat long for the city you provide 
    def extract_lat_long(self,location=None):
        loc_query=self.location_query
        if location != None:
            loc_query=location
        endpoint=f'https://maps.googleapis.com/maps/api/geocode/{self.data_type}'
        params={"address":loc_query,"key":self.api_key}
        url_param=urlencode(params)
        url=f'{endpoint}?{url_param}'
        r=requests.get(url)
        if r.status_code not in range(200,299):
            return {}
        latlng={}
        try:
            latlng=r.json()['results'][0]['geometry']['location']
            # lt=r.json()
            
        except:
            pass
        # print(lt)
        lat,lng=latlng.get('lat'),latlng.get('lng')
        self.lat,self.lng=lat,lng
        return lat,lng

    #search specific details like chinese food related restro with details
    def search(self,keywords='Nepali food',radius=1500,location=None):
        lat,lng=self.lat,self.lng
        if location!=None:
            lat,lng=self.extract_lat_long(location=location)

        base_endpoint_places2=f'https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}'
        parms={
            'key':self.api_key,
            "location":f"{lat},{lng}",
            "radius":radius,
            "keyword":keywords

        }
        parms_encoded=urlencode(parms)
        places_url=f"{base_endpoint_places2}?{parms_encoded}"

        r=requests.get(places_url)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    #to search for the details of a place,default value is for rangeli
    def detail(self,place_id='ChIJFxmRolh-7zkR5hR69DtpRQI'):
        base_endpoint_places_details=f"https://maps.googleapis.com/maps/api/place/details/{self.data_type}"
        # sample_main_url_we_need='https://maps.googleapis.com/maps/api/place/details/json?fields=name%2Crating%2Cformatted_phone_number&place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&key=YOUR_API_KEY'
        params_places_details={
            'key':self.api_key,
            'place_id':f"{place_id}",
            'fields':'name,rating,formatted_phone_number,formatted_address'
            
        }

        detail_param_encoded_places=urlencode(params_places_details)
        final_url=f"{base_endpoint_places_details}?{detail_param_encoded_places}"
        
        r=requests.get(final_url)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
               


client=GoogleMapApi(api_key=google_api_key,address_or_postal_code='Rangeli, Nepal')
#this will provide lat long for rangeli
# print(client.lat,client.lng)
#Belo fucttion call will find Nepali food(which is default) restro in auckland
# print(client.search(location="Auckland,New Zealand"))
#to find details of place using place id,default is provided
print(client.detail())