import requests, SignerPy, json, secrets, uuid, binascii, os, time, random
import httpx, asyncio


class PhoneToUsernameTikTok:
   def __init__(self,number:str) -> None:
      self.number=number
      self.secret = secrets.token_hex(16)
      self.client=self.client_builder()
      self.host = self.listHost()
      self.xor_number = self.xor(self.number)
      self.params = self.__get_param()
      self.cookies =  {"passport_csrf_token": self.secret,"passport_csrf_token_default": self.secret,"install_id": self.params["iid"],}
      
   def listHost(self) -> list[str]:
       # list of host tiktok
       return [
        "api16-normal-va.tiktokv.com",
        "api16-normal-c-alisg.tiktokv.com",
        "api16-normal-zr.tiktokv.com",
        "api31-normal-useast2a.tiktokv.com",
        "api16-normal-useast5.us.tiktokv.com",
        "api19-normal-useast8.us.tiktokv.com",
        "api31-normal-alisg.tiktokv.com",
        "api16-normal-c-tw.tiktokv.com",
        "api31-normal-zr.tiktokv.com",
        "api16-normal-no1a.tiktokv.eu",
        "api19-normal-ycru.tiktokv.com",
        "api16-normal.tiktokv.com",
        "api16-normal.ttapis.com",
        "api31-normal.tiktokv.com",
        "api22-normal.tiktokv.com",
        "api19-normal.tiktokv.com",
        "api-normal.tiktokv.com",
        "api21-normal.tiktokv.com",
        "api16-core.tiktokv.com",
        "api16-core-va.tiktokv.com",
        "api32-normal.tiktokv.com",
        "api33-normal.tiktokv.com"
    ]
       
   def client_builder(self) -> httpx.AsyncClient:
       return httpx.AsyncClient(http2=True,follow_redirects=True)
       
   def xor(self,string:str) -> str:
      return "".join([hex(ord(c) ^ 5)[2:] for c in string])
      
   def __get_param(self) -> dict:
       return {
        "request_tag_from": "h5",
        "fixed_mix_mode": "1",
        "mix_mode": "1",
        "account_param":self.xor_number,
        "scene": "1",
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "type": "3736",
        "_rticket": str(round(int(time.time()*1000))),
        "cdid": str(uuid.uuid4()),
        "channel": "googleplay",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "370805",
        "version_name": "37.8.5",
        "manifest_version_code": "2023708050",
        "update_version_code": "2023708050",
        "ab_version": "37.8.5",
        "resolution": "1600*900",
        "dpi": "240",
        "device_type": "SM-G998B",
        "device_brand": "samsung",
        "language": "en",
        "os_api": "28",
        "os_version": str(random.randint(7,33)) + "." + str(random.randint(0,9)) + "."+str(random.randint(0,9)),
        "ac": "wifi",
        "is_pad": "0",
        "current_region": "TW",
        "app_type": "normal",
        "sys_region": "US",
        "last_install_time": str(round(int(time.time()*1000))),
        "mcc_mnc": "46692",
        "timezone_name": "Asia/Baghdad",
        "carrier_region_v2": "466",
        "residence": "TW",
        "app_language": "en",
        "carrier_region": "TW",
        "timezone_offset": "10800",
        "host_abi": "arm64-v8a",
        "locale": "en-GB",
        "ac2": "wifi",
        "uoo": "1",
        "op_region": "TW",
        "build_number": "37.8.5",
        "region": "GB",
        "ts":str(round(int(time.time()))),
        "iid": str(random.randint(7400000000000000000, 7499999999999999999)),
        "device_id": str(random.randint(7400000000000000000, 7499999999999999999)),
        "openudid": str(binascii.hexlify(os.urandom(8)).decode()),
        "support_webview": "1",
        "okhttp_version": "4.2.210.6-tiktok",
        "use_store_region_cookie": "1",
        "app_version":"37.8.5"}
   #/*
   # this method return fake mail using temp mail io apis you can use mail tm apis (this better)
   #*\
   async def __get_email(self) -> str:
       try:
           response = await self.client.post('https://api.internal.temp-mail.io/api/v3/email/new')
           return response.json()["email"]
       except json.JSONDecodeError as e:
           return e
  
   #/*
   # this method get inbox from email (tempmail.io) apis  the response of get inbox is list( [] )
   # *\        
   async def __get_inbox(self,email:str) -> httpx.Response.json:
       try:
          response = await self.client.get(f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages')
         
          return response.json()
       except json.JSONDecodeError as e:
            return e
    
   # /*
   # get random host from list of host (all country in tiktok have host for example if use ASIA host and use american email the tiktok server return attemps)
   #*\
   def __get_host(self) -> str:
       return random.choice(self.listHost())
   
   #/*
   # get headers with signature(x-khronos,x-gorgon,x-ladon,x-argus,etc..) need signature from SignerPy (gogron 8404) and params
   # *\
   def __get_header(self, signature,parma:dict[str:str,str:str]) -> httpx.Headers:
      return  {
        'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_"+parma["region"]+"; "+parma["device_type"]+"; Build/SP1A.210812.016;tt-ok/3.12.13.16)",
        'Accept': "application/json, text/plain, */*",
        'x-ss-stub':signature['x-ss-stub'],
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket':signature['x-ss-req-ticket'],
        'x-ladon': signature['x-ladon'],
        'x-khronos': parma["ts"], # x-khroons = ts (params value)
        'x-argus': signature['x-argus'],
        'x-gorgon': signature['x-gorgon'],#version 8404 because he start in 8404
        'content-type': "application/x-www-form-urlencoded",
        'content-length': '0', # str(len(payload)) if payload else '0', 
        # content-length  = lengthe of payload(data) send to server
        }
   #/*
   # this method get  passport ticket 
   # *\
   async def __ticket_request(self) -> httpx.Response:
      try:
        signature = SignerPy.sign(params=self.params,cookie=self.cookies,aid=1233,version=8404)
        response = await self.client.post("https://"+self.__get_host()+"/passport/account_lookup/mobile/", headers=self.__get_header(signature,self.params), params=self.params, cookies=self.cookies)
        # if response return captch
        # return captch
        # if many captch in this response use did(deivce_id,iid) using in this request to solve captch and try another
        
        if "'verify_center_decision_conf'" in response.text:
            return "Captch"
        if response.json()["data"] == None:
            # if phone number not linked any account tiktok
            return None
        #else return response to get all info
        return response
      except Exception as e:
          #except return run method if host not work try another host 
          return await self.__ticket_request()

   async def send_code(self) -> str:
      email = await self.__get_email() #get fake mail
      response_ticket = await self.__ticket_request() # send ticket request
      if response_ticket == None:
          return "Phone Number Not found in TikTok"
      if response_ticket == "Captch":
          return await self.send_code()
      try:
          ticket = response_ticket.json()["data"]["accounts"][0]["passport_ticket"]
          
      except Exception as e:
        # if not return ticket in response try another 
        return await self.send_code()
          
      host = str(response_ticket.url).split("/passport/account_lookup/mobile/")[0].split("https://")[1]
      # get host from url
 

      
      self.params.update({"not_login_ticket": ticket, "email": self.xor(email),"ts":str(round(int(time.time()))),"_rticket": str(round(int(time.time()*1000)))})
      signature = SignerPy.sign(params=self.params, cookie=self.cookies,aid=1233,version=8404)
      #aid = 1233 app
      response = await self.client.post("https://"+host+"/passport/email/send_code/", headers=self.__get_header(signature,self.params), params=self.params, cookies=self.cookies)
      if "email_ticket" in response.text:
          await asyncio.sleep(5)
          inbox = await self.__get_inbox(email)
          username = await self.__extraxt_username(inbox)
          return username
      else:
          return await self.send_code()
          
   async def __extraxt_username(self,inbox:httpx.Response.json) -> str:
       try:
            username =inbox[0]["body_text"].split("\n\nTikTok 6-digit code\n\nHi ")[1].split(",")[0]
            #extract username from inbox dict
            return username
       except Exception as e:
            return str(e)

  

if __name__ == "__main__":
    username = asyncio.run(PhoneToUsernameTikTok(input("Enter Phone Number with country key :")).send_code())
    if username == "Phone Number Not found in TikTok":
        print("Phone Number Not found in TikTok")
    else:
        print("username -> ", username)
#include<string.h>
#include<stdlib.h>
#include<io.h> // if unix systems(mac,linux,freebsd) use #include<unistd.h>
# typedef struct{
#     size_t __n;
# }n;
# typedef struct{
#     n *_n;
#     char *__buf;
# }printf;
# static inline printf *print(printf *mm){
#     write(1,mm->__buf,mm->_n->__n);
#     return mm;
# }
# int main(int argc,char **argv[]){
#     printf *f = (printf*)malloc(sizeof(printf));
#     f->_n = (n*)malloc(sizeof(n));
#     f->__buf="S1(Ntro,Atro) Programming";
#     f->_n->__n = strlen(f->__buf);
#     f = print(f);
#     free(f->_n);
#     free(f);
#     return 0;
# }
# by -> s1
# join my channel -> https://t.me/+xOTpUVUrZkgwYzVl
# هسا تكول ليش مخلي هواي تعليقات
# اكلك حتى تفهم اداه شون تشتغل
